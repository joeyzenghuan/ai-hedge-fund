"""
数据模型和事件类 - 简化版
"""
from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import datetime


# 请求模型
class InvestmentRequest(BaseModel):
    """投资分析请求模型"""
    symbols: List[str]                    # 股票代码列表
    selected_agents: List[str]            # 选择的AI代理
    initial_cash: float = 100000.0        # 初始资金


# 事件模型
class BaseEvent(BaseModel):
    """所有Server-Sent Event事件的基类"""
    type: str
    
    def to_sse(self) -> str:
        """转换为Server-Sent Event格式"""
        event_type = self.type.lower()
        return f"event: {event_type}\ndata: {self.model_dump_json()}\n\n"


class StartEvent(BaseEvent):
    """开始事件"""
    type: Literal["start"] = "start"
    message: str = "分析开始"


class ProgressUpdateEvent(BaseEvent):
    """进度更新事件"""
    type: Literal["progress"] = "progress"
    agent: str
    status: str
    timestamp: Optional[str] = None
    analysis: Optional[str] = None


class ErrorEvent(BaseEvent):
    """错误事件"""
    type: Literal["error"] = "error"
    message: str
    details: Optional[str] = None


class CompleteEvent(BaseEvent):
    """完成事件"""
    type: Literal["complete"] = "complete"
    message: str = "分析完成"
    data: dict


# 响应模型
class InvestmentDecision(BaseModel):
    """投资决策模型"""
    symbol: str
    action: str  # 买入、卖出、持有
    position_size: float
    reason: str


class AnalysisResult(BaseModel):
    """分析结果模型"""
    decisions: List[InvestmentDecision]
    analysis_summary: dict
    risk_assessment: dict 