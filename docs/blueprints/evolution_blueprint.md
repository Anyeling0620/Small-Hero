# Small Hero 复刻级演进蓝图

## 1. 复刻基准 (Cloning Baseline)
- **核心逻辑**：必须实现“服务器时刻 (Tick)”驱动的战斗，即便前端关闭，后端也必须在 TiDB 中准确计算每一秒的收益。
- **数值精度**：力量、敏捷等对二级属性的贡献必须符合 $Attribute \times Coefficient$ 公式，禁止使用简化模型。

## 2. 演进硬指标 (Anti-Laziness Metrics)
- **单次演进规模**：架构师生成的每一个任务包，预期代码增量必须超过 **200 行** 有效逻辑代码。
- **关联性检查**：修改后端 Entity 时，必须同时强制更新 `openapi.yaml` 和前端 API 调用 Hooks。
- **测试覆盖**：每一个新增的 Service 必须配备对应的 JUnit 单元测试，否则架构师将判定演进失败。

## 3. 跨端适配 (App-Ready)
- 所有 UI 必须经过 `Capacitor` 适配层检查，确保在 Android/iOS 的不同刘海屏下像素完美对齐。