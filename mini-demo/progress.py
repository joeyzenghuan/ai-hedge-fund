"""
🎯 进度跟踪系统 - 观察者模式实现
📡 用于实现AI代理和Web前端间的实时通信
"""
from typing import Dict, List, Callable
from datetime import datetime, timezone


class AgentProgress:
    """ 管理多个AI代理的进度跟踪 - 观察者模式核心类"""
    
    def __init__(self):
        # 存储所有AI代理的状态信息
        self.agent_status: Dict[str, Dict[str, str]] = {}
        # 观察者回调函数列表 - 用于通知状态变化
        self.update_handlers: List[Callable] = []  # 事件处理器列表
    
    def register_handler(self, handler: Callable):
        """📝 注册进度更新处理器 - 建立观察者订阅关系"""
        self.update_handlers.append(handler)
        print(f" 已注册处理器，当前共 {len(self.update_handlers)} 个观察者")
    
    def unregister_handler(self, handler: Callable):
        """ 注销进度更新处理器 - 解除订阅，防止内存泄漏 """
        if handler in self.update_handlers:
            self.update_handlers.remove(handler)
            print(f"已注销处理器，当前剩余 {len(self.update_handlers)} 个观察者")
    
    def update_status(self, agent_name: str, status: str, analysis: str = None):
        """🚨 更新代理状态并通知所有处理器 - 观察者模式的核心触发器"""
        # 生成UTC时间戳
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # 💾 更新内部状态存储
        if agent_name not in self.agent_status:
            self.agent_status[agent_name] = {}
        
        self.agent_status[agent_name].update({
            "status": status,      # 📊 当前状态
            "analysis": analysis,  # 🔍 分析结果
            "timestamp": timestamp # ⏰ 更新时间
        })
        
        print(f"{agent_name}: {status}")
        
        # 📢 广播通知 - 遍历所有观察者并触发回调
        for handler in self.update_handlers:
            try:
                # 异步调用回调函数，传递最新状态
                handler(agent_name, status, analysis, timestamp)
            except Exception as e:
                # 异常隔离 - 一个观察者出错不影响其他观察者
                print(f"Handler error: {e}")
    
    def get_status(self, agent_name: str = None):
        """获取代理状态 - 查询接口"""
        if agent_name:
            return self.agent_status.get(agent_name, {})
        return self.agent_status


# 🌍 全局进度跟踪实例 - 单例模式，所有AI代理共享
progress = AgentProgress() 