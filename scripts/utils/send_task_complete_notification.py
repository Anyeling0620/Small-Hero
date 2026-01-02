#!/usr/bin/env python3
"""
任务完成通知
"""
import os
import sys
import requests
from datetime import datetime

def send_task_complete_notification():
    """发送任务完成通知到微信"""
    pushplus_token = os.getenv('PUSHPLUS_TOKEN')
    issue_number = os.getenv('ISSUE_NUMBER', 'Unknown')
    pr_number = os.getenv('PR_NUMBER', 'N/A')
    
    if not pushplus_token:
        print("⚠️  PUSHPLUS_TOKEN 未配置，跳过通知")
        return
    
    try:
        title = f"✅ 任务完成 - Issue #{issue_number}"
        content = f"""
<div style="font-family: Arial, sans-serif; padding: 20px; background: #d4edda;">
    <h2 style="color: #28a745;">✅ 任务执行完成</h2>
    <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745; margin: 10px 0;">
        <h3 style="color: #28a745;">完成信息</h3>
        <p><strong>Issue:</strong> #{issue_number}</p>
        <p><strong>Pull Request:</strong> #{pr_number}</p>
        <p><strong>时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
        <h3 style="color: #6c757d;">下一步</h3>
        <ul>
            <li>✅ 代码已提交到 PR</li>
            <li>🧪 等待 QA 测试</li>
            <li>✔️ 通过后即可合并</li>
        </ul>
    </div>
    
    <div style="background: #e7f3ff; padding: 15px; border-radius: 8px; margin: 10px 0;">
        <p style="margin: 0;">
            🔗 <a href="https://github.com/Anyeling0620/Small-Hero/issues/{issue_number}">查看 Issue</a> | 
            <a href="https://github.com/Anyeling0620/Small-Hero/pull/{pr_number}">查看 PR</a>
        </p>
    </div>
</div>
"""
        
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
                print(f"✅ 完成通知已发送")
            else:
                print(f"⚠️  通知发送失败: {result.get('msg', 'Unknown error')}")
        else:
            print(f"❌ 通知发送失败: HTTP {response.status_code}")
    
    except Exception as e:
        print(f"❌ 发送通知失败: {str(e)}")

if __name__ == '__main__':
    send_task_complete_notification()
