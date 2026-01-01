"""
PushPlus 通知工具
用于发送任务完成、错误等通知到微信
"""
import os
import json
import requests
from datetime import datetime
from typing import Dict, Optional

PUSHPLUS_TOKEN = os.getenv('PUSHPLUS_TOKEN')
PUSHPLUS_URL = "http://www.pushplus.plus/send"

class PushPlusNotifier:
    """PushPlus 通知类"""
    
    def __init__(self, token: str = None):
        self.token = token or PUSHPLUS_TOKEN
        
    def send_notification(
        self, 
        title: str, 
        content: str, 
        template: str = "html",
        channel: str = "wechat"
    ) -> bool:
        """
        发送通知
        
        Args:
            title: 通知标题
            content: 通知内容（支持HTML）
            template: 模板类型（html/txt/json/markdown）
            channel: 发送渠道（wechat/mail/sms）
        
        Returns:
            bool: 发送是否成功
        """
        if not self.token:
            print("⚠️  PushPlus Token 未配置，跳过通知发送")
            return False
        
        try:
            payload = {
                "token": self.token,
                "title": title,
                "content": content,
                "template": template,
                "channel": channel
            }
            
            response = requests.post(PUSHPLUS_URL, json=payload, timeout=10)
            result = response.json()
            
            if result.get('code') == 200:
                print(f"✅ PushPlus 通知发送成功: {title}")
                return True
            else:
                print(f"❌ PushPlus 通知发送失败: {result.get('msg')}")
                return False
                
        except Exception as e:
            print(f"❌ PushPlus 通知发送异常: {e}")
            return False
    
    def send_task_created(self, task: Dict) -> bool:
        """发送任务创建通知"""
        title = f"🎯 新任务创建: {task.get('title', 'Unknown')}"
        
        content = f"""
        <h2>📋 新任务已创建</h2>
        <hr>
        <p><strong>任务ID:</strong> {task.get('id', 'N/A')}</p>
        <p><strong>标题:</strong> {task.get('title', 'N/A')}</p>
        <p><strong>类型:</strong> <span style="color: #1E90FF;">{task.get('type', 'N/A')}</span></p>
        <p><strong>分配给:</strong> {task.get('assignedTo', 'N/A')}</p>
        <p><strong>优先级:</strong> <span style="color: #FF6347;">{task.get('priority', 'N/A')}</span></p>
        <p><strong>预计代码行数:</strong> {task.get('estimatedLines', 0)} 行</p>
        <p><strong>创建时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <hr>
        <p><strong>描述:</strong></p>
        <p>{task.get('description', 'N/A')}</p>
        """
        
        return self.send_notification(title, content)
    
    def send_task_completed(self, task: Dict, details: Dict) -> bool:
        """发送任务完成通知"""
        title = f"✅ 任务完成: {task.get('title', 'Unknown')}"
        
        # 计算代码统计
        code_stats = details.get('codeStats', {})
        files_changed = code_stats.get('filesChanged', 0)
        lines_added = code_stats.get('linesAdded', 0)
        lines_deleted = code_stats.get('linesDeleted', 0)
        
        # 质量评分
        quality_score = details.get('qualityScore', 'N/A')
        test_coverage = details.get('testCoverage', 'N/A')
        
        content = f"""
        <h2>✨ 任务已完成</h2>
        <hr>
        <p><strong>任务ID:</strong> {task.get('id', 'N/A')}</p>
        <p><strong>标题:</strong> {task.get('title', 'N/A')}</p>
        <p><strong>类型:</strong> <span style="color: #1E90FF;">{task.get('type', 'N/A')}</span></p>
        <p><strong>完成时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h3>📊 代码统计</h3>
        <ul>
            <li>修改文件: <strong>{files_changed}</strong> 个</li>
            <li>新增代码: <strong style="color: #28a745;">+{lines_added}</strong> 行</li>
            <li>删除代码: <strong style="color: #dc3545;">-{lines_deleted}</strong> 行</li>
            <li>净增代码: <strong>{lines_added - lines_deleted}</strong> 行</li>
        </ul>
        
        <h3>🎯 质量指标</h3>
        <ul>
            <li>代码质量评分: <strong>{quality_score}</strong></li>
            <li>测试覆盖率: <strong>{test_coverage}</strong></li>
        </ul>
        
        <h3>🔗 相关链接</h3>
        <p>Pull Request: <a href="{details.get('prUrl', '#')}">{details.get('prNumber', 'N/A')}</a></p>
        """
        
        return self.send_notification(title, content)
    
    def send_task_failed(self, task: Dict, error: str) -> bool:
        """发送任务失败通知"""
        title = f"❌ 任务失败: {task.get('title', 'Unknown')}"
        
        content = f"""
        <h2 style="color: #dc3545;">⚠️ 任务执行失败</h2>
        <hr>
        <p><strong>任务ID:</strong> {task.get('id', 'N/A')}</p>
        <p><strong>标题:</strong> {task.get('title', 'N/A')}</p>
        <p><strong>类型:</strong> {task.get('type', 'N/A')}</p>
        <p><strong>失败时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h3>🔍 错误信息</h3>
        <pre style="background: #f6f8fa; padding: 10px; border-radius: 5px;">{error}</pre>
        
        <p><em>系统将在 5 秒后自动重试...</em></p>
        """
        
        return self.send_notification(title, content)
    
    def send_pr_created(self, pr_info: Dict) -> bool:
        """发送 PR 创建通知"""
        title = f"🔄 PR 已创建: {pr_info.get('title', 'Unknown')}"
        
        content = f"""
        <h2>📝 Pull Request 已创建</h2>
        <hr>
        <p><strong>PR 编号:</strong> #{pr_info.get('number', 'N/A')}</p>
        <p><strong>标题:</strong> {pr_info.get('title', 'N/A')}</p>
        <p><strong>分支:</strong> {pr_info.get('branch', 'N/A')} → main</p>
        <p><strong>创建时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h3>📊 变更统计</h3>
        <ul>
            <li>修改文件: <strong>{pr_info.get('filesChanged', 0)}</strong> 个</li>
            <li>新增代码: <strong style="color: #28a745;">+{pr_info.get('additions', 0)}</strong> 行</li>
            <li>删除代码: <strong style="color: #dc3545;">-{pr_info.get('deletions', 0)}</strong> 行</li>
        </ul>
        
        <h3>🔗 查看详情</h3>
        <p><a href="{pr_info.get('url', '#')}">点击查看 Pull Request</a></p>
        """
        
        return self.send_notification(title, content)
    
    def send_test_result(self, test_result: Dict) -> bool:
        """发送测试结果通知"""
        passed = test_result.get('passed', False)
        title = f"{'✅ 测试通过' if passed else '❌ 测试失败'}: {test_result.get('name', 'Unknown')}"
        
        total_tests = test_result.get('totalTests', 0)
        passed_tests = test_result.get('passedTests', 0)
        failed_tests = test_result.get('failedTests', 0)
        
        content = f"""
        <h2>🧪 测试结果</h2>
        <hr>
        <p><strong>测试名称:</strong> {test_result.get('name', 'N/A')}</p>
        <p><strong>测试时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h3>📊 测试统计</h3>
        <ul>
            <li>总测试数: <strong>{total_tests}</strong></li>
            <li>通过: <strong style="color: #28a745;">{passed_tests}</strong></li>
            <li>失败: <strong style="color: #dc3545;">{failed_tests}</strong></li>
            <li>通过率: <strong>{(passed_tests/total_tests*100) if total_tests > 0 else 0:.1f}%</strong></li>
        </ul>
        
        <h3>🎯 覆盖率</h3>
        <p>代码覆盖率: <strong>{test_result.get('coverage', 'N/A')}</strong></p>
        """
        
        if not passed and test_result.get('errors'):
            content += f"""
            <h3 style="color: #dc3545;">❌ 失败详情</h3>
            <pre style="background: #f6f8fa; padding: 10px; border-radius: 5px;">{test_result.get('errors', 'N/A')}</pre>
            """
        
        return self.send_notification(title, content)
    
    def send_daily_report(self, report: Dict) -> bool:
        """发送每日报告通知"""
        title = f"📊 每日开发报告 - {datetime.now().strftime('%Y-%m-%d')}"
        
        content = f"""
        <h2>📈 Small Hero 每日开发报告</h2>
        <hr>
        <p><strong>报告日期:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
        
        <h3>📋 任务概况</h3>
        <ul>
            <li>新建任务: <strong>{report.get('tasksCreated', 0)}</strong></li>
            <li>完成任务: <strong style="color: #28a745;">{report.get('tasksCompleted', 0)}</strong></li>
            <li>进行中: <strong style="color: #ffc107;">{report.get('tasksInProgress', 0)}</strong></li>
            <li>失败任务: <strong style="color: #dc3545;">{report.get('tasksFailed', 0)}</strong></li>
        </ul>
        
        <h3>💻 代码统计</h3>
        <ul>
            <li>新增代码: <strong style="color: #28a745;">+{report.get('linesAdded', 0)}</strong> 行</li>
            <li>提交次数: <strong>{report.get('commits', 0)}</strong></li>
            <li>PR 数量: <strong>{report.get('prs', 0)}</strong></li>
        </ul>
        
        <h3>🎮 游戏进度</h3>
        <ul>
            <li>完成度: <strong>{report.get('completionPercentage', 0)}%</strong></li>
            <li>相似度: <strong>{report.get('similarityScore', 0)}%</strong></li>
            <li>当前阶段: <strong>{report.get('currentPhase', 'N/A')}</strong></li>
        </ul>
        
        <h3>📚 游戏研究</h3>
        <p>{report.get('gameResearch', '今日未爬取游戏资讯')}</p>
        """
        
        return self.send_notification(title, content)


