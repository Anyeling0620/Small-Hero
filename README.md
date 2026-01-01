# Small Hero - AI 全自动开发快速启动指南

## 🎯 项目概述

这是一个由 AI 团队全自动驱动的游戏开发项目，目标是高度复刻小小勇者（Tiny Hero）游戏。

## 📋 准备工作

### 1. GitHub Secrets 配置

在 GitHub 仓库中配置以下 Secrets（Settings → Secrets and variables → Actions）：

```
DB_HOST              - TiDB Cloud 数据库主机地址
DB_NAME              - 数据库名称
DB_PASSWORD          - 数据库密码
DB_PORT              - 数据库端口（默认 4000）
DB_USER              - 数据库用户名
GEMINI_API_KEY       - Google Gemini API 密钥（主AI模型）
DEEPSEEK_API_KEY     - DeepSeek API 密钥（备用AI模型）
GH_PAT               - GitHub Personal Access Token（需要 repo 和 workflow 权限）
SPRING_DATASOURCE_URL - 完整的数据库连接 URL
PUSHPLUS_TOKEN       - PushPlus Token（用于微信通知）
```

### 2. 获取必要的 API 密钥

#### Gemini API Key（主AI模型）
1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 创建新的 API 密钥
3. 复制并保存到 GitHub Secrets

