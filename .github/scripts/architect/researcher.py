import sys
from duckduckgo_search import DDGS
import json

def deep_research_game_mechanic(topic):
    """
    无需 API Key 的联网搜索函数，专门抓取《小小勇者》的精细数据
    """
    results = []
    with DDGS() as ddgs:
        # 针对性搜索攻略、数值公式、玩法介绍
        query = f"小小勇者 {topic} 详细数值公式 玩法机制"
        print(f"🔍 正在互联网搜索: {query}...")
        ddgs_gen = ddgs.text(query, region='cn-zh', safesearch='off', timelimit='y')
        for i, r in enumerate(ddgs_gen):
            if i >= 5: break  # 获取前5条高质量结果
            results.append({
                "title": r['title'],
                "body": r['body'],
                "href": r['href']
            })
    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        topic = sys.argv[1]
        data = deep_research_game_mechanic(topic)
        print(json.dumps(data, ensure_ascii=False, indent=2))