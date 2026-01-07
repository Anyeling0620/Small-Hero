#!/usr/bin/env python3
"""
使用 AI 生成前端代码
"""
import os
import sys
import json

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from scripts.utils.ai_helper import AIModelHelper

def generate_frontend_code():
    """生成前端代码"""
    issue_number = os.getenv('ISSUE_NUMBER')
    
    if not issue_number:
        print("❌ ISSUE_NUMBER 环境变量未设置")
        return 1
    
    try:
        print(f"🎨 为 Issue #{issue_number} 生成前端代码")
        
        # 读取需求文件
        requirements_file = f'.github/temp/issue-{issue_number}-requirements.json'
        if not os.path.exists(requirements_file):
            print(f"⚠️  需求文件不存在: {requirements_file}")
            print("尝试继续生成...")
            requirements = {
                'issue_number': issue_number,
                'title': f'Frontend task for issue #{issue_number}',
                'body': 'Implement frontend feature as described in the issue.'
            }
        else:
            with open(requirements_file, 'r', encoding='utf-8') as f:
                requirements = json.load(f)
        
        # 构建提示
        prompt = f"""
你是一个资深的前端开发工程师，正在开发一个类似"小小勇者"的游戏前端。

任务需求：
标题: {requirements.get('title', 'Unknown')}
描述: {requirements.get('body', 'No description')}

技术栈：
- React 18+
- TypeScript
- TailwindCSS
- Zustand (状态管理)
- React Query (数据获取)

请生成完整的 React 组件代码，包括：
1. 组件文件 (.tsx)
2. 类型定义 (.ts)
3. 样式文件 (如果需要)
4. 基本的单元测试

要求：
- 代码规范，使用 TypeScript
- 遵循 React 最佳实践
- 使用函数组件和 Hooks
- 添加适当的注释
- 代码至少 200 行

请直接输出可运行的代码。
"""
        
        # 使用 AI 生成代码
        from scripts.utils.ai_helper import create_ai_helper
        ai_helper = create_ai_helper('frontendDev')
        response = ai_helper.generate_content(prompt)
        
        if not response:
            print("❌ AI 生成失败")
            return 1
        
        print("✅ 前端代码生成成功")
        print(f"生成内容长度: {len(response)} 字符")
        
        # 保存生成的代码
        output_dir = f'frontend/src/generated/issue-{issue_number}'
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = f'{output_dir}/generated-code.tsx'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response)
        
        print(f"✅ 代码已保存到: {output_file}")
        
        # TODO: 解析 AI 响应，提取不同的文件并保存到合适的位置
        
        return 0
    
    except Exception as e:
        print(f"❌ 生成前端代码失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(generate_frontend_code())
