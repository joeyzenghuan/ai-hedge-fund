"""
AI代理模块 - 简化版，使用mock data
"""
import time
import random
from langchain_core.messages import HumanMessage, AIMessage
from state import AgentState
from progress import progress


def start_node(state: AgentState):
    """起始节点"""
    progress.update_status("system", "初始化系统...", "系统启动中")
    time.sleep(1)  # 模拟处理时间
    
    state["data"].update({
        "symbols": state["data"].get("symbols", ["AAPL", "MSFT"]),
        "analysis_results": {}
    })
    
    progress.update_status("system", "系统就绪", "初始化完成")
    return state


def analyst_agent_a(state: AgentState):
    """分析师代理A - 巴菲特风格"""
    agent_name = "巴菲特分析师"
    progress.update_status(agent_name, "开始基本面分析...", "正在分析价值投资机会")
    time.sleep(2)  # 模拟分析时间
    
    # Mock分析结果
    symbols = state["data"]["symbols"]
    analysis = {}
    
    for symbol in symbols:
        # 随机生成分析结果
        recommendation = random.choice(["买入", "持有", "卖出"])
        confidence = random.uniform(0.6, 0.95)
        
        analysis[symbol] = {
            "recommendation": recommendation,
            "confidence": confidence,
            "reason": f"基于价值投资理念，{symbol}的内在价值评估显示{recommendation}信号"
        }
    
    # 更新状态
    state["data"]["analysis_results"]["巴菲特分析师"] = analysis
    
    # 添加消息
    recommendations = [f"{s}({analysis[s]['recommendation']})" for s in symbols]
    message = f"巴菲特分析师完成分析：{', '.join(recommendations)}"
    # state["messages"].append(AIMessage(content=message))
    state["messages"]  = [(AIMessage(content=message))]
    
    progress.update_status(agent_name, "分析完成", f"已完成{len(symbols)}只股票的基本面分析")
    return state


def analyst_agent_b(state: AgentState):
    """分析师代理B - 技术分析师"""
    agent_name = "技术分析师"
    progress.update_status(agent_name, "开始技术分析...", "正在分析技术指标")
    time.sleep(2)  # 模拟分析时间
    
    # Mock分析结果
    symbols = state["data"]["symbols"]
    analysis = {}
    
    for symbol in symbols:
        # 随机生成技术分析结果
        trend = random.choice(["上涨", "下跌", "横盘"])
        strength = random.uniform(0.5, 0.9)
        
        analysis[symbol] = {
            "trend": trend,
            "strength": strength,
            "indicators": {
                "RSI": random.uniform(30, 70),
                "MACD": random.choice(["金叉", "死叉", "震荡"])
            }
        }
    
    # 更新状态
    state["data"]["analysis_results"]["技术分析师"] = analysis
    
    # 添加消息
    trends = [f"{s}({analysis[s]['trend']})" for s in symbols]
    message = f"技术分析师完成分析：{', '.join(trends)}"
    # state["messages"].append(AIMessage(content=message))
    state["messages"] = [(AIMessage(content=message))]
    
    progress.update_status(agent_name, "分析完成", f"已完成{len(symbols)}只股票的技术分析")
    return state


def risk_manager(state: AgentState):
    """风险管理代理"""
    agent_name = "风险管理师"
    progress.update_status(agent_name, "评估投资风险...", "正在计算风险指标")
    time.sleep(1.5)  # 模拟计算时间
    
    # Mock风险评估
    symbols = state["data"]["symbols"]
    risk_assessment = {}
    
    for symbol in symbols:
        risk_level = random.choice(["低", "中", "高"])
        var = random.uniform(0.02, 0.15)  # Value at Risk
        
        risk_assessment[symbol] = {
            "risk_level": risk_level,
            "var_1_day": var,
            "max_position": random.uniform(0.1, 0.3)  # 最大仓位比例
        }
    
    # 更新状态
    state["data"]["risk_assessment"] = risk_assessment
    
    # 添加消息
    message = f"风险评估完成：整体投资组合风险等级为{random.choice(['中等', '偏低', '偏高'])}"
    # state["messages"].append(AIMessage(content=message))
    state["messages"] = [(AIMessage(content=message))]
    
    progress.update_status(agent_name, "风险评估完成", "已完成投资组合风险分析")
    return state


def portfolio_manager(state: AgentState):
    """投资组合管理代理"""
    agent_name = "组合管理师"
    progress.update_status(agent_name, "生成投资决策...", "正在制定投资组合策略")
    time.sleep(2)  # 模拟决策时间
    
    # 综合所有分析结果生成最终决策
    symbols = state["data"]["symbols"]
    analysis_results = state["data"]["analysis_results"]
    risk_assessment = state["data"]["risk_assessment"]
    
    final_decisions = {}
    
    for symbol in symbols:
        # 综合分析结果
        buffett_rec = analysis_results.get("巴菲特分析师", {}).get(symbol, {}).get("recommendation", "持有")
        tech_trend = analysis_results.get("技术分析师", {}).get(symbol, {}).get("trend", "横盘")
        risk_level = risk_assessment.get(symbol, {}).get("risk_level", "中")
        max_position = risk_assessment.get(symbol, {}).get("max_position", 0.2)
        
        # 简单决策逻辑
        if buffett_rec == "买入" and tech_trend == "上涨" and risk_level != "高":
            action = "买入"
            position = max_position * 0.8
        elif buffett_rec == "卖出" or tech_trend == "下跌":
            action = "卖出"
            position = 0
        else:
            action = "持有"
            position = max_position * 0.5
        
        final_decisions[symbol] = {
            "action": action,
            "position_size": position,
            "reason": f"基于{buffett_rec}建议和{tech_trend}趋势，风险等级{risk_level}"
        }
    
    # 更新状态
    state["data"]["final_decisions"] = final_decisions
    
    # 添加最终消息
    decisions_summary = ", ".join([f"{s}:{final_decisions[s]['action']}" for s in symbols])
    message = f"投资组合管理完成，最终决策：{decisions_summary}"
    # state["messages"].append(AIMessage(content=message))
    state["messages"] = [(AIMessage(content=message))]
    
    progress.update_status(agent_name, "决策完成", f"已生成{len(symbols)}只股票的投资决策")
    return state


# 代理配置
AGENT_CONFIG = {
    "buffett_analyst": {
        "name": "巴菲特分析师",
        "agent_func": analyst_agent_a,
        "description": "价值投资导向的基本面分析"
    },
    "tech_analyst": {
        "name": "技术分析师", 
        "agent_func": analyst_agent_b,
        "description": "基于技术指标的趋势分析"
    }
} 