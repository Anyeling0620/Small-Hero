#!/usr/bin/env python3
"""
任务失败通知
"""
import os
import sys
import requests
from datetime import datetime

def send_task_failed_notification():
    """发送任务失败通知到微信"""
    pushplus_token = os.getenv('PUSHPLUS_TOKEN')
    issue_number = os.getenv('ISSUE_NUMBER', 'Unknown')
    error_message = os.getenv('ERROR_MESSAGE', '任务执行失败')
    
    if not pushplus_token:
        print("⚠️  PUSHPLUS_TOKEN 未配置，跳过通知")
        return
    
    try:
        title = f"❌ 任务失败 - Issue #{issue_number}"
        content = f"""
<div style="font-family: Arial, sans-serif; padding: 20px; background: #fff3cd;">
    <h2 style="color: #dc3545;">❌ 任务执行失败</h2>
    <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #dc3545; margin: 10px 0;">
        <h3 style="color: #dc3545;">失败信息</h3>
        <p><strong>Issue:</strong> #{issue_number}</p>
        <p><strong>时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>错误:</strong> {error_message}</p>
    </div>
    
    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
        <h3 style="color: #6c757d;">下一步操作</h3>
        <ul>
            <li>系统将自动重试</li>
            <li>如果持续失败，请检查日志</li>
            <li>可能需要手动介入</li>
        </ul>
    </div>
    
    <div style="background: #e7f3ff; padding: 15px; border-radius: 8px; margin: 10px 0;">
        <p style="margin: 0;">
            🔗 <a href="https://github.com/Anyeling0620/Small-Hero/issues/{issue_number}">查看 Issue</a> | 
            <a href="https://github.com/Anyeling0620/Small-Hero/actions">查看 Actions</a>
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
                print(f"✅ 失败通知已发送")
            else:
                print(f"⚠️  通知发送失败: {result.get('msg', 'Unknown error')}")
        else:
            print(f"❌ 通知发送失败: HTTP {response.status_code}")
    
    except Exception as e:
        print(f"❌ 发送通知失败: {str(e)}")

if __name__ == '__main__':
    send_task_failed_notification()
