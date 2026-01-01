# Small Hero - AI 全自动开发架构

## 项目概述
本项目是一个由 AI 全自动驱动的游戏开发项目，目标是高度复刻小小勇者（Tiny Hero）的游戏体验，包括战斗逻辑、数值系统、UI/UX 设计等核心要素。

## 技术栈

### 前端
- **框架**: React 18+ with TypeScript
- **构建工具**: Vite
- **样式**: TailwindCSS
- **状态管理**: Zustand
- **数据获取**: React Query
- **动画**: Framer Motion
- **移动端**: Capacitor (支持 Android/iOS)
- **UI 组件**: [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)

### 后端
- **框架**: Spring Boot 3.x
- **语言**: Java 17+
- **数据库**: TiDB Cloud (MySQL 兼容)
- **ORM**: Spring Data JPA
- **缓存**: Redis
- **实时通信**: WebSocket
- **API 文档**: OpenAPI 3.0

### 数据库设计原则
- 使用云端 TiDB Cloud 数据库
- 支持服务器时刻（Tick）驱动的挂机计算
- 所有游戏数值必须准确存储，不允许简化
- 设计支持横向扩展的分片策略

## AI 团队架构

### 1. 架构师（Chief Architect）
- **AI 模型**: Gemini 2.0 Flash Exp
- **工作时间**: 每天早上 9:00 UTC+8 自动触发
- **主要职责**:
  - 爬取小小勇者游戏最新资讯和玩法内容
  - 分析游戏版本更新和玩家反馈
  - 评估项目当前完成度（复刻相似度目标：95%）
  - 制定技术演进路线图
  - 生成每日任务池并分配给团队成员
  - 审核所有代码变更，确保符合质量标准

### 2. 后端开发（Backend Developer）
- **AI 模型**: GitHub Copilot Pro
- **主要职责**:
  - 实现 Spring Boot 后端服务
  - 实现游戏核心逻辑（战斗、装备、技能、英雄等系统）
  - 实现服务器 Tick 驱动的挂机收益计算
  - 编写单元测试和集成测试（覆盖率要求：80%+）
  - 更新 OpenAPI 规范文档

### 3. 前端开发（Frontend Developer）
- **AI 模型**: Gemini 2.0 Flash Exp
- **主要职责**:
  - 实现 React 前端界面
  - 复刻小小勇者的 UI/UX 设计风格
  - 实现游戏动画和特效
  - **创建和管理素材库**（图标、角色、装备等，不使用简单 emoji）
  - 实现响应式设计，支持移动端
  - 集成 Capacitor 实现原生 App 功能

### 4. 测试工程师（QA Engineer）
- **AI 模型**: Gemini 1.5 Pro
- **主要职责**:
  - 编写和执行自动化测试
  - 进行游戏逻辑验证
  - 对比原版游戏进行相似度测试
  - 性能测试和负载测试
  - UI/UX 一致性检查
  - 生成测试报告

## 质量硬性规定

### 代码增量要求
- **最小代码行数**: 每个任务必须新增至少 **200 行**有效逻辑代码
- **最大代码行数**: 单个任务不超过 2000 行，避免过度复杂
- **禁止简化修改**: 不允许只修改几行代码或删除几行代码的"敷衍"提交

### 关联性检查
- 修改后端 Entity 时，必须同时更新 `api-spec/openapi.yaml`
- 修改后端 API 时，必须同步更新前端 API 调用代码
- 新增数据库字段时，必须同时更新前后端对应代码

### 测试覆盖要求
- 每个新增的 Service 必须配备对应的 JUnit 单元测试
- 测试覆盖率目标：80%+
- 关键业务逻辑（战斗、数值计算）覆盖率要求：90%+

### 禁止的代码模式
- `TODO` 注释（必须立即实现，不允许留待后续）
- `FIXME` 注释
- `console.log` / `System.out.println`（使用正规日志框架）
- 硬编码的魔法数字（必须使用常量或配置）

## 游戏功能演进优先级

### P1 - 基础核心系统
1. **战斗系统**: 服务器 Tick 驱动的挂机战斗，包括攻击、技能、暴击等机制
2. **属性系统**: 力量、敏捷、智力等一级属性，以及攻击力、防御力等二级属性计算

