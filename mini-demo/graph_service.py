"""
🏗️ LangGraph图服务 - 动态工作流构建引擎
🎯 负责根据用户选择动态构建AI代理协同工作流
🔄 提供同步→异步的包装机制，确保Web应用响应性
"""
import asyncio
from typing import List
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

from state import AgentState
from agents import (
    start_node, analyst_agent_a, analyst_agent_b, 
    risk_manager, portfolio_manager, AGENT_CONFIG
)


def create_graph(selected_agents: List[str]) -> StateGraph:
    """🎨 根据用户选择动态创建AI代理工作流 - 灵活的多代理协同系统"""
    # 🏗️ 创建LangGraph状态图 - 多代理协同的基础架构
    graph = StateGraph(AgentState)
    
    # 🚀 添加起始节点 - 工作流的入口点
    graph.add_node("start_node", start_node)
    
    # 📋 AI代理映射表 - 可扩展的代理注册中心
    agent_mapping = {
        "buffett_analyst": ("buffett_agent", analyst_agent_a),  # 📊 巴菲特价值投资风格
        "tech_analyst": ("tech_agent", analyst_agent_b)        # 💻 技术分析专家
    }
    
    # 🎯 动态添加用户选择的分析师代理
    added_agents = []
    for agent_name in selected_agents:
        if agent_name in agent_mapping:
            node_name, node_func = agent_mapping[agent_name]
            # 🔗 将代理函数注册为图中的节点
            graph.add_node(node_name, node_func)
            added_agents.append(node_name)
            print(f"✅ 已添加代理: {node_name}")
    
    # 🛡️ 添加必要的管理代理 - 系统核心组件
    graph.add_node("risk_manager", risk_manager)      # ⚠️ 风险管理代理
    graph.add_node("portfolio_manager", portfolio_manager)  # 💼 投资组合代理
    
    # 🔄 建立代理执行流程 - 定义工作流的执行顺序
    # 📊 采用串行流水线模式：分析师A → 分析师B → 风险管理 → 投资组合管理
    if added_agents:
        # 🚀 从起始节点到第一个分析师
        graph.add_edge("start_node", added_agents[0])
        
        # 🔗 分析师之间串行连接 - 确保分析结果能传递
        for i in range(len(added_agents) - 1):
            graph.add_edge(added_agents[i], added_agents[i + 1])
        
        # 📈 最后一个分析师到风险管理
        graph.add_edge(added_agents[-1], "risk_manager")
    else:
        # ⚠️ 如果没有选择分析师，直接进入风险管理
        print("⚠️ 未选择分析师，跳过分析阶段")
        graph.add_edge("start_node", "risk_manager")
    
    # 🔗 建立后续流程链
    graph.add_edge("risk_manager", "portfolio_manager")  # ⚠️ → 💼
    graph.add_edge("portfolio_manager", END)             # 💼 → 🏁
    graph.set_entry_point("start_node")                  # 🚀 设置入口
    
    print(f"🏗️ 工作流构建完成，包含 {len(added_agents)} 个分析师代理")
    return graph


def run_graph(graph, symbols: List[str], initial_cash: float = 100000.0):
    """⚙️ 执行LangGraph并返回结果 - 同步版本"""
    # 📦 创建初始状态 - 所有AI代理共享的数据结构
    initial_state = {
        "messages": [HumanMessage(content="请基于提供的数据做出投资决策")],  # 💬 系统指令
        "data": {
            "symbols": symbols,           # 📊 待分析股票代码
            "initial_cash": initial_cash, # 💰 初始资金
            "analysis_results": {},      # 🔍 分析师结果存储
            "risk_assessment": {},       # ⚠️ 风险评估结果
            "final_decisions": {}        # 📈 最终投资决策
        },
        "metadata": {
            "model_name": "mock-model",   # 🤖 使用的AI模型
            "show_reasoning": True        # 🧠 是否显示推理过程
        }
    }
    
    print("🚀 开始执行LangGraph工作流...")
    
    # ⚙️ 执行图 - 按定义的顺序运行所有AI代理
    result = graph.invoke(initial_state)
    
    print("✅ LangGraph执行完成")
    return result


async def run_graph_async(graph, symbols: List[str], initial_cash: float = 100000.0):
    """🔄 异步包装器 - 关键：避免阻塞Web服务器的事件循环"""
    # 🎯 核心技术：使用线程池执行器将同步代码包装为异步
    # 🔧 问题：LangGraph是同步的，但FastAPI需要异步处理
    # 💡 解决方案：在独立线程中运行同步代码，主线程保持异步响应
    
    print("🔄 准备异步执行LangGraph...")
    
    # 📡 获取当前事件循环
    loop = asyncio.get_running_loop()
    
    # 🏭 在线程池中执行同步函数，避免阻塞主事件循环
    result = await loop.run_in_executor(
        None,  # 💻 使用默认线程池
        lambda: run_graph(graph, symbols, initial_cash)  # 🔄 包装同步调用
    )
    
    print("✅ 异步执行完成")
    return result 