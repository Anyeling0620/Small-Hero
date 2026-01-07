#!/usr/bin/env python3
"""
检查最近工作流运行状态
"""
import os
import sys
import json
from github import Github

def check_workflow_status():
    """检查最近的工作流运行状态"""
    gh_token = os.getenv('GH_PAT')
    if not gh_token:
        print("❌ GH_PAT 环境变量未设置")
        sys.exit(1)
    
    try:
        g = Github(gh_token)
        repo = g.get_repo('Anyeling0620/Small-Hero')
        
        # 获取最近的工作流运行
        workflows = repo.get_workflows()
        print(f"\n📊 工作流概览：")
        print("=" * 80)
        
        for workflow in workflows:
            print(f"\n工作流: {workflow.name}")
            runs = workflow.get_runs()[:5]  # 最近5次运行
            
            for run in runs:
                status_icon = {
                    'completed': '✅' if run.conclusion == 'success' else '❌',
                    'in_progress': '⏳',
                    'queued': '⏰'
                }.get(run.status, '❓')
                
                print(f"  {status_icon} Run #{run.run_number} - {run.status}")
                print(f"     结论: {run.conclusion}")
                print(f"     触发: {run.event}")
                print(f"     时间: {run.created_at}")
                print(f"     URL: {run.html_url}")
                
                if run.conclusion == 'failure':
                    # 获取失败的作业
                    jobs = run.jobs()
                    for job in jobs:
                        if job.conclusion == 'failure':
                            print(f"\n     ❌ 失败的作业: {job.name}")
                            print(f"        步骤:")
                            for step in job.steps:
                                if step.conclusion == 'failure':
                                    print(f"          ❌ {step.name}")
                                    print(f"             {step.number}. 状态: {step.conclusion}")
                print()
        
        # 检查未解决的问题
        print("\n📋 最近的 Issues：")
        print("=" * 80)
        issues = repo.get_issues(state='open')[:10]
        for issue in issues:
            labels = [label.name for label in issue.labels]
            print(f"  #{issue.number}: {issue.title}")
            print(f"     标签: {', '.join(labels)}")
            print(f"     创建: {issue.created_at}")
            print()
    
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    check_workflow_status()
