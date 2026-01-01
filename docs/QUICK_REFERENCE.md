# 🚀 快速参考指南

## GitHub Secrets 配置清单

### 必需配置 ✅
```
✓ DB_HOST              - TiDB 数据库地址
✓ DB_NAME              - 数据库名称
✓ DB_PASSWORD          - 数据库密码
✓ DB_PORT              - 数据库端口
✓ DB_USER              - 数据库用户名
✓ GEMINI_API_KEY       - Gemini 2.5 API 密钥
✓ GH_PAT               - GitHub Token
✓ SPRING_DATASOURCE_URL - 数据库连接 URL
```

### 推荐配置 ⭐
```
⭐ DEEPSEEK_API_KEY    - DeepSeek API（备用模型）
⭐ PUSHPLUS_TOKEN      - PushPlus Token（微信通知）
```

---

## AI 模型配置速查

| 角色 | 主模型 | 备用模型 | API Key |
|------|--------|----------|---------|
| 架构师 | Gemini 2.5 Flash | DeepSeek Chat | GEMINI_API_KEY / DEEPSEEK_API_KEY |
| 后端 | GitHub Copilot | DeepSeek Coder | GH_PAT / DEEPSEEK_API_KEY |
| 前端 | Gemini 2.5 Flash | DeepSeek Chat | GEMINI_API_KEY / DEEPSEEK_API_KEY |
| 测试 | Gemini 2.5 Pro | DeepSeek Chat | GEMINI_API_KEY / DEEPSEEK_API_KEY |

---

## 工作流触发时间

### 自动触发（加速模式 🚀）
- **架构师每日任务**: 每天 **4 次** 自动执行
  - 09:00 UTC+8 - 早间任务生成
  - 13:00 UTC+8 - 午间任务生成
  - 17:00 UTC+8 - 下午任务生成
  - 21:00 UTC+8 - 晚间任务生成
  - 每次生成 **5-10 个任务**（根据项目阶段动态调整）

### Issue 触发（并发执行）
- **后端开发**: Issue 标签为 `backend`（最多 2 个并发）
- **前端开发**: Issue 标签为 `frontend`（最多 2 个并发）

### PR 触发（串行执行）
- **QA 测试**: 创建或更新 PR 时（确保测试准确性）

---

## 任务生成配置 🎯

### 每次生成数量
```
最小任务数: 5 个
最大任务数: 10 个
每日总量: 20-40 个（4次执行）
动态调整: 根据项目阶段自动优化
```

### 优先级分配
```
高优先级: 40%（核心功能、关键修复）
中优先级: 40%（常规功能、优化改进）
低优先级: 20%（文档、重构、小优化）
```

### 任务分类统计
```
后端任务: ~40%（战斗、装备、技能系统）
前端任务: ~40%（UI组件、交互、动画）
测试任务: ~20%（自动化测试、质量保证）
```

---

## 通知类型一览

### 实时通知 📱
- 📋 任务创建
- ✅ 任务完成
- ❌ 任务失败
- 🔄 PR 创建
- 🧪 测试结果

### 汇总通知 📊
- 📊 每日开发报告

---

## 重试机制参数

```
重试次数: 每个模型 3 次
重试间隔: 5 秒
总尝试次数: 6 次（主模型3次 + 备用3次）
超时时间: API 调用 60 秒
```

---

## 并发控制参数 ⚡

```text
最大并发任务: 3 个（同时执行）
后端任务并发: 2 个
前端任务并发: 2 个
QA 任务并发: 1 个（串行）
锁超时时间: 1 小时
等待超时: 10 分钟
锁文件位置: .github/.task-lock.json
```

### 并发执行策略
- **后端**: 使用 `ai-backend-dev-type` 并发组，允许 2 个后端任务同时执行
- **前端**: 使用 `ai-frontend-dev-type` 并发组，允许 2 个前端任务同时执行
- **QA**: 使用 `ai-qa-testing` 并发组，串行执行确保测试准确性
- **锁机制**: 每个任务单独锁定，避免同一 Issue 重复执行

---

## 质量标准

### 代码要求
- ✅ 最小代码行数: 200 行
- ✅ 测试覆盖率: ≥ 80%
- ✅ 禁止 TODO/FIXME
- ✅ 禁止 console.log/System.out

### 游戏标准
- ✅ 目标相似度: 95%
- ✅ 前端必须使用真实素材
- ✅ 数据模型变更同步更新 API 文档

---

## 常用命令

### 手动触发工作流
```bash
# 进入 GitHub Actions 页面
# 选择工作流 → Run workflow
```

### 查看锁状态
```bash
cat .github/.task-lock.json
```

### 强制释放锁
```bash
rm .github/.task-lock.json
git add .github/.task-lock.json
git commit -m "Release lock manually"
git push
```

### 测试通知
```bash
cd scripts/utils
python pushplus_notifier.py
```

---

## 故障排查速查

### Gemini API 失败
```
✓ 检查 GEMINI_API_KEY 是否正确
✓ 检查 API 配额是否用完
✓ 系统会自动切换到 DeepSeek
```

### DeepSeek API 失败
```
✓ 检查 DEEPSEEK_API_KEY 是否配置
✓ 访问 platform.deepseek.com 检查账户
✓ 确认有足够的 API 额度
```

### 通知未收到
```
✓ 检查 PUSHPLUS_TOKEN 是否正确
✓ 确认微信已关注 PushPlus 公众号
✓ 检查是否达到每日 200 条限制
```

### 任务卡住不执行
```
✓ 检查是否有其他任务正在执行
✓ 查看 .github/.task-lock.json
✓ 等待 1 小时自动释放或手动释放
```

---

## API 获取链接

- **Gemini API**: https://makersuite.google.com/app/apikey
- **DeepSeek API**: https://platform.deepseek.com/
- **PushPlus**: http://www.pushplus.plus/
- **GitHub Token**: https://github.com/settings/tokens

---

## 项目文档快速导航

- 📖 [README.md](../README.md) - 完整使用说明
- ✨ [FEATURE_UPDATE.md](./FEATURE_UPDATE.md) - 新功能详解
- 🎉 [SETUP_COMPLETE.md](../SETUP_COMPLETE.md) - 初始化完成说明
- 🏗️ [architecture.md](../architecture.md) - 架构文档
- 💻 [BE_CODING_STANDARD.md](./team/BE_CODING_STANDARD.md) - 后端规范
- 🎨 [FE_CODING_STANDARD.md](./team/FE_CODING_STANDARD.md) - 前端规范
- 🧪 [QA_CHECKLIST.md](./team/QA_CHECKLIST.md) - 测试清单

---

**保存此页面便于快速查阅！** 📌
