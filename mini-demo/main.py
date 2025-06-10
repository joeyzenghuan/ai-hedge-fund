"""
FastAPI主应用 - 简化版AI投资分析系统
"""
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from models import (
    InvestmentRequest, StartEvent, ProgressUpdateEvent, 
    ErrorEvent, CompleteEvent, InvestmentDecision
)
from graph_service import create_graph, run_graph_async
from progress import progress


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    print("🚀 AI投资分析系统启动中...")
    yield
    # 关闭时
    print("🛑 AI投资分析系统关闭")


# 创建FastAPI应用
app = FastAPI(
    title="AI投资分析系统 - Mini Demo",
    description="基于LangGraph的多AI代理投资决策系统",
    version="1.0.0",
    lifespan=lifespan
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI投资分析系统 Mini Demo",
        "version": "1.0.0",
        "available_agents": ["buffett_analyst", "tech_analyst"],
        "docs": "/docs"
    }


@app.get("/agents")
async def get_available_agents():
    """获取可用的AI代理列表"""
    return {
        "agents": [
            {
                "id": "buffett_analyst",
                "name": "巴菲特分析师",
                "description": "价值投资导向的基本面分析"
            },
            {
                "id": "tech_analyst", 
                "name": "技术分析师",
                "description": "基于技术指标的趋势分析"
            }
        ]
    }


@app.post("/analyze")
async def analyze_investments(request: InvestmentRequest):
    """🚀 运行投资分析 - Server-Sent Events流式响应"""
    
    async def event_generator():
        """ 生成Server-Sent Events流 - 系统核心引擎"""
        # 1️⃣ 创建异步队列 - 用于AI代理和Web前端间的通信桥梁
        progress_queue = asyncio.Queue()
        
        # 2️⃣ 定义进度处理器（回调函数）- 观察者模式的核心
        def progress_handler(agent_name, status, analysis, timestamp):
            """🔔 进度回调处理器 - 将AI代理的状态更新转换为SSE事件"""
            #  创建进度更新事件
            event = ProgressUpdateEvent(
                agent=agent_name, 
                status=status, 
                timestamp=timestamp, 
                analysis=analysis
            )
            # 非阻塞方式放入队列 - 不会阻塞AI代理执行
            progress_queue.put_nowait(event)
        
        # 3️⃣ 注册处理器到全局进度跟踪器 - 建立观察者关系
        progress.register_handler(progress_handler)
        
        try:
            # 4️⃣ 创建和编译AI代理工作流图 - 动态构建多AI代理协同系统
            graph = create_graph(request.selected_agents)  
            compiled_graph = graph.compile() 
            
            # 5️⃣ 启动后台任务执行LangGraph - 在独立线程中运行避免阻塞
            run_task = asyncio.create_task(
                run_graph_async(  # 🔄 异步包装器：同步→异步
                    compiled_graph, 
                    request.symbols, 
                    request.initial_cash
                )
            )
            
            # 6️⃣ 发送开始事件 - 通知前端分析开始
            yield StartEvent(message=f"开始分析 {', '.join(request.symbols)}").to_sse()
            
            # 7️⃣ 核心事件循环 - 实时监听AI代理进度并推送给前端
            while not run_task.done():  # 持续检查后台任务状态
                try:
                    # 等待队列中的新事件（超时1秒保持连接活跃）
                    event = await asyncio.wait_for(progress_queue.get(), timeout=1.0)
                    # 立即推送SSE事件给前端
                    yield event.to_sse()
                except asyncio.TimeoutError:
                    # 超时继续循环，保持SSE连接活跃
                    continue
                except Exception as e:
                    # 处理队列操作异常
                    yield ErrorEvent(message="进度更新错误", details=str(e)).to_sse()
            
            # 8️⃣ 获取最终结果并发送完成事件
            try:
                # 🏁 等待后台任务完成并获取结果
                result = await run_task
                
                # 📊 解析AI代理的最终投资决策
                final_decisions = result.get("data", {}).get("final_decisions", {})
                decisions = [
                    InvestmentDecision(
                        symbol=symbol,
                        action=decision["action"],
                        position_size=decision["position_size"],
                        reason=decision["reason"]
                    ).model_dump()
                    for symbol, decision in final_decisions.items()
                ]
                
                # 发送完成事件 - 包含所有分析结果
                final_data = CompleteEvent(
                    message="投资分析完成",
                    data={
                        "decisions": decisions,  # 📈 最终投资决策
                        "analysis_results": result.get("data", {}).get("analysis_results", {}),  # 🔍 分析师结果
                        "risk_assessment": result.get("data", {}).get("risk_assessment", {}),  # ⚠️ 风险评估
                        "messages": [msg.content for msg in result.get("messages", []) if hasattr(msg, 'content')]  # 📝 执行日志
                    }
                )
                yield final_data.to_sse()
                
            except Exception as e:
                yield ErrorEvent(message="分析执行错误", details=str(e)).to_sse()
            
        except Exception as e:
            yield ErrorEvent(message="系统错误", details=str(e)).to_sse()
        finally:
            # 9️⃣ 清理资源 - 确保不会内存泄漏
            progress.unregister_handler(progress_handler)  # 注销观察者
            yield "event: end\ndata: {}\n\n"  # 🔚 发送结束信号关闭SSE连接
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 