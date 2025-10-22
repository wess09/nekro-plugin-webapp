/**
 * Cloudflare Worker 自动部署脚本
 * 
 * 功能：
 * 1. 检查 D1 数据库是否存在
 * 2. 如果不存在则创建数据库
 * 3. 更新 wrangler.toml 中的 database_id
 * 4. 初始化数据库表结构
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WRANGLER_TOML = path.join(__dirname, 'wrangler.toml');
const SCHEMA_SQL = path.join(__dirname, 'schema.sql');
const DATABASE_NAME = 'webapp-db';

console.log('🚀 开始配置 Cloudflare Worker...\n');

/**
 * 执行命令并返回输出
 */
function exec(command) {
  try {
    return execSync(command, { encoding: 'utf-8', stdio: 'pipe' });
  } catch (error) {
    return error.stdout || error.stderr || '';
  }
}

/**
 * 检查数据库是否存在
 */
function checkDatabaseExists() {
  console.log('📊 检查数据库是否存在...');
  const output = exec('wrangler d1 list');
  return output.includes(DATABASE_NAME);
}

/**
 * 创建数据库
 */
function createDatabase() {
  console.log('📦 创建数据库...');
  const output = exec(`wrangler d1 create ${DATABASE_NAME}`);
  console.log(output);
  
  // 从输出中提取 database_id
  const match = output.match(/database_id\s*=\s*"([^"]+)"/);
  if (match && match[1]) {
    return match[1];
  }
  
  // 如果创建失败，尝试从列表中获取
  const listOutput = exec('wrangler d1 list');
  const listMatch = listOutput.match(new RegExp(`${DATABASE_NAME}.*?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})`, 'i'));
  if (listMatch && listMatch[1]) {
    return listMatch[1];
  }
  
  return null;
}

/**
 * 从 wrangler.toml 中获取 database_id
 */
function getDatabaseId() {
  const content = fs.readFileSync(WRANGLER_TOML, 'utf-8');
  const match = content.match(/database_id\s*=\s*"([^"]+)"/);
  return match ? match[1] : null;
}

/**
 * 更新 wrangler.toml 中的 database_id
 */
function updateDatabaseId(databaseId) {
  console.log(`📝 更新配置文件 (database_id: ${databaseId})...`);
  let content = fs.readFileSync(WRANGLER_TOML, 'utf-8');
  
  // 替换 database_id
  if (content.includes('database_id')) {
    content = content.replace(
      /database_id\s*=\s*"[^"]*"/,
      `database_id = "${databaseId}"`
    );
  } else {
    // 如果没有 database_id，在 database_name 后面添加
    content = content.replace(
      /(database_name\s*=\s*"[^"]+")/,
      `$1\ndatabase_id = "${databaseId}"`
    );
  }
  
  fs.writeFileSync(WRANGLER_TOML, content, 'utf-8');
  console.log('✅ 配置文件已更新\n');
}

/**
 * 初始化数据库
 */
function initializeDatabase(databaseId) {
  console.log('🗄️  初始化数据库表结构...');
  
  // 检查 schema.sql 是否存在
  if (!fs.existsSync(SCHEMA_SQL)) {
    console.log('⚠️  schema.sql 文件不存在，跳过初始化');
    return;
  }
  
  // 执行 SQL
  try {
    const output = exec(`wrangler d1 execute ${DATABASE_NAME} --file=${SCHEMA_SQL}`);
    console.log(output);
    console.log('✅ 数据库初始化完成\n');
  } catch (error) {
    // 如果表已存在，忽略错误
    if (error.message && error.message.includes('already exists')) {
      console.log('ℹ️  数据库表已存在，跳过初始化\n');
    } else {
      console.log('⚠️  数据库初始化失败（可能已初始化）\n');
    }
  }
}

/**
 * 主函数
 */
function main() {
  try {
    // 1. 检查 wrangler.toml 中是否已有 database_id
    let databaseId = getDatabaseId();
    
    if (databaseId && databaseId.length > 20) {
      console.log(`✅ 数据库已配置 (ID: ${databaseId.substring(0, 8)}...)\n`);
    } else {
      // 2. 检查数据库是否存在
      const exists = checkDatabaseExists();
      
      if (exists) {
        console.log('✅ 数据库已存在\n');
        // 尝试从列表中获取 database_id
        const listOutput = exec('wrangler d1 list');
        const match = listOutput.match(new RegExp(`${DATABASE_NAME}.*?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})`, 'i'));
        if (match && match[1]) {
          databaseId = match[1];
        }
      } else {
        // 3. 创建数据库
        databaseId = createDatabase();
        if (!databaseId) {
          console.error('❌ 无法创建或获取数据库 ID');
          process.exit(1);
        }
        console.log(`✅ 数据库创建成功 (ID: ${databaseId.substring(0, 8)}...)\n`);
      }
      
      // 4. 更新配置文件
      if (databaseId) {
        updateDatabaseId(databaseId);
      }
    }
    
    // 5. 初始化数据库（如果需要）
    if (databaseId) {
      initializeDatabase(databaseId);
    }
    
    console.log('🎉 配置完成！准备部署 Worker...\n');
    
  } catch (error) {
    console.error('❌ 配置失败:', error.message);
    process.exit(1);
  }
}

main();

