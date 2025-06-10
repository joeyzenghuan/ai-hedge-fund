#!/usr/bin/env python3
"""
API测试脚本 - 测试Web服务器接口
"""
import requests
import json
import time


def test_api_endpoints():
    """测试API端点"""
    base_url = "http://localhost:8000"
    
    print("🧪 开始测试API端点...")
    print("=" * 50)
    
    # 测试根路径
    print("📍 测试根路径 (/)")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print(f"✅ 根路径测试成功: {response.json()}")
        else:
            print(f"❌ 根路径测试失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False
    
    # 测试代理列表
    print("\n🤖 测试代理列表 (/agents)")
    try:
        response = requests.get(f"{base_url}/agents")
        if response.status_code == 200:
            agents = response.json()
            print(f"✅ 代理列表获取成功:")
            for agent in agents.get("agents", []):
                print(f"   - {agent['name']}: {agent['description']}")
        else:
            print(f"❌ 代理列表测试失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取代理列表失败: {e}")
    
    # 测试健康检查
    print("\n💚 测试健康检查 (/health)")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print(f"✅ 健康检查成功: {response.json()}")
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 基础API测试完成!")
    print("💡 提示: 可以在浏览器中打开 http://localhost:8000/docs 查看API文档")
    print("🌐 可以打开 frontend.html 文件使用Web界面")
    
    return True


if __name__ == "__main__":
    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    time.sleep(3)
    
    test_api_endpoints() 