### P2 - 进阶系统
3. **装备系统**: 装备穿戴、强化、品质系统
4. **技能系统**: 主动技能、被动技能、技能升级

### P3 - 内容系统
5. **英雄系统**: 英雄招募、升级、转职
6. **副本系统**: 关卡设计、怪物配置、掉落系统

### P4 - 经济系统
7. **货币系统**: 金币、钻石、以太货币等多种货币
8. **商店系统**: 道具购买、刷新机制

### P5 - 后期系统
9. **雕像系统**: 后期增幅系统，包括各种雕像效果
10. **成就系统**: 成就解锁和奖励

## 数值系统设计原则

### 属性计算公式
```
二级属性 = 基础值 + Σ(一级属性 × 系数)
```

示例：
```
攻击力 = 基础攻击力 + (力量 × 2) + (敏捷 × 0.5)
暴击率 = 基础暴击率 + (敏捷 × 0.001)
```

### 战斗计算
- 必须实现服务器 Tick（每秒计算）
- 即使前端关闭，后端也必须在数据库中准确计算收益
- 战斗日志必须完整记录，支持回放

## 工作流程

### 1. 每日流程（自动化）
```
09:00 UTC+8: 架构师启动
├── 爬取游戏最新资讯（TapTap、Reddit、B站等）
├── 分析游戏更新内容
├── 评估项目当前进度
├── 生成本日任务池
└── 创建 GitHub Issues 分配任务

任务分配后：
├── 后端任务 → 触发后端开发 Workflow
├── 前端任务 → 触发前端开发 Workflow
└── 测试任务 → 自动化测试

代码提交后：
├── 创建 Pull Request
├── 触发 QA 测试 Workflow
├── AI 代码审查
└── 合并到主分支
```

### 2. 分支策略
- **主分支**: `main`
- **功能分支**: `feature/backend-issue-{number}`, `feature/frontend-issue-{number}`
- **热修复分支**: `hotfix/{description}`

### 3. 提交信息格式
```
[{member-id}] {type}: {description}

示例：
[architect] feat: Add daily task generation system
[backend-dev] feat: Implement combat system core logic
[frontend-dev] feat: Create hero selection UI
[qa-tester] test: Add integration tests for equipment system
```

## 跨端适配

### 移动端要求
- 所有 UI 必须经过 Capacitor 适配层检查
- 确保在 Android/iOS 不同刘海屏下像素完美对齐
- 支持触摸手势（滑动、缩放、长按）
- 适配不同屏幕尺寸（5.5" - 6.7"）

### 性能要求
- 首屏加载时间 < 2 秒
- 战斗帧率 ≥ 60 FPS
- API 响应时间 < 200ms
- 内存占用 < 150MB

## 素材管理

### 素材库结构
```
frontend/src/assets/game/
├── sprites/          # 角色和怪物精灵图
├── icons/            # UI 图标
├── backgrounds/      # 背景图
├── effects/          # 特效资源
└── animations/       # 动画资源
```

### 素材来源
- 使用 AI 生成工具创建原创素材
- 参考小小勇者的美术风格
- 确保素材质量符合移动端游戏标准（2x, 3x 图）

## 监控和报告

### 每日报告内容
- 任务完成情况
- 代码增量统计
- 测试覆盖率变化
- 游戏完成度评估
- 下一步计划

### 质量指标
- 代码质量评分
- 测试通过率
- 性能指标
- 复刻相似度评分

## Git 配置
- **用户名**: Anyeling0620
- **邮箱**: 3463645195@qq.com
- **默认分支**: main

## 环境变量（GitHub Secrets）
```
DB_HOST              # 数据库主机地址
DB_NAME              # 数据库名称
DB_PASSWORD          # 数据库密码
DB_PORT              # 数据库端口
DB_USER              # 数据库用户名
GEMINI_API_KEY       # Gemini AI API 密钥
GH_PAT               # GitHub Personal Access Token
SPRING_DATASOURCE_URL # Spring Boot 数据库连接 URL
```

## 参考链接
- [小小勇者 TapTap](https://www.taptap.cn/app/233851)
- [UI 组件库](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
- [项目仓库](https://github.com/Anyeling0620/Small-Hero)
