#!/bin/bash
# 测试 Ralph 改进效果

echo "🧪 测试 Ralph 改进..."
echo ""

# 1. 测试 confidence 计算
echo "1️⃣ 测试 Confidence 计算改进"
echo "----------------------------------------"

# 创建测试用的 JSON 输出
cat > /tmp/test_output.json <<EOF
{
  "type": "result",
  "subtype": "success",
  "result": "Successfully created 3 files and modified 2 existing files. All tests passed.",
  "sessionId": "test-session-123",
  "metadata": {
    "files_changed": 5,
    "has_errors": false
  }
}
EOF

# 调用 response_analyzer
source ~/.ralph/lib/date_utils.sh
source ~/.ralph/lib/response_analyzer.sh

echo "测试场景：修改了 5 个文件，输出长度 90 字符"
parse_json_response /tmp/test_output.json /tmp/test_result.json
confidence=$(jq -r '.confidence' /tmp/test_result.json)
echo "计算出的 Confidence: $confidence%"
echo ""

# 2. 测试退出机制不受影响
echo "2️⃣ 验证退出机制独立性"
echo "----------------------------------------"
if grep -q "confidence" ~/.ralph/lib/circuit_breaker.sh; then
    echo "⚠️  警告：断路器中使用了 confidence"
else
    echo "✅ 确认：断路器不使用 confidence，只基于进展判断"
fi
echo ""

# 3. 显示实时输出改进
echo "3️⃣ 实时输出改进"
echo "----------------------------------------"
echo "新的 jq 过滤器将显示："
echo "  • 工具名称：⚡ [Read]"
echo "  • 工具参数：📋 {command: 'ls -la', ...}"
echo "  • 执行结果：✅ 成功 / ❌ 错误"
echo ""

# 清理
rm -f /tmp/test_output.json /tmp/test_result.json

echo "✅ 测试完成！"
echo ""
echo "📌 下一步：运行实际任务测试"
echo "   cd D:/AI_Projects/system-max"
echo "   bash ~/.ralph/ralph_loop.sh --live --verbose --reset-circuit"
