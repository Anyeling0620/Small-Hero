#!/usr/bin/env python3
"""
使用 AI 生成后端代码
"""
import os
import sys
import json

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from scripts.utils.ai_helper import create_ai_helper

def generate_backend_code():
    """生成后端代码"""
    issue_number = os.getenv('ISSUE_NUMBER')
    
    if not issue_number:
        print("❌ ISSUE_NUMBER 环境变量未设置")
        return 1
    
    try:
        print(f"💻 为 Issue #{issue_number} 生成后端代码")
        
        # 读取需求
        requirements_file = f'.github/temp/issue-{issue_number}-requirements.json'
        if not os.path.exists(requirements_file):
            print(f"⚠️  需求文件不存在，使用默认需求")
            requirements = {
                'issue_number': issue_number,
                'title': f'Backend task for issue #{issue_number}',
                'body': 'Implement backend feature as described.'
            }
        else:
            with open(requirements_file, 'r', encoding='utf-8') as f:
                requirements = json.load(f)
        
        # 构建提示
        prompt = f"""
你是一个资深的 Java/Spring Boot 后端开发工程师，正在开发一个类似"小小勇者"的游戏后端。

任务需求：
标题: {requirements.get('title', 'Unknown')}
描述: {requirements.get('body', 'No description')}

技术栈：
- Spring Boot 3.x
- Java 17+
- Spring Data JPA
- MySQL/TiDB
- Redis (缓存)
- WebSocket (实时通信)

请生成完整的后端代码，包括：
1. Entity 实体类
2. Repository 接口
3. Service 业务逻辑
4. Controller REST API
5. DTO 数据传输对象
6. 单元测试

要求：
- 遵循 Spring Boot 最佳实践
- 使用 RESTful API 设计
- 添加适当的注释和文档
- 编写单元测试
- 代码至少 200 行
- 更新 OpenAPI 文档

请直接输出可运行的 Java 代码。
"""
        
        # 使用 AI 生成代码
        ai_helper = create_ai_helper('backendDev')
        response = ai_helper.generate_content(prompt)
        
        if not response:
            print("❌ AI 生成失败")
            return 1
        
        print("✅ 后端代码生成成功")
        print(f"生成内容长度: {len(response)} 字符")
        
        # 保存生成的代码
        output_dir = f'backend/src/main/generated/issue-{issue_number}'
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = f'{output_dir}/generated-code.java'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response)
        
        print(f"✅ 代码已保存到: {output_file}")
        
        # TODO: 解析 AI 响应，按照 Java 包结构保存文件
        
        return 0
    
    except Exception as e:
        print(f"❌ 生成后端代码失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(generate_backend_code())
