/**
 * chrono-syntax-check.js
 * 从 chrono-simulation-standalone.html 提取所有 <script> 块，
 * 用 node -c 逐块验证 JS 语法。
 *
 * 用法：node chrono-syntax-check.js
 * 退出码：0 = 全部通过，1 = 有语法错误
 */

var fs = require('fs');
var path = require('path');

var file = path.join(__dirname, 'chrono-simulation-standalone.html');
var src = fs.readFileSync(file, 'utf8');

// 提取所有 <script> 块内容（跳过含 src= 的外部脚本）
var scriptRe = /<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi;
var blocks = [];
var m;
while ((m = scriptRe.exec(src)) !== null) {
  var tag = m[0].substring(0, 60);
  if (m[1].trim().length > 0) {
    blocks.push({ index: blocks.length + 1, tag: tag, code: m[1] });
  }
}

console.log('[syntax-check] Found ' + blocks.length + ' inline script block(s)\n');

var passed = 0;
var failed = 0;

blocks.forEach(function(b) {
  // 写临时文件给 node -c 检查
  var tmpFile = path.join(__dirname, '_syntax_tmp_' + b.index + '.js');
  fs.writeFileSync(tmpFile, b.code, 'utf8');

  try {
    var result = require('child_process').execSync(
      'node -c "' + tmpFile + '" 2>&1',
      { encoding: 'utf8' }
    );
    console.log('[PASS] Block #' + b.index);
    passed++;
  } catch (e) {
    console.log('[FAIL] Block #' + b.index);
    console.log('  Tag: ' + b.tag + '...');
    console.log('  Error: ' + e.stdout.trim());
    console.log('  First 200 chars of block: ' + b.code.substring(0, 200).replace(/\n/g, '\\n'));
    console.log();
    failed++;
  }

  try { fs.unlinkSync(tmpFile); } catch (_) {}
});

console.log('\n[syntax-check] Result: ' + passed + ' passed, ' + failed + ' failed');
process.exit(failed > 0 ? 1 : 0);
