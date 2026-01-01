"""
架构师 - 分析项目当前进度
评估已完成的功能和下一步方向
"""
import os
import json
import subprocess
from datetime import datetime
import google.generativeai as genai

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

def get_git_stats():
    """获取 Git 统计信息"""
    print("📊 分析 Git 代码统计...")
    
    stats = {
        'total_commits': 0,
        'backend_files': 0,
        'frontend_files': 0,
        'total_lines': 0
    }
    
    try:
        # 获取提交数
        result = subprocess.run(['git', 'rev-list', '--count', 'HEAD'], 
                              capture_output=True, text=True)
        stats['total_commits'] = int(result.stdout.strip())
        
        # 统计后端文件
        result = subprocess.run(['git', 'ls-files', 'backend/**/*.java'], 
                              capture_output=True, text=True, shell=True)
        stats['backend_files'] = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        
        # 统计前端文件
        result = subprocess.run(['git', 'ls-files', 'frontend/**/*.tsx', 'frontend/**/*.ts'], 
                              capture_output=True, text=True, shell=True)
        stats['frontend_files'] = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        
    except Exception as e:
        print(f"⚠️  Git 统计失败: {e}")
    
    return stats

def read_current_config():
    """读取当前项目配置"""
    print("📖 读取项目配置...")
    
    config_path = 'ai-orchestrator/project-config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def read_latest_research():
    """读取最新的游戏研究报告"""
    print("📖 读取最新研究报告...")
    
    today = datetime.now().strftime('%Y-%m-%d')
    report_path = f'docs/game-research/daily-reports/{today}.json'
    
    if os.path.exists(report_path):
        with open(report_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def analyze_progress_with_ai(git_stats, config, research):
    """使用 AI 分析项目进度"""
    print("🤖 使用 AI 分析项目进度...")
    
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    prompt = f"""
你是小小勇者克隆项目的首席架构师。请根据以下信息分析项目当前进度：

**项目配置信息：**
{json.dumps(config, ensure_ascii=False, indent=2)}

**Git 代码统计：**
{json.dumps(git_stats, ensure_ascii=False, indent=2)}

**最新游戏研究：**
{json.dumps(research, ensure_ascii=False, indent=2)}

请完成以下分析：

1. **当前完成度评估**（0-100%）：
   - 基础架构完成度
   - 核心系统完成度
   - UI/UX 完成度
   - 游戏相似度

2. **已实现功能清单**：列出已完成的主要功能

3. **下一步优先级**：
   - 根据游戏演进优先级，确定接下来应该开发的 3-5 个功能
   - 每个功能说明原因和预计工作量

4. **技术债务**：识别当前存在的问题和需要优化的地方

5. **相似度差距分析**：对比原版游戏，列出主要差距

请以 JSON 格式输出，便于程序解析。
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ AI 分析失败: {e}")
        return None

def save_progress_report(analysis):
    """保存进度分析报告"""
    today = datetime.now().strftime('%Y-%m-%d')
    report_dir = 'docs/game-research/progress-reports'
    os.makedirs(report_dir, exist_ok=True)
    
    report_path = f"{report_dir}/{today}.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            'date': today,
            'analysis': analysis
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 进度报告已保存至: {report_path}")
    return report_path

def main():
    print("=" * 60)
    print("📈 架构师 - 项目进度分析")
    print("=" * 60)
    
    # 收集数据
    git_stats = get_git_stats()
    config = read_current_config()
    research = read_latest_research()
    
    # AI 分析
    analysis = analyze_progress_with_ai(git_stats, config, research)
    
    if analysis:
        # 保存报告
        save_progress_report(analysis)
        print("\n✨ 进度分析完成！")
    else:
        print("\n❌ 进度分析失败！")

if __name__ == '__main__':
    main()
