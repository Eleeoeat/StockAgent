#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
一键启动脚本 - 双击运行应用
"""

import subprocess
import sys
import os

def main():
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, "app_v2_enhanced.py")
    
    # 检查应用文件是否存在
    if not os.path.exists(app_path):
        print("❌ 错误：找不到 app_v2_enhanced.py")
        print(f"期望路径：{app_path}")
        input("按任意键退出...")
        sys.exit(1)
    
    print("🚀 启动 AI 价值投资分析助手...")
    print(f"📁 应用路径：{app_path}")
    print(f"🐍 Python 环境：{sys.executable}")
    
    try:
        # 启动 Streamlit 应用
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", app_path],
            cwd=script_dir
        )
    except FileNotFoundError:
        print("❌ 错误：找不到 streamlit，请先运行:")
        print("   pip install streamlit akshare openai pandas numpy")
        input("按任意键退出...")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 启动失败：{str(e)}")
        input("按任意键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()
