#!/usr/bin/env python3
"""
测试结果通知
"""
import os
import sys
import requests
from datetime import datetime

def send_test_result_notification():
    """发送测试结果通知到微信"""
    pushplus_token = os.getenv('PUSHPLUS_TOKEN')
    pr_number = os.getenv('PR_NUMBER', 'Unknown')
    test_passed = os.getenv('TEST_PASSED', 'false') == 'true'
    coverage = os.getenv('TEST_COVERAGE', 'N/A')
    
    if not pushplus_token:
        print("⚠️  PUSHPLUS_TOKEN 未配置，跳过通知")
        return
    
    try:
        status_icon = "✅" if test_passed else "❌"
        status_text = "通过" if test_passed else "失败"
        status_color = "#28a745" if test_passed else "#dc3545"
        bg_color = "#d4edda" if test_passed else "#f8d7da"
        
        title = f"{status_icon} 测试{status_text} - PR #{pr_number}"
        content = f"""
<div style="font-family: Arial, sans-serif; padding: 20px; background: {bg_color};">
    <h2 style="color: {status_color};">{status_icon} 测试{status_text}</h2>
    <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid {status_color}; margin: 10px 0;">
        <h3 style="color: {status_color};">测试结果</h3>
        <p><strong>Pull Request:</strong> #{pr_number}</p>
        <p><strong>状态:</strong> {status_text}</p>
        <p><strong>覆盖率:</strong> {coverage}</p>
        <p><strong>时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
        <h3 style="color: #6c757d;">详情</h3>
        <p>完整的测试报告已发布在 PR 评论中</p>
    </div>
    
    <div style="background: #e7f3ff; padding: 15px; border-radius: 8px; margin: 10px 0;">
        <p style="margin: 0;">
            🔗 <a href="https://github.com/Anyeling0620/Small-Hero/pull/{pr_number}">查看 PR</a> | 
            <a href="https://github.com/Anyeling0620/Small-Hero/actions">查看详细日志</a>
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
                print(f"✅ 测试结果通知已发送")
            else:
                print(f"⚠️  通知发送失败: {result.get('msg', 'Unknown error')}")
        else:
            print(f"❌ 通知发送失败: HTTP {response.status_code}")
    
    except Exception as e:
        print(f"❌ 发送通知失败: {str(e)}")

if __name__ == '__main__':
    send_test_result_notification()
