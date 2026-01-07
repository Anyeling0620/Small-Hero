#!/usr/bin/env python3
"""
解析 GitHub Issue 需求
"""
import os
import sys
import json
from github import Github

def parse_issue():
    """解析 Issue 需求"""
    gh_token = os.getenv('GH_PAT')
    issue_number = os.getenv('ISSUE_NUMBER')
    
    if not gh_token:
        print("❌ GH_PAT 环境变量未设置")
        sys.exit(1)
    
    if not issue_number:
        print("❌ ISSUE_NUMBER 环境变量未设置")
        sys.exit(1)
    
    try:
        g = Github(gh_token)
        repo = g.get_repo('Anyeling0620/Small-Hero')
        issue = repo.get_issue(int(issue_number))
        
        print(f"📋 解析 Issue #{issue_number}: {issue.title}")
        print(f"描述: {issue.body}")
        
        # 提取需求信息
        requirements = {
            'issue_number': issue_number,
            'title': issue.title,
            'body': issue.body,
            'labels': [label.name for label in issue.labels],
            'created_at': str(issue.created_at)
        }
        
        # 保存到文件供后续步骤使用
        output_file = f'.github/temp/issue-{issue_number}-requirements.json'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(requirements, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 需求已解析并保存到: {output_file}")
        return 0
    
    except Exception as e:
        print(f"❌ 解析 Issue 失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(parse_issue())
