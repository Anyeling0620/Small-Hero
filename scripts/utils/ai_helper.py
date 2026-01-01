"""
AI 模型辅助工具
支持 Gemini 和 DeepSeek 自动切换，带重试机制
"""
import os
import time
import json
from typing import Optional, Dict, Any
import google.generativeai as genai

# 配置 API 密钥
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

class AIModelHelper:
    """AI 模型辅助类，支持主备切换和重试"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化 AI 模型辅助类
        
        Args:
            config: 模型配置，包含 primary 和 fallback
        """
        self.config = config
        self.primary_model = config.get('primary', {})
        self.fallback_model = config.get('fallback', {})
        self.retry_attempts = config.get('retryAttempts', 3)
        self.retry_delay = config.get('retryDelay', 5000) / 1000  # 转换为秒
        
        # 配置 Gemini
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
    
    def generate_content(self, prompt: str) -> Optional[str]:
        """
        生成内容，自动重试和备用模型切换
        
        Args:
            prompt: 提示词
            
        Returns:
            生成的内容，失败返回 None
        """
        # 首先尝试主模型
        result = self._try_model(self.primary_model, prompt, "主模型")
        if result:
            return result
        
        # 主模型失败，尝试备用模型
        print(f"⚠️  主模型失败，切换到备用模型...")
        result = self._try_model(self.fallback_model, prompt, "备用模型")
        if result:
            return result
        
        print(f"❌ 所有模型均失败！")
        return None
    
    def _try_model(self, model_config: Dict, prompt: str, model_name: str) -> Optional[str]:
        """
        尝试使用指定模型生成内容，带重试机制
        
        Args:
            model_config: 模型配置
            prompt: 提示词
            model_name: 模型名称（用于日志）
            
        Returns:
            生成的内容，失败返回 None
        """
        model_type = model_config.get('model', '')
        
        for attempt in range(1, self.retry_attempts + 1):
            try:
                print(f"🤖 尝试使用 {model_name} ({model_type})，第 {attempt}/{self.retry_attempts} 次...")
                
                # Gemini 模型
                if 'gemini' in model_type.lower():
                    result = self._call_gemini(model_config, prompt)
                    if result:
                        print(f"✅ {model_name} 成功生成内容")
                        return result
                
                # DeepSeek 模型
                elif 'deepseek' in model_type.lower():
                    result = self._call_deepseek(model_config, prompt)
                    if result:
                        print(f"✅ {model_name} 成功生成内容")
                        return result
                
                else:
                    print(f"❌ 不支持的模型类型: {model_type}")
                    return None
                    
            except Exception as e:
                print(f"❌ {model_name} 第 {attempt} 次尝试失败: {e}")
                
                if attempt < self.retry_attempts:
                    print(f"⏳ 等待 {self.retry_delay} 秒后重试...")
                    time.sleep(self.retry_delay)
        
        return None
    
    def _call_gemini(self, config: Dict, prompt: str) -> Optional[str]:
        """调用 Gemini API"""
        model_name = config.get('model', 'gemini-2.5-flash-latest')
        temperature = config.get('temperature', 0.7)
        max_tokens = config.get('maxTokens', 8000)
        
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
        )
        
        response = model.generate_content(prompt)
        return response.text
    
    def _call_deepseek(self, config: Dict, prompt: str) -> Optional[str]:
        """调用 DeepSeek API"""
        import requests
        
        model_name = config.get('model', 'deepseek-chat')
        base_url = config.get('baseUrl', 'https://api.deepseek.com/v1')
        temperature = config.get('temperature', 0.7)
        max_tokens = config.get('maxTokens', 8000)
        
        if not DEEPSEEK_API_KEY:
            raise Exception("DEEPSEEK_API_KEY 未配置")
        
        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': model_name,
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        response.raise_for_status()
        result = response.json()
        
        return result['choices'][0]['message']['content']


def create_ai_helper(role: str) -> AIModelHelper:
    """
    根据角色创建 AI 辅助类
    
    Args:
        role: 角色名称 (architect/backendDev/frontendDev/qaTester)
        
    Returns:
        AIModelHelper 实例
    """
    # 读取配置
    config_path = 'ai-orchestrator/project-config.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        project_config = json.load(f)
    
    ai_config = project_config.get('aiModelConfig', {}).get(role, {})
    
    return AIModelHelper(ai_config)


if __name__ == '__main__':
    # 测试
    helper = create_ai_helper('architect')
    
    test_prompt = "请简单介绍一下小小勇者这款游戏。"
    result = helper.generate_content(test_prompt)
    
    if result:
        print("\n生成结果:")
        print(result)
    else:
        print("\n生成失败！")