#### DeepSeek API Key（备用AI模型）
1. 访问 [DeepSeek Platform](https://platform.deepseek.com/)
2. 注册并创建 API 密钥
3. 复制并保存到 GitHub Secrets
4. **当 Gemini 不可用时，系统会自动切换到 DeepSeek**

#### PushPlus Token（微信通知）
1. 访问 [PushPlus官网](http://www.pushplus.plus/)
2. 使用微信扫码登录
3. 复制您的 Token
4. 保存到 GitHub Secrets
5. **每次任务完成都会发送详细通知到您的微信**

#### GitHub Personal Access Token
1. 访问 GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 创建新 token，勾选 `repo` 和 `workflow` 权限
3. 复制并保存到 GitHub Secrets

#### TiDB Cloud 数据库
1. 注册 [TiDB Cloud](https://tidbcloud.com/)
2. 创建免费的 Serverless 集群
3. 获取连接信息并保存到 GitHub Secrets

## 🚀 启动 AI 自动开发

### 自动定时触发（全天候加速开发）

**🚀 加速模式已启用！** AI 架构师会在每天以下时间自动运行（UTC+8）：
- **09:00** - 早间任务生成
- **13:00** - 午间任务生成
- **17:00** - 下午任务生成
- **21:00** - 晚间任务生成

每次执行会：
1. 爬取游戏最新资讯
2. 分析项目进度
3. 生成 **5-10 个高质量任务**（根据项目阶段动态调整）
4. 创建 GitHub Issues
5. 自动分配优先级（高优先级40%，中优先级40%，低优先级20%）

**✨ 并发执行能力**：
- 同时执行最多 **3 个任务**
- 后端任务：最多 **2 个并发**
- 前端任务：最多 **2 个并发**
- QA 测试：**串行执行**（确保测试准确性）

**📈 开发速度提升**：
- 从每天 3-5 个任务提升到 **每天 20-40 个任务**
- 通过并发执行，实际完成速度提升 **2-3 倍**
- 预计游戏开发周期缩短 **60-70%**

**无需任何手动操作！AI团队全天候工作！**

## 📊 工作流程

### 每日自动化流程（加速模式）

```text
每天4次执行 (09:00 / 13:00 / 17:00 / 21:00 UTC+8)
├── 架构师启动
│   ├── 爬取游戏资讯（TapTap、Reddit、B站）
│   ├── 使用 Gemini 2.5 分析游戏内容
│   ├── 评估项目当前进度
│   ├── 生成 5-10 个高质量任务（根据阶段动态调整）
│   └── 创建 GitHub Issues（自动分配优先级）
│
任务并发执行（最多3个任务同时进行）
├── 后端任务 (最多2个并发)
│   ├── 触发 "AI Backend Development" workflow
│   ├── 使用 GitHub Copilot 或 DeepSeek Coder 生成代码
│   ├── 自动运行单元测试
│   ├── 验证代码质量（200+行，80%+覆盖率）
│   └── 创建 Pull Request
│
├── 前端任务 (最多2个并发)
│   ├── 触发 "AI Frontend Development" workflow
│   ├── 使用 Gemini 2.5 或 DeepSeek 生成代码
│   ├── 生成游戏素材（如需要）
│   ├── 运行 ESLint 和构建测试
│   └── 创建 Pull Request
│
└── QA 测试 (串行执行，确保准确性)
    ├── PR 创建后自动触发 "AI QA Testing"
    ├── 运行后端和前端测试套件
    ├── AI 代码审查（Gemini 2.5 Pro）
    ├── 验证游戏逻辑正确性
    ├── 检查代码质量标准
    ├── 生成详细测试报告
    └── 在 PR 中评论测试结果

实时通知（PushPlus → 微信）
├── 任务创建 → 发送任务详情
├── 任务完成 → 发送代码统计和质量评分
├── 测试完成 → 发送测试覆盖率和结果
└── 任务失败 → 发送错误信息和重试状态

审查通过后
└── 手动合并 PR（或配置自动合并）
```

**开发效率提升：**

- 📅 **每天 4 次任务生成**：从单次提升到全天候执行
- 🔢 **每天 20-40 个任务**：从 3-5 个提升到 5-10 个/次 × 4 次
- ⚡ **并发执行能力**：2 个后端 + 2 个前端同时开发
- 🚀 **实际吞吐量**：比传统单线程快 **3-4 倍**

## 📁 项目结构

```
Small-Hero/
├── .github/workflows/          # GitHub Actions 工作流
│   ├── ai-architect-daily.yml  # 架构师每日任务
│   ├── ai-backend-dev.yml      # 后端开发
│   ├── ai-frontend-dev.yml     # 前端开发
│   └── ai-qa-testing.yml       # QA 测试
├── ai-orchestrator/            # AI 协调配置
│   ├── member-roles.json       # 团队成员角色
│   ├── project-config.json     # 项目配置
│   └── task-pool.json          # 任务池
├── scripts/                    # 自动化脚本
│   ├── architect/              # 架构师脚本
│   ├── backend/                # 后端脚本
│   ├── frontend/               # 前端脚本
│   └── qa/                     # 测试脚本
├── backend/                    # Spring Boot 后端
├── frontend/                   # React 前端
├── docs/                       # 文档
│   ├── blueprints/             # 演进蓝图
│   └── team/                   # 团队规范
└── architecture.md             # 架构文档
```

## 🔍 监控进度

### 查看每日报告

生成的研究和分析报告会保存在：
```
docs/game-research/
├── daily-reports/      # 每日游戏资讯爬取报告
├── progress-reports/   # 项目进度分析报告
└── task-summaries/     # 任务摘要
```

### 查看任务状态

所有任务都会以 GitHub Issues 的形式创建，可以在仓库的 Issues 页面查看：
- `backend` 标签：后端开发任务
- `frontend` 标签：前端开发任务
- `qa` 标签：测试任务
- `high/medium/low` 标签：优先级

### 查看 Pull Requests

每个完成的任务都会创建对应的 PR：
- 分支命名：`feature/backend-issue-{number}` 或 `feature/frontend-issue-{number}`
- PR 标题包含任务类型和描述
- PR 描述包含详细的改动说明

## ⚙️ 本地开发（可选）

如果需要本地调试：

### 后端
```powershell
cd backend
.\mvnw spring-boot:run
```

访问：http://localhost:8080/api
API 文档：http://localhost:8080/swagger-ui.html

### 前端
```powershell
cd frontend
npm install
npm run dev
```

访问：http://localhost:5173

## ✨ 新增功能特性

### 🤖 多AI模型支持（主备切换）
- **主模型**: Gemini 2.5 Flash/Pro（最新版本）
- **备用模型**: DeepSeek Chat/Coder
- **自动切换**: 当主模型不可用时，自动切换到备用模型
- **智能重试**: 每个模型最多重试 3 次，间隔 5 秒

#### AI 模型分配策略
| 角色 | 主模型 | 备用模型 | 用途 |
|------|--------|----------|------|
| 架构师 | Gemini 2.5 Flash | DeepSeek Chat | 游戏分析、任务生成 |
| 后端开发 | GitHub Copilot | DeepSeek Coder | 后端代码生成 |
| 前端开发 | Gemini 2.5 Flash | DeepSeek Chat | 前端代码生成 |
| 测试工程师 | Gemini 2.5 Pro | DeepSeek Chat | 测试和质量检查 |

### 📱 PushPlus 微信通知
实时推送任务进度到您的微信，包含以下通知：

- **任务创建**: 新任务生成时推送详情
- **任务完成**: 展示代码统计、质量评分、PR链接
- **任务失败**: 错误信息和重试状态
- **PR创建**: PR编号、变更统计、查看链接
- **测试结果**: 通过率、覆盖率、失败详情
- **每日报告**: 汇总当日所有开发活动

#### 通知示例
```
✅ 任务完成: 实现战斗系统核心逻辑

📊 代码统计
• 修改文件: 12 个
• 新增代码: +350 行
• 删除代码: -45 行

🎯 质量指标
• 代码质量: 95/100
• 测试覆盖率: 87%

🔗 Pull Request: #42
```

### 🔒 并发锁机制
确保任务串行执行，避免冲突：

- **自动加锁**: 任务开始时自动获取锁
- **防止并发**: 同一时间只允许一个任务执行
- **超时释放**: 1小时未完成自动释放锁
- **等待队列**: 任务排队等待，最长等待10分钟

### 🔄 错误重试机制
提高系统稳定性：

- **自动重试**: 失败后自动重试最多3次
- **指数退避**: 重试间隔逐渐增加（5秒 → 10秒 → 15秒）
- **模型切换**: 主模型失败后切换到备用模型
- **通知告警**: 失败时立即发送通知

## 📊 质量硬性规定

### 代码增量要求
- ✅ 每个任务必须新增至少 **200 行**有效代码
- ✅ 后端改动必须包含单元测试
- ✅ 修改数据模型必须同时更新 OpenAPI 规范
- ✅ 前端必须使用真实素材，不能用 emoji 或文字

### 测试覆盖率
- 后端测试覆盖率目标：**80%+**
- 关键业务逻辑覆盖率：**90%+**

### 游戏相似度
- 目标相似度：**95%**
- 战斗逻辑必须准确实现
- UI/UX 风格高度还原

## 🛠️ 故障排查

### Workflow 失败

1. **检查 Secrets 配置**
   - 确保所有必需的 Secrets 都已配置
   - 检查 API 密钥是否有效

2. **查看 Actions 日志**
   - 进入 GitHub Actions 页面
   - 点击失败的 workflow
   - 查看详细错误日志

3. **常见问题**
   - `GEMINI_API_KEY` 配额不足 → 检查 API 使用量
   - `GH_PAT` 权限不足 → 重新生成 token 并确保权限正确
   - 数据库连接失败 → 检查 TiDB Cloud 连接信息

### 任务未自动创建

1. 检查定时任务是否正常运行（Actions 页面）
2. 手动触发 workflow 测试
3. 查看架构师脚本输出日志

## 📚 进一步学习

- **架构文档**: [architecture.md](./architecture.md)
- **后端规范**: [docs/team/BE_CODING_STANDARD.md](./docs/team/BE_CODING_STANDARD.md)
- **前端规范**: [docs/team/FE_CODING_STANDARD.md](./docs/team/FE_CODING_STANDARD.md)
- **QA 清单**: [docs/team/QA_CHECKLIST.md](./docs/team/QA_CHECKLIST.md)

## 🎮 游戏开发路线图

### 当前阶段：Foundation（基础架构）
- [x] 项目初始化
- [ ] 核心战斗系统
- [ ] 属性系统

### 下一阶段：Core Systems（核心系统）
- [ ] 装备系统
- [ ] 技能系统
- [ ] 英雄系统

### 未来阶段：Advanced Features（高级功能）
- [ ] 副本系统
- [ ] 货币和商店
- [ ] 雕像系统（后期增幅）

## 📞 联系方式

- **GitHub 仓库**: https://github.com/Anyeling0620/Small-Hero
- **邮箱**: 3463645195@qq.com

---

## 🎉 开始使用

一切配置完成后，AI 团队将：
- ✅ 每天自动分析游戏内容
- ✅ 自动生成开发任务
- ✅ 自动编写代码
- ✅ 自动运行测试
- ✅ 持续迭代直至游戏完成

**只需配置好 Secrets，然后让 AI 接管一切！** 🚀
