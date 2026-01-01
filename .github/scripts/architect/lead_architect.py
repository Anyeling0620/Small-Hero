import os
import json
import subprocess
import google.generativeai as genai
from pathlib import Path

# 初始化 Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro')

def get_repo_structure():
    """扫描项目全貌，包括文件内容，以便 AI 理解当前进度"""
    structure = {}
    exclude = {'.git', 'node_modules', 'target', '.github', 'ai-orchestrator/internal_state'}
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in exclude]
        relative_path = os.path.relpath(root, ".")
        structure[relative_path] = files
    return structure

def run_research(topic):
    """调用 researcher.py 获取实时数据"""
    result = subprocess.run(
        ["python", ".github/scripts/architect/researcher.py", topic],
        capture_ascii=True, text=True, encoding='utf-8'
    )
    return result.stdout

def lead_architect_evolution():
    print("🚀 架构师开始自主演进审计...")
    
    # 1. 感知当前状态
    repo_map = get_repo_structure()
    
    # 2. 架构师决定今天要攻克的方向（基于《小小勇者》核心玩法路线）
    # 架构师会根据已有的文件判断，如果没后端就先做后端，没数值就先做数值
    strategic_prompt = f"""
    你是《Small Hero》项目的自主架构师。
    
    当前代码仓库结构: {json.dumps(repo_map)}
    
    你的职责：
    1. 对比《小小勇者》原版游戏（包含战斗、数值、精灵、佣兵、以太、雕像等系统）。
    2. 确定当前项目最缺失的“核心功能块”。
    3. 给出今天必须完成的深度研发任务。
    
    硬性要求：
    - 任务必须是全栈式的（涵盖数据库、后端、前端、跨端适配）。
    - 禁止提交碎片的、无意义的修改。
    - 必须指定至少 5 个以上需要新建或修改的文件。
    - 如果需要新的 GitHub Action 工作流，请在任务中明确指出。

    请输出 JSON 格式的任务定义。
    """
    
    response = model.generate_content(strategic_prompt)
    decision = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
    
    # 3. 针对决策方向进行联网深度搜索
    topic = decision.get("target_module", "游戏核心逻辑")
    web_data = run_research(topic)
    
    # 4. 融合搜索结果，生成“不可偷工减料”的详细任务
    final_task_prompt = f"""
    基于搜索到的真实游戏数据: {web_data}
    
    请细化以下任务目标: {json.dumps(decision)}
    
    输出最终的 task-pool.json 内容。
    要求任务描述极其详尽，包含必须实现的类名、函数名、数据库表字段定义。
    确保执行 AI (Copilot/Gemini) 没有任何偷懒的空间。
    """
    
    final_response = model.generate_content(final_task_prompt)
    final_tasks = json.loads(final_response.text.strip().replace('```json', '').replace('```', ''))
    
    # 5. 写入任务池
    with open("ai-orchestrator/task-pool.json", "w", encoding='utf-8') as f:
        json.dump(final_tasks, f, ensure_ascii=False, indent=2)
    
    print(f"🎯 架构师已完成深度调研并下发任务：{topic}")

if __name__ == "__main__":
    lead_architect_evolution()