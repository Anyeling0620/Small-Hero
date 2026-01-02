#!/usr/bin/env python3
"""
每日开发报告生成和发送
"""
import os
import sys
import json
import requests
from datetime import datetime, timedelta

def send_daily_report():
    """发送每日开发报告到微信"""
    pushplus_token = os.getenv('PUSHPLUS_TOKEN')
    
    if not pushplus_token:
        print("⚠️  PUSHPLUS_TOKEN 未配置，跳过每日报告")
        return
    
    try:
        # 获取今日统计数据
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 尝试读取任务池
        task_pool_path = 'ai-orchestrator/task-pool.json'
        tasks_created = 0
        tasks_completed = 0
        tasks_in_progress = 0
        
        if os.path.exists(task_pool_path):
            try:
                with open(task_pool_path, 'r', encoding='utf-8') as f:
                    task_pool = json.load(f)
                    tasks = task_pool.get('tasks', [])
                    tasks_created = len([t for t in tasks if t.get('status') == 'pending'])
                    tasks_completed = len([t for t in tasks if t.get('status') == 'completed'])
                    tasks_in_progress = len([t for t in tasks if t.get('status') == 'in-progress'])
            except Exception as e:
                print(f"⚠️  无法读取任务池: {str(e)}")
        
        # 读取项目状态
        state_path = 'ai-orchestrator/internal_state/project_memory.json'
        total_tasks = 0
        total_commits = 0
        
        if os.path.exists(state_path):
            try:
                with open(state_path, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    total_tasks = state.get('statistics', {}).get('totalTasks', 0)
                    total_commits = state.get('statistics', {}).get('totalCommits', 0)
            except Exception as e:
                print(f"⚠️  无法读取项目状态: {str(e)}")
        
        # 构建报告内容
        title = f"📊 Small Hero 每日开发报告 - {today}"
        content = f"""
<div style="font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5;">
    <h2 style="color: #2c3e50;">📊 今日开发概览</h2>
    <div style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0;">
        <h3 style="color: #3498db;">📝 任务统计</h3>
        <ul style="list-style: none; padding: 0;">
            <li>🆕 待开始: <b style="color: #e74c3c;">{tasks_created}</b> 个</li>
            <li>⏳ 进行中: <b style="color: #f39c12;">{tasks_in_progress}</b> 个</li>
            <li>✅ 已完成: <b style="color: #27ae60;">{tasks_completed}</b> 个</li>
        </ul>
    </div>
    
    <div style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0;">
        <h3 style="color: #3498db;">📈 项目进度</h3>
        <ul style="list-style: none; padding: 0;">
            <li>📚 累计任务: <b>{total_tasks}</b> 个</li>
            <li>💻 代码提交: <b>{total_commits}</b> 次</li>
        </ul>
    </div>
    
    <div style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0;">
        <h3 style="color: #3498db;">🤖 AI 团队状态</h3>
        <p>✅ 架构师: 正常运行</p>
        <p>✅ 后端开发: 待命中</p>
        <p>✅ 前端开发: 待命中</p>
        <p>✅ QA 测试: 待命中</p>
    </div>
    
    <div style="background: #ecf0f1; padding: 15px; border-radius: 8px; margin: 10px 0;">
        <p style="color: #7f8c8d; font-size: 12px; margin: 0;">
            ⏰ 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
            🔗 <a href="https://github.com/Anyeling0620/Small-Hero">查看项目详情</a>
        </p>
    </div>
</div>
"""
        
        # 发送通知
        response = requests.post(
            'http://www.pushplus.plus/send',
            json={
                'token': pushplus_token,
                'title': title,
                'content': content,
                'template': 'html'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 200:
                print(f"✅ 每日报告已发送到微信")
            else:
                print(f"⚠️  报告发送失败: {result.get('msg', 'Unknown error')}")
        else:
            print(f"❌ 报告发送失败: HTTP {response.status_code}")
    
    except requests.exceptions.Timeout:
        print("❌ 发送报告超时")
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {str(e)}")
    except Exception as e:
        print(f"❌ 生成报告失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    send_daily_report()
