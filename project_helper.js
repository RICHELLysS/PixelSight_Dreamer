const fs = require('fs');
const path = require('path');

// 扫描目录
const targetDirs = ['frontend/src', 'frontend/src/stores', 'backend'];
// 扫描后缀
const targetExts = ['.ts', '.vue', '.js', '.json', '.py', '.env'];

function walkDir(dir, callback) {
    if (!fs.existsSync(dir)) return;
    fs.readdirSync(dir).forEach(f => {
        let dirPath = path.join(dir, f);
        if (fs.statSync(dirPath).isDirectory()) {
            walkDir(dirPath, callback);
        } else {
            callback(path.join(dir, f));
        }
    });
}

function stripBOM(filePath) {
    const ext = path.extname(filePath);
    if (!targetExts.includes(ext)) return;

    try {
        // 1. 读取原始二进制 Buffer
        const buf = fs.readFileSync(filePath);

        // 2. 检测 UTF-8 BOM (EF BB BF)
        if (buf.length >= 3 && buf[0] === 0xEF && buf[1] === 0xBB && buf[2] === 0xBF) {
            console.log(`💣 发现 BOM: ${filePath}`);
            
            // 3. 物理切除前3个字节
            const cleanBuf = buf.subarray(3);
            
            // 4. 写回文件
            fs.writeFileSync(filePath, cleanBuf);
            console.log(`✅ 已移除 BOM: ${filePath}`);
        }
        // 5. 检测 UTF-16 LE (FF FE) - 之前的顽固文件
        else if (buf.length >= 2 && buf[0] === 0xFF && buf[1] === 0xFE) {
            console.log(`🔄 发现 UTF-16: ${filePath}`);
            const content = buf.toString('utf16le');
            fs.writeFileSync(filePath, content, { encoding: 'utf8' });
            console.log(`✅ 已转为 UTF-8: ${filePath}`);
        }
    } catch (e) {
        console.error(`❌ 处理失败: ${filePath}`, e);
    }
}

console.log('🚀 开始二进制级 BOM 清洗...');
targetDirs.forEach(dir => {
    walkDir(path.join(__dirname, dir), stripBOM);
});