"""
并发锁管理工具
防止多个任务同时执行，确保串行处理
"""
import os
import json
import time
from datetime import datetime, timedelta
from typing import Optional, Dict
from pathlib import Path

class ConcurrencyLock:
    """并发锁类"""
    
    def __init__(self, lock_file: str = ".github/.task-lock.json", timeout: int = 3600000):
        """
        初始化并发锁
        
        Args:
            lock_file: 锁文件路径
            timeout: 锁超时时间（毫秒）
        """
        self.lock_file = lock_file
        self.timeout = timeout / 1000  # 转换为秒
        self._ensure_lock_file()
    
    def _ensure_lock_file(self):
        """确保锁文件存在"""
        lock_dir = os.path.dirname(self.lock_file)
        if lock_dir and not os.path.exists(lock_dir):
            os.makedirs(lock_dir, exist_ok=True)
        
        if not os.path.exists(self.lock_file):
            self._write_lock_data({
                'locked': False,
                'taskId': None,
                'lockedAt': None,
                'lockedBy': None
            })
    
    def _read_lock_data(self) -> Dict:
        """读取锁数据"""
        try:
            with open(self.lock_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  读取锁文件失败: {e}")
            return {
                'locked': False,
                'taskId': None,
                'lockedAt': None,
                'lockedBy': None
            }
    
    def _write_lock_data(self, data: Dict):
        """写入锁数据"""
        try:
            with open(self.lock_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ 写入锁文件失败: {e}")
    
    def is_locked(self) -> bool:
        """检查是否被锁定"""
        lock_data = self._read_lock_data()
        
        if not lock_data.get('locked'):
            return False
        
        # 检查是否超时
        locked_at_str = lock_data.get('lockedAt')
        if locked_at_str:
            try:
                locked_at = datetime.fromisoformat(locked_at_str)
                if datetime.now() > locked_at + timedelta(seconds=self.timeout):
                    print(f"⚠️  锁已超时，自动释放")
                    self.release()
                    return False
            except Exception:
                pass
        
        return True
    
    def acquire(self, task_id: str, locked_by: str, max_wait: int = 300) -> bool:
        """
        获取锁
        
        Args:
            task_id: 任务ID
            locked_by: 锁持有者（如 architect, backend-dev 等）
            max_wait: 最大等待时间（秒），0 表示不等待
            
        Returns:
            bool: 是否成功获取锁
        """
        start_time = time.time()
        
        while True:
            if not self.is_locked():
                # 锁可用，尝试获取
                lock_data = {
                    'locked': True,
                    'taskId': task_id,
                    'lockedAt': datetime.now().isoformat(),
                    'lockedBy': locked_by
                }
                self._write_lock_data(lock_data)
                print(f"🔒 成功获取锁: {task_id} (by {locked_by})")
                return True
            
            # 锁被占用
            lock_data = self._read_lock_data()
            current_task = lock_data.get('taskId', 'Unknown')
            current_owner = lock_data.get('lockedBy', 'Unknown')
            
            elapsed = time.time() - start_time
            
            if max_wait == 0:
                print(f"❌ 锁被占用: {current_task} (by {current_owner})，不等待")
                return False
            
            if elapsed >= max_wait:
                print(f"❌ 等待锁超时: {current_task} (by {current_owner})")
                return False
            
            print(f"⏳ 锁被占用: {current_task} (by {current_owner})，等待中... ({int(elapsed)}s/{max_wait}s)")
            time.sleep(10)  # 每10秒检查一次
    
    def release(self, task_id: str = None):
        """
        释放锁
        
        Args:
            task_id: 任务ID（可选，用于验证）
        """
        lock_data = self._read_lock_data()
        
        if task_id and lock_data.get('taskId') != task_id:
            print(f"⚠️  尝试释放不属于自己的锁: {task_id} != {lock_data.get('taskId')}")
            return
        
        self._write_lock_data({
            'locked': False,
            'taskId': None,
            'lockedAt': None,
            'lockedBy': None
        })
        print(f"🔓 锁已释放: {task_id or 'Unknown'}")
    
    def get_lock_info(self) -> Dict:
        """获取锁信息"""
        return self._read_lock_data()


def with_lock(task_id: str, locked_by: str, max_wait: int = 300):
    """
    装饰器：自动管理锁
    
    Args:
        task_id: 任务ID
        locked_by: 锁持有者
        max_wait: 最大等待时间（秒）
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            lock = ConcurrencyLock()
            
            # 获取锁
            if not lock.acquire(task_id, locked_by, max_wait):
                print(f"❌ 无法获取锁，任务取消: {task_id}")
                return None
            
            try:
                # 执行任务
                result = func(*args, **kwargs)
                return result
            finally:
                # 释放锁
                lock.release(task_id)
        
        return wrapper
    return decorator


if __name__ == '__main__':
    # 测试并发锁
    lock = ConcurrencyLock()
    
    print("\n=== 测试 1: 获取和释放锁 ===")
    if lock.acquire('TEST-001', 'test-user', max_wait=0):
        print("✅ 成功获取锁")
        time.sleep(2)
        lock.release('TEST-001')
        print("✅ 成功释放锁")
    
    print("\n=== 测试 2: 锁被占用 ===")
    lock.acquire('TEST-002', 'user-1', max_wait=0)
    
    if not lock.acquire('TEST-003', 'user-2', max_wait=0):
        print("✅ 正确阻止了第二个任务")
    
    lock.release('TEST-002')
    
    print("\n=== 测试 3: 锁信息 ===")
    lock.acquire('TEST-004', 'user-3', max_wait=0)
    info = lock.get_lock_info()
    print(f"锁信息: {json.dumps(info, indent=2, ensure_ascii=False)}")
    lock.release('TEST-004')
