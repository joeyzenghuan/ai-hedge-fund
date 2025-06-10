"""
LangGraph图服务 - 简化版
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
    """根据用户选择动态创建AI代理工作流"""
    graph = StateGraph(AgentState)
    
    # 添加起始节点
    graph.add_node("start_node", start_node)
    
    # 动态添加选择的分析师代理
    agent_mapping = {
        "buffett_analyst": ("buffett_agent", analyst_agent_a),
        "tech_analyst": ("tech_agent", analyst_agent_b)
    }
    
    added_agents = []
    for agent_name in selected_agents:
        if agent_name in agent_mapping:
            node_name, node_func = agent_mapping[agent_name]
            graph.add_node(node_name, node_func)
            added_agents.append(node_name)
    
    # 添加风险管理和投资组合管理
    graph.add_node("risk_manager", risk_manager)
    graph.add_node("portfolio_manager", portfolio_manager)
    
    # 简化的串行执行流程
    if added_agents:
        # 从start_node到第一个分析师
        graph.add_edge("start_node", added_agents[0])
        
        # 分析师之间串行连接
        for i in range(len(added_agents) - 1):
            graph.add_edge(added_agents[i], added_agents[i + 1])
        
        # 最后一个分析师到风险管理
        graph.add_edge(added_agents[-1], "risk_manager")
    else:
        # 如果没有选择分析师，直接进入风险管理
        graph.add_edge("start_node", "risk_manager")
    
    # 风险管理到投资组合管理
    graph.add_edge("risk_manager", "portfolio_manager")
    graph.add_edge("portfolio_manager", END)
    graph.set_entry_point("start_node")
    
    return graph


def run_graph(graph, symbols: List[str], initial_cash: float = 100000.0):
    """执行图并返回结果"""
    # 创建初始状态
    initial_state = {
        "messages": [HumanMessage(content="请基于提供的数据做出投资决策")],
        "data": {
            "symbols": symbols,
            "initial_cash": initial_cash,
            "analysis_results": {},
            "risk_assessment": {},
            "final_decisions": {}
        },
        "metadata": {
            "model_name": "mock-model",
            "show_reasoning": True
        }
    }
    
    # 执行图
    result = graph.invoke(initial_state)
    return result


async def run_graph_async(graph, symbols: List[str], initial_cash: float = 100000.0):
    """异步包装器，避免阻塞事件循环"""
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        None, 
        lambda: run_graph(graph, symbols, initial_cash)
    )
    return result 