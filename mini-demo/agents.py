"""
🤖 AI代理模块 - 多智能体协同投资分析系统
📊 使用模拟数据展示完整的AI投资决策流程
🎯 每个代理都是独立的专家，具有特定的分析风格和专长

架构说明：
🔄 观察者模式：每个代理通过progress.update_status()实时报告工作状态
📡 状态共享：通过AgentState在所有代理间传递数据和分析结果
🎭 角色扮演：每个代理模拟真实投资专家的分析风格
⚡ 异步友好：使用time.sleep()模拟真实AI推理的耗时过程
"""
import time
import random
from langchain_core.messages import HumanMessage, AIMessage
from state import AgentState
from progress import progress


def start_node(state: AgentState):
    """🚀 起始节点 - 系统初始化和环境准备"""
    # 📢 通知前端：系统开始初始化
    progress.update_status("system", "初始化系统...", "系统启动中")
    time.sleep(1)  # ⏱️ 模拟系统启动时间
    
    # 📊 初始化共享数据结构
    state["data"].update({
        "symbols": state["data"].get("symbols", ["AAPL", "MSFT"]),  # 📈 确保有股票代码
        "analysis_results": {}  # 🔍 初始化分析结果存储
    })
    
    # ✅ 通知前端：系统准备完毕
    progress.update_status("system", "系统就绪", "初始化完成")
    return state


def analyst_agent_a(state: AgentState):
    """🏛️ 巴菲特价值投资分析师 - 专注于基本面和内在价值评估"""
    agent_name = "巴菲特分析师"
    
    # 📢 阶段1：通知开始分析
    progress.update_status(agent_name, "开始基本面分析...", "正在分析价值投资机会")
    time.sleep(2)  # ⏱️ 模拟深度基本面分析时间
    
    # 📊 生成模拟分析结果 - 基于价值投资理念
    symbols = state["data"]["symbols"]
    analysis = {}
    
    for symbol in symbols:
        # 🎲 随机生成分析结果 - 实际应用中会调用真实AI模型
        recommendation = random.choice(["买入", "持有", "卖出"])
        confidence = random.uniform(0.6, 0.95)  # 📈 信心度
        
        # 💰 价值投资风格的分析结果
        analysis[symbol] = {
            "recommendation": recommendation,
            "confidence": confidence,
            "reason": f"基于价值投资理念，{symbol}的内在价值评估显示{recommendation}信号",
            "pe_ratio": random.uniform(15, 25),      # 📊 市盈率
            "book_value": random.uniform(0.8, 1.5), # 📚 账面价值
            "div_yield": random.uniform(0.01, 0.05) # 💵 股息收益率
        }
    
    # 💾 更新共享状态 - 供后续代理使用
    state["data"]["analysis_results"]["巴菲特分析师"] = analysis
    
    # 📝 添加到消息链 - LangGraph的消息传递机制
    recommendations = [f"{s}({analysis[s]['recommendation']})" for s in symbols]
    message = f"巴菲特分析师完成分析：{', '.join(recommendations)}"
    state["messages"] = [(AIMessage(content=message))]
    
    # ✅ 阶段2：通知分析完成
    progress.update_status(agent_name, "分析完成", f"已完成{len(symbols)}只股票的基本面分析")
    return state


def analyst_agent_b(state: AgentState):
    """📈 技术分析师 - 专注于图表模式和技术指标分析"""
    agent_name = "技术分析师"
    
    # 📢 阶段1：通知开始技术分析
    progress.update_status(agent_name, "开始技术分析...", "正在分析技术指标")
    time.sleep(2)  # ⏱️ 模拟技术指标计算时间
    
    # 📊 生成模拟技术分析结果
    symbols = state["data"]["symbols"]
    analysis = {}
    
    for symbol in symbols:
        # 🎲 随机生成技术分析结果 - 实际应用中会使用真实的技术指标
        trend = random.choice(["上涨", "下跌", "横盘"])
        strength = random.uniform(0.5, 0.9)  # 📊 趋势强度
        
        # 📈 技术分析风格的结果
        analysis[symbol] = {
            "trend": trend,
            "strength": strength,
            "indicators": {
                "RSI": random.uniform(30, 70),                    # 📊 相对强弱指数
                "MACD": random.choice(["金叉", "死叉", "震荡"]),    # 🔄 MACD指标
                "MA_20": random.uniform(140, 180),               # 📈 20日移动平均线
                "volume": random.choice(["放量", "缩量", "平量"])   # 📊 成交量特征
            },
            "support_level": random.uniform(140, 160),            # 📉 支撑位
            "resistance_level": random.uniform(170, 190)         # 📈 阻力位
        }
    
    # 💾 更新共享状态 - 供风险管理代理使用
    state["data"]["analysis_results"]["技术分析师"] = analysis
    
    # 📝 添加到消息链
    trends = [f"{s}({analysis[s]['trend']})" for s in symbols]
    message = f"技术分析师完成分析：{', '.join(trends)}"
    state["messages"] = [(AIMessage(content=message))]
    
    # ✅ 阶段2：通知技术分析完成
    progress.update_status(agent_name, "分析完成", f"已完成{len(symbols)}只股票的技术分析")
    return state


