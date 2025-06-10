"""
进度跟踪系统 - 简化版
"""
from typing import Dict, List, Callable
from datetime import datetime, timezone


class AgentProgress:
    """管理多个代理的进度跟踪"""
    
    def __init__(self):
        self.agent_status: Dict[str, Dict[str, str]] = {}
        self.update_handlers: List[Callable] = []  # 事件处理器列表
    
    def register_handler(self, handler: Callable):
        """注册进度更新处理器"""
        self.update_handlers.append(handler)
    
    def unregister_handler(self, handler: Callable):
        """注销进度更新处理器"""
        if handler in self.update_handlers:
            self.update_handlers.remove(handler)
    
    def update_status(self, agent_name: str, status: str, analysis: str = None):
        """更新代理状态并通知所有处理器"""
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # 更新内部状态
        if agent_name not in self.agent_status:
            self.agent_status[agent_name] = {}
        
        self.agent_status[agent_name].update({
            "status": status,
            "analysis": analysis,
            "timestamp": timestamp
        })
        
        # 通知所有注册的处理器
        for handler in self.update_handlers:
            try:
                handler(agent_name, status, analysis, timestamp)
            except Exception as e:
                print(f"Error in progress handler: {e}")
    
    def get_status(self, agent_name: str = None):
        """获取代理状态"""
        if agent_name:
            return self.agent_status.get(agent_name, {})
        return self.agent_status


# 全局进度跟踪实例
progress = AgentProgress() 