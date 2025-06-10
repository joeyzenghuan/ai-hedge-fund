"""
📊 数据模型和事件类 - Server-Sent Events与API通信规范
🎯 定义前后端通信的所有数据结构和事件格式
🌐 支持实时Web通信的核心组件
"""
from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import datetime


# 📨 API请求模型
class InvestmentRequest(BaseModel):
    """ 投资分析请求模型 - 前端发送的分析参数"""
    symbols: List[str]                    # 📈 股票代码列表，如 ["AAPL", "MSFT"]
    selected_agents: List[str]            # 🤖 选择的AI代理，如 ["buffett_analyst", "tech_analyst"]
    initial_cash: float = 100000.0        # 💰 初始资金，默认10万美元


# 🌐 Server-Sent Events 事件模型系统
class BaseEvent(BaseModel):
    """📡 所有Server-Sent Event事件的基类 - 统一的事件格式化接口"""
    type: str
    
    def to_sse(self) -> str:
        """🔄 转换为Server-Sent Event格式 - 符合W3C SSE标准"""
        # 📝 SSE协议格式：event: 事件类型\ndata: JSON数据\n\n
        # 🌍 这是Web标准格式，浏览器EventSource API可以直接解析
        event_type = self.type.lower()
        return f"event: {event_type}\ndata: {self.model_dump_json()}\n\n"


class StartEvent(BaseEvent):
    """🚀 开始事件 - 通知前端分析工作流开始执行"""
    type: Literal["start"] = "start"
    message: str = "分析开始"  # 📢 向用户显示的消息


class ProgressUpdateEvent(BaseEvent):
    """📊 进度更新事件 - 实时推送AI代理工作状态（观察者模式的产物）"""
    type: Literal["progress"] = "progress"
    agent: str                        # 🤖 当前工作的AI代理名称
    status: str                       # 📍 代理当前状态描述
    timestamp: Optional[str] = None   # ⏰ 状态更新时间戳
    analysis: Optional[str] = None    # 🔍 代理产生的分析内容（可选）


class ErrorEvent(BaseEvent):
    """❌ 错误事件 - 推送系统异常信息给前端用户"""
    type: Literal["error"] = "error"
    message: str                      # ⚠️ 用户友好的错误描述
    details: Optional[str] = None     # 🔍 技术细节（开发调试用）


class CompleteEvent(BaseEvent):
    """🎯 完成事件 - 推送最终分析结果和投资建议"""
    type: Literal["complete"] = "complete"
    message: str = "分析完成"         # 📢 完成提示消息
    data: dict                        # 📊 完整的分析结果数据包


# 📊 业务响应模型
class InvestmentDecision(BaseModel):
    """💰 投资决策模型 - AI代理产生的具体投资建议"""
    symbol: str          # 📈 股票代码，如 "AAPL"
    action: str          # 🎯 投资操作：'buy', 'sell', 'hold'
    position_size: float # 📏 建议仓位大小（股数或资金比例）
    reason: str          # 🧠 AI决策的详细理由


class AnalysisResult(BaseModel):
    """📋 完整分析结果模型 - 包含所有AI代理的输出汇总"""
    decisions: List[InvestmentDecision]  # 📈 投资决策列表
    analysis_summary: dict               # 📊 分析摘要
    risk_assessment: dict                # ⚠️ 风险评估结果 