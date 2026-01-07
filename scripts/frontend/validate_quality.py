#!/usr/bin/env python3
"""
验证代码质量
"""
import os
import sys
import glob

def validate_quality():
    """验证代码质量"""
    issue_number = os.getenv('ISSUE_NUMBER', 'unknown')
    
    print(f"🔍 验证 Issue #{issue_number} 的代码质量")
    
    # 检查生成的文件
    generated_dir = f'frontend/src/generated/issue-{issue_number}'
    
    if not os.path.exists(generated_dir):
        print(f"⚠️  生成目录不存在: {generated_dir}")
        print("跳过质量验证")
        return 0
    
    # 统计代码行数
    total_lines = 0
    files = glob.glob(f'{generated_dir}/**/*.{tsx,ts,jsx,js}', recursive=True)
    
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                lines = len([line for line in f.readlines() if line.strip()])
                total_lines += lines
                print(f"  {file}: {lines} 行")
        except Exception as e:
            print(f"  ⚠️  无法读取 {file}: {e}")
    
    print(f"\n📊 总代码行数: {total_lines}")
    
    # 检查是否满足最小行数要求
    min_lines = 200
    if total_lines < min_lines:
        print(f"❌ 代码行数不足 {min_lines} 行")
        return 1
    
    print(f"✅ 代码质量验证通过")
    return 0

if __name__ == '__main__':
    sys.exit(validate_quality())
