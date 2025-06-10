#!/usr/bin/env python3
"""
命令行测试脚本 - 不依赖Web界面直接测试核心功能
"""
import asyncio
from graph_service import create_graph, run_graph


def test_basic_functionality():
    """测试基本功能"""
    print("🚀 开始测试AI投资分析系统...")
    print("=" * 50)
    
    # 测试参数
    symbols = ["AAPL", "MSFT"]
    selected_agents = ["buffett_analyst", "tech_analyst"]
    initial_cash = 100000.0
    
    print(f"📊 分析股票: {', '.join(symbols)}")
    print(f"🤖 使用代理: {', '.join(selected_agents)}")
    print(f"💰 初始资金: ${initial_cash:,.2f}")
    print()
    
    # 创建和编译图
    print("📈 创建AI代理工作流...")
    graph = create_graph(selected_agents)
    compiled_graph = graph.compile()
    print("✅ 工作流创建成功")
    print()
    
    # 执行分析
    print("🔄 开始执行分析...")
    result = run_graph(compiled_graph, symbols, initial_cash)
    
    # 输出结果
    print("\n" + "=" * 50)
    print("📋 分析结果汇总:")
    print("=" * 50)
    
    # 显示消息历史
    messages = result.get("messages", [])
    print("\n📝 执行日志:")
    for i, msg in enumerate(messages, 1):
        if hasattr(msg, 'content'):
            print(f"  {i}. {msg.content}")
    
    # 显示最终决策
    final_decisions = result.get("data", {}).get("final_decisions", {})
    if final_decisions:
        print("\n🎯 投资决策:")
        for symbol, decision in final_decisions.items():
            action = decision['action']
            position = decision['position_size']
            reason = decision['reason']
            
            # 颜色编码
            action_emoji = {"买入": "🟢", "卖出": "🔴", "持有": "🟡"}.get(action, "⚫")
            
            print(f"  {action_emoji} {symbol}: {action}")
            print(f"     └─ 仓位大小: {position:.1%}")
            print(f"     └─ 决策理由: {reason}")
            print()
    
    # 显示分析师结果
    analysis_results = result.get("data", {}).get("analysis_results", {})
    if analysis_results:
        print("🔍 分析师详细结果:")
        for analyst, results in analysis_results.items():
            print(f"\n  📊 {analyst}:")
            for symbol, analysis in results.items():
                print(f"     {symbol}: {analysis}")
    
    # 显示风险评估
    risk_assessment = result.get("data", {}).get("risk_assessment", {})
    if risk_assessment:
        print("\n⚠️  风险评估:")
        for symbol, risk in risk_assessment.items():
            risk_level = risk.get('risk_level', 'N/A')
            var = risk.get('var_1_day', 0)
            max_pos = risk.get('max_position', 0)
            
            risk_emoji = {"低": "🟢", "中": "🟡", "高": "🔴"}.get(risk_level, "⚫")
            
            print(f"  {risk_emoji} {symbol}: 风险等级 {risk_level}")
            print(f"     └─ 日VaR: {var:.2%}")
            print(f"     └─ 最大仓位: {max_pos:.1%}")
    
    print("\n" + "=" * 50)
    print("✨ 测试完成!")


if __name__ == "__main__":
    test_basic_functionality() 