#!/usr/bin/env python3
"""
启动脚本 - 支持多种运行模式
"""
import sys
import subprocess
import webbrowser
import time


def print_banner():
    """打印启动横幅"""
    print("🤖" + "=" * 60 + "🤖")
    print("🚀  AI投资分析系统 - Mini Demo")
    print("🏗️  基于 FastAPI + LangGraph 的多AI代理系统")
    print("=" * 64)
    print()


def run_cli_test():
    """运行命令行测试"""
    print("📋 模式: 命令行测试")
    print("🔄 正在执行测试...")
    print("-" * 40)
    
    try:
        subprocess.run([sys.executable, "test_cli.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 测试失败: {e}")
        return False
    except FileNotFoundError:
        print("❌ 找不到 test_cli.py 文件")
        return False
    
    print("-" * 40)
    print("✅ 命令行测试完成!")
    return True


def run_web_server():
    """运行Web服务器"""
    print("📋 模式: Web服务器")
    print("🌐 启动 FastAPI 服务器...")
    print("📍 服务地址: http://localhost:8000")
    print("📖 API文档: http://localhost:8000/docs")
    print()
    print("💡 提示: 可以用浏览器打开 frontend.html 使用Web界面")
    print("🔧 按 Ctrl+C 停止服务")
    print("-" * 40)
    
    try:
        # 询问是否自动打开浏览器
        response = input("🌐 是否自动打开API文档? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            # 延迟打开浏览器
            def open_browser():
                time.sleep(2)  # 等待服务器启动
                webbrowser.open("http://localhost:8000/docs")
            
            import threading
            threading.Thread(target=open_browser, daemon=True).start()
        
        # 启动服务器
        subprocess.run([sys.executable, "main.py"], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 服务器启动失败: {e}")
        return False
    except FileNotFoundError:
        print("❌ 找不到 main.py 文件")
        return False


def check_dependencies():
    """检查依赖是否安装"""
    print("🔍 检查依赖...")
    
    required_packages = [
        "fastapi", "uvicorn", "pydantic", 
        "langgraph", "langchain", "langchain-openai"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ 缺少以下依赖包:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print()
        print("📦 请运行以下命令安装依赖:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖已安装")
    return True


def show_menu():
    """显示运行模式菜单"""
    print("🎯 请选择运行模式:")
    print("   1. 命令行测试 (快速验证功能)")
    print("   2. Web服务器 (完整体验)")
    print("   3. 检查依赖")
    print("   4. 退出")
    print()
    
    while True:
        choice = input("👉 请输入选择 (1-4): ").strip()
        
        if choice == "1":
            print()
            return run_cli_test()
        elif choice == "2":
            print()
            return run_web_server()
        elif choice == "3":
            print()
            return check_dependencies()
        elif choice == "4":
            print("👋 再见!")
            return True
        else:
            print("❌ 无效选择，请输入 1-4")


def main():
    """主函数"""
    print_banner()
    
    # 先检查依赖
    if not check_dependencies():
        print()
        sys.exit(1)
    
    print()
    
    # 显示菜单并执行
    if len(sys.argv) > 1:
        # 命令行参数模式
        mode = sys.argv[1].lower()
        if mode in ["cli", "test"]:
            run_cli_test()
        elif mode in ["web", "server"]:
            run_web_server()
        elif mode in ["check", "deps"]:
            check_dependencies()
        else:
            print(f"❌ 未知模式: {mode}")
            print("💡 可用模式: cli, web, check")
    else:
        # 交互式菜单模式
        show_menu()


if __name__ == "__main__":
    main() 