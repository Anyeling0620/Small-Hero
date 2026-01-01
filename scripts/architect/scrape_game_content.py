"""
架构师 - 游戏内容爬取脚本
每日自动爬取小小勇者相关的游戏资讯、更新日志、玩家反馈等
"""
import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import google.generativeai as genai

# 配置 Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

def scrape_taptap():
    """爬取 TapTap 小小勇者页面"""
    print("🔍 正在爬取 TapTap 游戏信息...")
    
    url = "https://www.taptap.cn/app/233851"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 提取游戏信息
        game_info = {
            'source': 'TapTap',
            'url': url,
            'scraped_at': datetime.now().isoformat(),
            'description': soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else '',
            'raw_html': str(soup)[:5000]  # 保存部分 HTML 供 AI 分析
        }
        
        return game_info
    except Exception as e:
        print(f"❌ TapTap 爬取失败: {e}")
        return None

def scrape_reddit():
    """爬取 Reddit 相关讨论"""
    print("🔍 正在爬取 Reddit 社区讨论...")
    
    url = "https://www.reddit.com/r/TinyRogues/top.json?limit=10"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        posts = []
        for post in data['data']['children']:
            post_data = post['data']
            posts.append({
                'title': post_data.get('title', ''),
                'content': post_data.get('selftext', ''),
                'score': post_data.get('score', 0),
                'url': f"https://www.reddit.com{post_data.get('permalink', '')}"
            })
        
        return {
            'source': 'Reddit',
            'scraped_at': datetime.now().isoformat(),
            'posts': posts
        }
    except Exception as e:
        print(f"❌ Reddit 爬取失败: {e}")
        return None

def analyze_with_gemini(scraped_data):
    """使用 Gemini AI 分析爬取的内容"""
    print("🤖 使用 Gemini AI 分析游戏内容...")
    
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    prompt = f"""
你是一位资深游戏架构师，专门负责分析小小勇者（Tiny Hero）游戏的核心机制。

请分析以下爬取的游戏信息：

{json.dumps(scraped_data, ensure_ascii=False, indent=2)}

请提取以下关键信息：
1. **核心玩法机制**：战斗系统、升级系统、装备系统等
2. **数值系统**：属性计算公式、成长曲线
3. **UI/UX 特点**：界面风格、交互设计
4. **最新更新内容**：新增功能、改动点
5. **玩家反馈重点**：玩家最关注的功能和问题

以 JSON 格式输出，包含以上 5 个关键点。
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Gemini 分析失败: {e}")
        return None

def save_report(data):
    """保存每日研究报告"""
    today = datetime.now().strftime('%Y-%m-%d')
    report_dir = 'docs/game-research/daily-reports'
    os.makedirs(report_dir, exist_ok=True)
    
    report_path = f"{report_dir}/{today}.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 研究报告已保存至: {report_path}")

def main():
    print("=" * 60)
    print("🏗️  架构师 - 每日游戏内容爬取")
    print("=" * 60)
    
    # 爬取各个来源
    scraped_data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'sources': []
    }
    
    # TapTap
    taptap_data = scrape_taptap()
    if taptap_data:
        scraped_data['sources'].append(taptap_data)
    
    # Reddit
    reddit_data = scrape_reddit()
    if reddit_data:
        scraped_data['sources'].append(reddit_data)
    
    # AI 分析
    analysis = analyze_with_gemini(scraped_data)
    if analysis:
        scraped_data['ai_analysis'] = analysis
    
    # 保存报告
    save_report(scraped_data)
    
    print("\n✨ 每日爬取任务完成！")

if __name__ == '__main__':
    main()
