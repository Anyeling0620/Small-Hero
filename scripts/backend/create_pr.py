#!/usr/bin/env python3
"""
创建后端 Pull Request
"""
import os
import sys
from github import Github

def create_pr():
    """创建 Pull Request"""
    gh_token = os.getenv('GH_PAT')
    issue_number = os.getenv('ISSUE_NUMBER')
    
    if not gh_token:
        print("❌ GH_PAT 环境变量未设置")
        return 1
    
    if not issue_number:
        print("❌ ISSUE_NUMBER 环境变量未设置")
        return 1
    
    try:
        g = Github(gh_token)
        repo = g.get_repo('Anyeling0620/Small-Hero')
        issue = repo.get_issue(int(issue_number))
        
        branch_name = f"feature/backend-issue-{issue_number}"
        
        print(f"🔄 为后端 Issue #{issue_number} 创建 PR")
        
        pr_title = f"[Backend] {issue.title}"
        pr_body = f"""
## 相关 Issue
Closes #{issue_number}

## 变更说明
自动生成的后端代码，实现了 Issue 中描述的功能。

## 技术栈
- Spring Boot 3.x
- Java 17+
- Spring Data JPA
- TiDB Cloud

## 检查清单
- [x] 代码已生成
- [x] 通过代码质量检查
- [ ] 等待 QA 测试
- [ ] API 文档已更新

## AI 生成
本 PR 由 AI 后端开发工程师自动生成。
"""
        
        try:
            pr = repo.create_pull(
                title=pr_title,
                body=pr_body,
                head=branch_name,
                base='main'
            )
            
            print(f"✅ PR 创建成功: {pr.html_url}")
            print(f"PR 编号: #{pr.number}")
            
            os.environ['PR_NUMBER'] = str(pr.number)
            
            issue.create_comment(f"✅ PR #{pr.number} 已创建: {pr.html_url}")
            
            return 0
        
        except Exception as e:
            if 'already exists' in str(e).lower() or 'no commits' in str(e).lower():
                print(f"⚠️  PR 可能已存在或没有新的提交: {e}")
                return 0
            raise
    
    except Exception as e:
        print(f"❌ 创建 PR 失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(create_pr())
