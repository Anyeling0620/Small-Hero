"""
架构师 - 创建 GitHub Issues
将任务池中的任务转换为 GitHub Issues
"""
import os
import json
from datetime import datetime
from github import Github

GH_PAT = os.getenv('GH_PAT')
REPO_NAME = 'Anyeling0620/Small-Hero'

def read_task_pool():
    """读取任务池"""
    task_path = 'ai-orchestrator/task-pool.json'
    if os.path.exists(task_path):
        with open(task_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'taskPool': []}

def create_github_issues():
    """创建 GitHub Issues"""
    print("🎫 创建 GitHub Issues...")
    
    try:
        g = Github(GH_PAT)
        repo = g.get_repo(REPO_NAME)
        
        task_data = read_task_pool()
        pending_tasks = [t for t in task_data['taskPool'] if t['status'] == 'pending']
        
        created_count = 0
        for task in pending_tasks:
            # 构建 Issue 内容
            title = f"[{task['type'].upper()}] {task['title']}"
            
            body = f"""
## 任务描述
{task['description']}

## 任务信息
- **类型**: {task['type']}
- **分配给**: {task['assignedTo']}
- **优先级**: {task['priority']}
- **预计代码行数**: {task['estimatedLines']}
- **创建时间**: {task['createdAt']}

## 验收标准
"""
            
            if 'validationCriteria' in task:
                for key, value in task['validationCriteria'].items():
                    body += f"- [ ] {key}: {value}\n"
            
            # 依赖项
            if task.get('dependencies'):
                body += f"\n## 依赖任务\n"
                for dep in task['dependencies']:
                    body += f"- {dep}\n"
            
            body += f"""

---
**任务 ID**: `{task['id']}`
**由 AI 架构师自动生成**
"""
            
            # 确定标签
            labels = [task['type'], task['priority'], 'ai-generated']
            
            # 创建 Issue
            issue = repo.create_issue(
                title=title,
                body=body,
                labels=labels
            )
            
            print(f"  ✅ 创建 Issue #{issue.number}: {title}")
            
            # 更新任务状态，添加 Issue 编号
            task['status'] = 'created'
            task['github_issue'] = issue.number
            
            created_count += 1
        
        # 保存更新后的任务池
        task_path = 'ai-orchestrator/task-pool.json'
        with open(task_path, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✨ 成功创建 {created_count} 个 GitHub Issues")
        
    except Exception as e:
        print(f"❌ 创建 Issues 失败: {e}")

def main():
    print("=" * 60)
    print("🎫 架构师 - 创建 GitHub Issues")
    print("=" * 60)
    
    create_github_issues()

if __name__ == '__main__':
    main()
