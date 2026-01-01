"""
架构师 - 生成每日开发任务
根据进度分析和游戏研究生成具体的开发任务
"""
import os
import json
from datetime import datetime
import google.generativeai as genai

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

def read_progress_report():
    """读取今日的进度报告"""
    today = datetime.now().strftime('%Y-%m-%d')
    report_path = f'docs/game-research/progress-reports/{today}.json'
    
    if os.path.exists(report_path):
        with open(report_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def read_project_config():
    """读取项目配置"""
    config_path = 'ai-orchestrator/project-config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def read_current_tasks():
    """读取当前任务池"""
    task_path = 'ai-orchestrator/task-pool.json'
    if os.path.exists(task_path):
        with open(task_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'taskPool': [], 'completedTasks': []}

def generate_tasks_with_ai(progress_report, config, current_tasks):
    """使用 AI 生成今日任务"""
    print("🤖 生成今日开发任务...")
    
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    prompt = f"""
你是小小勇者克隆项目的首席架构师。根据以下信息生成今日的开发任务：

**项目配置：**
{json.dumps(config, ensure_ascii=False, indent=2)}

**进度分析：**
{json.dumps(progress_report, ensure_ascii=False, indent=2)}

**当前任务池：**
{json.dumps(current_tasks, ensure_ascii=False, indent=2)}

**任务生成规则（必须严格遵守）：**
1. 每个任务必须预计新增至少 200 行有效代码
2. 后端任务分配给 GitHub Copilot（backend-dev）
3. 前端任务分配给 Gemini（frontend-dev）
4. 测试任务分配给 QA（qa-tester）
5. 后端任务必须包含单元测试
6. 修改数据模型必须同时更新 OpenAPI 规范
7. 前端任务必须创建实际的素材资源，不能使用简单的 emoji 或文字

**请生成 3-5 个高优先级任务**，包含：
- id: 唯一标识符（格式：YYYYMMDD-001）
- title: 任务标题（简洁明确）
- description: 详细描述（包括具体要实现的功能、技术要求、验收标准）
- type: backend/frontend/qa
- assignedTo: backend-dev/frontend-dev/qa-tester
- priority: high/medium/low
- estimatedLines: 预计代码行数（至少 200）
- dependencies: 依赖的其他任务 ID
- validationCriteria: 验收标准

以 JSON 数组格式输出任务列表。确保任务具体、可执行、符合硬性规定。
"""
    
    try:
        response = model.generate_content(prompt)
        # 尝试从响应中提取 JSON
        text = response.text
        # 移除可能的 markdown 代码块标记
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0]
        elif '```' in text:
            text = text.split('```')[1].split('```')[0]
        
        tasks = json.loads(text.strip())
        return tasks
    except Exception as e:
        print(f"❌ 任务生成失败: {e}")
        return []

def update_task_pool(new_tasks):
    """更新任务池"""
    task_path = 'ai-orchestrator/task-pool.json'
    current_data = read_current_tasks()
    
    # 添加新任务到任务池
    for task in new_tasks:
        task['status'] = 'pending'
        task['createdAt'] = datetime.now().isoformat()
        current_data['taskPool'].append(task)
    
    # 保存更新后的任务池
    with open(task_path, 'w', encoding='utf-8') as f:
        json.dump(current_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已添加 {len(new_tasks)} 个任务到任务池")

def save_task_summary():
    """保存任务摘要"""
    today = datetime.now().strftime('%Y-%m-%d')
    task_data = read_current_tasks()
    
    summary_dir = 'docs/game-research/task-summaries'
    os.makedirs(summary_dir, exist_ok=True)
    
    summary_path = f"{summary_dir}/{today}.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump({
            'date': today,
            'pending_tasks': len([t for t in task_data['taskPool'] if t['status'] == 'pending']),
            'in_progress_tasks': len([t for t in task_data['taskPool'] if t['status'] == 'in-progress']),
            'completed_tasks': len(task_data['completedTasks']),
            'tasks': task_data['taskPool']
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 任务摘要已保存至: {summary_path}")

def main():
    print("=" * 60)
    print("📝 架构师 - 生成今日开发任务")
    print("=" * 60)
    
    # 读取必要数据
    progress_report = read_progress_report()
    config = read_project_config()
    current_tasks = read_current_tasks()
    
    # 生成新任务
    new_tasks = generate_tasks_with_ai(progress_report, config, current_tasks)
    
    if new_tasks:
        # 更新任务池
        update_task_pool(new_tasks)
        
        # 保存任务摘要
        save_task_summary()
        
        print(f"\n✨ 今日任务生成完成！共生成 {len(new_tasks)} 个任务")
        
        # 打印任务概览
        print("\n📋 今日任务概览：")
        for task in new_tasks:
            print(f"  • [{task['type']}] {task['title']} (预计 {task['estimatedLines']} 行)")
    else:
        print("\n❌ 任务生成失败！")

if __name__ == '__main__':
    main()
