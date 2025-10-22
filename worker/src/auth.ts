/**
 * 认证和授权模块
 */

import { Env, ApiKey, AuthResult } from './types';

/**
 * 计算字符串的 SHA-256 哈希
 */
async function sha256(message: string): Promise<string> {
	const msgBuffer = new TextEncoder().encode(message);
	const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
	const hashArray = Array.from(new Uint8Array(hashBuffer));
	return hashArray.map((b) => b.toString(16).padStart(2, '0')).join('');
}

/**
 * 验证 API 密钥
 */
export async function validateApiKey(authorization: string | null, env: Env): Promise<AuthResult> {
	if (!authorization || !authorization.startsWith('Bearer ')) {
		return { valid: false };
	}

	const apiKey = authorization.substring(7);
	const keyHash = await sha256(apiKey);

	// 检查是否是管理员密钥
	if (keyHash === env.ADMIN_KEY_HASH) {
		return {
			valid: true,
			keyId: 'admin',
			permissions: ['create', 'view', 'delete', 'manage'],
		};
	}

	// 检查数据库中的密钥
	const result = await env.DB.prepare('SELECT * FROM api_keys WHERE key_hash = ? AND is_active = 1').bind(keyHash).first<ApiKey>();

	if (!result) {
		return { valid: false };
	}

	// 检查是否过期
	if (result.expires_at && result.expires_at < Date.now()) {
		return { valid: false };
	}

	// 更新使用次数
	await env.DB.prepare('UPDATE api_keys SET usage_count = usage_count + 1 WHERE key_id = ?').bind(result.key_id).run();

	return {
		valid: true,
		keyId: result.key_id,
		permissions: result.permissions.split(','),
	};
}

/**
 * 检查权限
 */
export function hasPermission(permissions: string[], required: string): boolean {
	return permissions.includes(required) || permissions.includes('manage');
}

/**
 * 生成 SHA-256 哈希（用于管理接口）
 */
export async function generateKeyHash(key: string): Promise<string> {
	return await sha256(key);
}

