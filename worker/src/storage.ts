/**
 * 数据库存储操作模块
 */

import { Env, Page, ApiKey, CreatePageRequest } from './types';

/**
 * 生成唯一的页面 ID
 */
function generatePageId(): string {
	return crypto.randomUUID().substring(0, 8);
}

/**
 * 创建页面
 */
export async function createPage(request: CreatePageRequest, createdBy: string, env: Env): Promise<Page> {
	const now = Date.now();
	const pageId = generatePageId();
	const expiresAt = request.expires_in_days && request.expires_in_days > 0 ? now + request.expires_in_days * 24 * 60 * 60 * 1000 : null;

	await env.DB.prepare(
		`
            INSERT INTO pages (
                page_id, title, description, html_content,
                created_by, created_at, expires_at, is_active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        `
	)
		.bind(pageId, request.title, request.description, request.html_content, createdBy, now, expiresAt)
		.run();

	return {
		page_id: pageId,
		title: request.title,
		description: request.description,
		html_content: request.html_content,
		created_by: createdBy,
		created_at: now,
		expires_at: expiresAt,
		access_count: 0,
		last_accessed: null,
		is_active: 1,
		metadata: null,
	};
}

/**
 * 获取页面
 */
export async function getPage(pageId: string, env: Env): Promise<Page | null> {
	const result = await env.DB.prepare('SELECT * FROM pages WHERE page_id = ? AND is_active = 1').bind(pageId).first<Page>();

	if (!result) {
		return null;
	}

	// 检查是否过期
	if (result.expires_at && result.expires_at < Date.now()) {
		return null;
	}

	return result;
}

/**
 * 更新访问计数
 */
export async function incrementAccessCount(pageId: string, env: Env): Promise<void> {
	await env.DB.prepare(
		`
            UPDATE pages 
            SET access_count = access_count + 1, last_accessed = ?
            WHERE page_id = ?
        `
	)
		.bind(Date.now(), pageId)
		.run();
}

/**
 * 删除页面
 */
export async function deletePage(pageId: string, env: Env): Promise<boolean> {
	const result = await env.DB.prepare('UPDATE pages SET is_active = 0 WHERE page_id = ?').bind(pageId).run();

	return result.success;
}

/**
 * 列出所有页面
 */
export async function listPages(env: Env, limit: number = 100): Promise<Page[]> {
	const result = await env.DB.prepare(
		`
            SELECT * FROM pages 
            WHERE is_active = 1 
            ORDER BY created_at DESC 
            LIMIT ?
        `
	)
		.bind(limit)
		.all<Page>();

	return result.results || [];
}

/**
 * 创建 API 密钥
 */
export async function createApiKey(keyName: string, keyHash: string, createdBy: string, env: Env): Promise<ApiKey> {
	const now = Date.now();
	const keyId = crypto.randomUUID().substring(0, 12);

	await env.DB.prepare(
		`
            INSERT INTO api_keys (
                key_id, key_hash, key_name, created_by,
                created_at, is_active, max_pages, permissions
            ) VALUES (?, ?, ?, ?, ?, 1, 100, 'create,view')
        `
	)
		.bind(keyId, keyHash, keyName, createdBy, now)
		.run();

	return {
		key_id: keyId,
		key_hash: keyHash,
		key_name: keyName,
		created_by: createdBy,
		created_at: now,
		expires_at: null,
		is_active: 1,
		usage_count: 0,
		max_pages: 100,
		permissions: 'create,view',
		metadata: null,
	};
}

/**
 * 列出所有 API 密钥
 */
export async function listApiKeys(env: Env): Promise<ApiKey[]> {
	const result = await env.DB.prepare('SELECT * FROM api_keys WHERE is_active = 1 ORDER BY created_at DESC').all<ApiKey>();

	return result.results || [];
}

/**
 * 删除 API 密钥
 */
export async function deleteApiKey(keyId: string, env: Env): Promise<boolean> {
	const result = await env.DB.prepare('UPDATE api_keys SET is_active = 0 WHERE key_id = ?').bind(keyId).run();

	return result.success;
}

/**
 * 获取统计信息
 */
export async function getStats(env: Env): Promise<{
	pages_count: number;
	keys_count: number;
	total_access: number;
}> {
	const pagesCount = await env.DB.prepare('SELECT COUNT(*) as count FROM pages WHERE is_active = 1').first<{ count: number }>();

	const keysCount = await env.DB.prepare('SELECT COUNT(*) as count FROM api_keys WHERE is_active = 1').first<{ count: number }>();

	const totalAccess = await env.DB.prepare('SELECT SUM(access_count) as total FROM pages WHERE is_active = 1').first<{ total: number }>();

	return {
		pages_count: pagesCount?.count || 0,
		keys_count: keysCount?.count || 0,
		total_access: totalAccess?.total || 0,
	};
}

