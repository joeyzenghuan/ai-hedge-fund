"""
AI代理状态管理 - 简化版
"""
from typing import TypedDict, Annotated, Sequence, Dict, Any
from langchain_core.messages import BaseMessage
import operator


def merge_dicts(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    """合并字典，用于状态更新"""
    return {**a, **b}


class AgentState(TypedDict):
    """AI代理状态类"""
    messages: Annotated[Sequence[BaseMessage], operator.add]  # 消息链
    data: Annotated[Dict[str, Any], merge_dicts]             # 共享数据
    metadata: Annotated[Dict[str, Any], merge_dicts]         # 元数据 