# 便捷函数
def notify_task_created(task: Dict) -> bool:
    """快捷发送任务创建通知"""
    notifier = PushPlusNotifier()
    return notifier.send_task_created(task)


def notify_task_completed(task: Dict, details: Dict) -> bool:
    """快捷发送任务完成通知"""
    notifier = PushPlusNotifier()
    return notifier.send_task_completed(task, details)


def notify_task_failed(task: Dict, error: str) -> bool:
    """快捷发送任务失败通知"""
    notifier = PushPlusNotifier()
    return notifier.send_task_failed(task, error)


def notify_pr_created(pr_info: Dict) -> bool:
    """快捷发送 PR 创建通知"""
    notifier = PushPlusNotifier()
    return notifier.send_pr_created(pr_info)


def notify_test_result(test_result: Dict) -> bool:
    """快捷发送测试结果通知"""
    notifier = PushPlusNotifier()
    return notifier.send_test_result(test_result)


def notify_daily_report(report: Dict) -> bool:
    """快捷发送每日报告通知"""
    notifier = PushPlusNotifier()
    return notifier.send_daily_report(report)


if __name__ == '__main__':
    # 测试通知
    test_task = {
        'id': 'TEST-001',
        'title': '测试任务',
        'type': 'backend',
        'assignedTo': 'backend-dev',
        'priority': 'high',
        'estimatedLines': 250,
        'description': '这是一个测试任务'
    }
    
    notifier = PushPlusNotifier()
    notifier.send_task_created(test_task)