def risk_manager(state: AgentState):
    """⚠️ 风险管理师 - 评估投资风险并设定仓位限制"""
    agent_name = "风险管理师"
    
    # 📢 阶段1：通知开始风险评估
    progress.update_status(agent_name, "评估投资风险...", "正在计算风险指标")
    time.sleep(1.5)  # ⏱️ 模拟风险计算和建模时间
    
    # 📊 生成模拟风险评估结果
    symbols = state["data"]["symbols"]
    risk_assessment = {}
    
    for symbol in symbols:
        # 🎲 随机生成风险指标 - 实际应用中会使用复杂的风险模型
        risk_level = random.choice(["低", "中", "高"])
        var = random.uniform(0.02, 0.15)  # 📉 风险价值（VaR）
        volatility = random.uniform(0.15, 0.45)  # 📊 波动率
        
        # ⚠️ 风险评估结果
        risk_assessment[symbol] = {
            "risk_level": risk_level,
            "var_1_day": var,                         # 📉 1日风险价值
            "volatility": volatility,                # 📊 历史波动率
            "max_position": random.uniform(0.1, 0.3), # 📏 最大仓位比例
            "correlation_score": random.uniform(0.3, 0.8),  # 🔗 与市场相关性
            "liquidity_score": random.uniform(0.7, 1.0),    # 💧 流动性评分
        }
    
    # 💾 更新共享状态 - 供投资组合管理器使用
    state["data"]["risk_assessment"] = risk_assessment
    
    # 📊 计算整体组合风险
    overall_risk = random.choice(['中等', '偏低', '偏高'])
    
    # 📝 添加到消息链
    message = f"风险评估完成：整体投资组合风险等级为{overall_risk}"
    state["messages"] = [(AIMessage(content=message))]
    
    # ✅ 阶段2：通知风险评估完成
    progress.update_status(agent_name, "风险评估完成", "已完成投资组合风险分析")
    return state


def portfolio_manager(state: AgentState):
    """💼 投资组合管理师 - 综合所有分析结果制定最终投资策略"""
    agent_name = "组合管理师"
    
    # 📢 阶段1：通知开始策略制定
    progress.update_status(agent_name, "生成投资决策...", "正在制定投资组合策略")
    time.sleep(2)  # ⏱️ 模拟策略优化和决策时间
    
    # 📊 获取所有前置分析结果
    symbols = state["data"]["symbols"]
    analysis_results = state["data"]["analysis_results"]
    risk_assessment = state["data"]["risk_assessment"]
    
    final_decisions = {}
    
    # 🎯 为每只股票制定投资决策
    for symbol in symbols:
        # 📋 收集各个专家的建议
        buffett_rec = analysis_results.get("巴菲特分析师", {}).get(symbol, {}).get("recommendation", "持有")
        tech_trend = analysis_results.get("技术分析师", {}).get(symbol, {}).get("trend", "横盘")
        risk_level = risk_assessment.get(symbol, {}).get("risk_level", "中")
        max_position = risk_assessment.get(symbol, {}).get("max_position", 0.2)
        
        # 🧠 智能决策逻辑 - 综合多个维度
        if buffett_rec == "买入" and tech_trend == "上涨" and risk_level != "高":
            # 💚 强烈买入信号：基本面+技术面+风险可控
            action = "买入"
            position = max_position * 0.8  # 📈 高仓位
        elif buffett_rec == "卖出" or tech_trend == "下跌":
            # ❌ 卖出信号：任一专家建议卖出或技术面转差
            action = "卖出"
            position = 0
        else:
            # 📊 中性信号：保持观望或小仓位
            action = "持有"
            position = max_position * 0.5  # 📉 中等仓位
        
        # 📝 记录决策及其依据
        final_decisions[symbol] = {
            "action": action,
            "position_size": position,
            "reason": f"基于{buffett_rec}建议和{tech_trend}趋势，风险等级{risk_level}",
            "confidence": random.uniform(0.7, 0.95),  # 📊 决策信心度
            "expected_return": random.uniform(-0.1, 0.2) if action != "卖出" else 0  # 📈 预期收益
        }
    
    # 💾 更新最终状态 - 整个工作流的输出
    state["data"]["final_decisions"] = final_decisions
    
    # 📝 生成决策摘要消息
    decisions_summary = ", ".join([f"{s}:{final_decisions[s]['action']}" for s in symbols])
    message = f"投资组合管理完成，最终决策：{decisions_summary}"
    state["messages"] = [(AIMessage(content=message))]
    
    # ✅ 阶段2：通知决策完成 - 整个AI分析流程结束
    progress.update_status(agent_name, "决策完成", f"已生成{len(symbols)}只股票的投资决策")
    return state


# 🎯 AI代理配置注册表 - 可扩展的专家系统
AGENT_CONFIG = {
    "buffett_analyst": {
        "name": "巴菲特分析师",                    # 🏛️ 价值投资大师
        "agent_func": analyst_agent_a,
        "description": "价值投资导向的基本面分析",
        "expertise": "基本面分析、内在价值评估、长期投资",
        "style": "保守稳健，注重企业质量"
    },
    "tech_analyst": {
        "name": "技术分析师",                      # 📈 技术分析专家
        "agent_func": analyst_agent_b,
        "description": "基于技术指标的趋势分析",
        "expertise": "技术指标、图表分析、趋势预测",
        "style": "数据驱动，关注市场情绪"
    }
} 