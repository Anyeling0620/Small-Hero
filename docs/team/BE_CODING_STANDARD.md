# 后端开发编码规范

## 1. 项目结构

```
backend/src/main/java/com/smallhero/
├── SmallHeroApplication.java          # 主应用入口
├── config/                            # 配置类
│   ├── WebSocketConfig.java
│   ├── RedisConfig.java
│   └── SecurityConfig.java
├── controller/                        # REST API 控制器
│   ├── HeroController.java
│   ├── CombatController.java
│   └── EquipmentController.java
├── service/                           # 业务逻辑层
│   ├── HeroService.java
│   ├── CombatService.java
│   └── EquipmentService.java
├── repository/                        # 数据访问层
│   ├── HeroRepository.java
│   └── EquipmentRepository.java
├── entity/                            # 数据库实体
│   ├── Hero.java
│   ├── Equipment.java
│   └── Combat.java
├── dto/                               # 数据传输对象
│   ├── request/
│   └── response/
├── exception/                         # 自定义异常
│   ├── GameException.java
│   └── GlobalExceptionHandler.java
└── util/                              # 工具类
    ├── GameCalculator.java
    └── TimeUtils.java
```

## 2. 命名规范

### 2.1 类命名
- **Entity**: 名词，如 `Hero`, `Equipment`, `Combat`
- **Service**: 名词 + Service，如 `HeroService`, `CombatService`
- **Controller**: 名词 + Controller，如 `HeroController`
- **Repository**: 名词 + Repository，如 `HeroRepository`
- **DTO**: 描述性名词 + Request/Response，如 `CreateHeroRequest`, `HeroDetailResponse`

### 2.2 方法命名
- **查询**: `findById`, `findAll`, `getHeroDetails`
- **创建**: `create`, `save`, `add`
- **更新**: `update`, `modify`
- **删除**: `delete`, `remove`
- **业务操作**: 动词开头，如 `calculateDamage`, `equipItem`, `startCombat`

### 2.3 变量命名
- 使用驼峰命名法：`heroLevel`, `attackPower`
- 常量使用大写加下划线：`MAX_LEVEL`, `BASE_ATTACK`
- 布尔值以 `is`, `has`, `can` 开头：`isAlive`, `hasEquipment`, `canLevelUp`

## 3. 代码风格

### 3.1 注解使用
```java
@RestController
@RequestMapping("/heroes")
@RequiredArgsConstructor
@Slf4j
public class HeroController {
    
    private final HeroService heroService;
    
    @GetMapping("/{id}")
    @Operation(summary = "获取英雄详情", description = "根据ID获取英雄完整信息")
    public ResponseEntity<HeroDetailResponse> getHero(@PathVariable Long id) {
        // 实现
    }
}
```

### 3.2 实体类规范
```java
@Entity
@Table(name = "heroes")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Hero {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, length = 50)
    private String name;
    
    @Column(nullable = false)
    private Integer level = 1;
    
    // 一级属性
    @Column(nullable = false)
    private Integer strength = 10;
    
    @Column(nullable = false)
    private Integer agility = 10;
    
    @Column(nullable = false)
    private Integer intelligence = 10;
    
    // 时间戳
    @CreatedDate
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @LastModifiedDate
    @Column(nullable = false)
    private LocalDateTime updatedAt;
    
    // 计算二级属性（不存储在数据库）
    @Transient
    public Integer getAttackPower() {
        return strength * 2 + agility / 2;
    }
}
```

### 3.3 Service 层规范
```java
@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class HeroService {
    
    private final HeroRepository heroRepository;
    
    public HeroDetailResponse getHeroDetails(Long id) {
        Hero hero = heroRepository.findById(id)
            .orElseThrow(() -> new GameException("英雄不存在"));
        
        return HeroDetailResponse.builder()
            .id(hero.getId())
            .name(hero.getName())
            .level(hero.getLevel())
            .attackPower(hero.getAttackPower())
            .build();
    }
    
    public Hero createHero(CreateHeroRequest request) {
        Hero hero = Hero.builder()
            .name(request.getName())
            .strength(request.getStrength())
            .agility(request.getAgility())
            .intelligence(request.getIntelligence())
            .build();
        
        return heroRepository.save(hero);
    }
}
```

## 4. 数值计算规范

### 4.1 属性计算公式必须准确
```java
public class AttributeCalculator {
    
    // 攻击力 = 基础攻击力 + (力量 × 2) + (敏捷 × 0.5)
    public static double calculateAttackPower(Hero hero) {
        double baseAttack = 10.0;
        return baseAttack + (hero.getStrength() * 2) + (hero.getAgility() * 0.5);
    }
    
    // 暴击率 = 基础暴击率 + (敏捷 × 0.001)
    public static double calculateCritRate(Hero hero) {
        double baseCritRate = 0.05;  // 5%
        return baseCritRate + (hero.getAgility() * 0.001);
    }
}
```

### 4.2 服务器 Tick 系统
```java
@Service
@Slf4j
public class GameTickService {
    
    @Scheduled(fixedRate = 1000)  // 每秒执行一次
    public void processTick() {
        // 处理所有进行中的战斗
        List<Combat> activeCombats = combatRepository.findByStatus(CombatStatus.ACTIVE);
        
        for (Combat combat : activeCombats) {
            processOneTick(combat);
        }
    }
    
    private void processOneTick(Combat combat) {
        // 计算本次 tick 的伤害
        double damage = calculateDamage(combat.getAttacker(), combat.getDefender());
        
        // 更新战斗状态
        combat.setDefenderHp(combat.getDefenderHp() - damage);
        
        // 保存到数据库
        combatRepository.save(combat);
    }
}
```

## 5. 异常处理

### 5.1 自定义异常
```java
public class GameException extends RuntimeException {
    private final String errorCode;
    
    public GameException(String message) {
        super(message);
        this.errorCode = "GAME_ERROR";
    }
    
    public GameException(String errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }
}
```

### 5.2 全局异常处理
```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {
    
    @ExceptionHandler(GameException.class)
    public ResponseEntity<ErrorResponse> handleGameException(GameException e) {
        log.error("游戏异常: {}", e.getMessage());
        return ResponseEntity.badRequest()
            .body(new ErrorResponse(e.getErrorCode(), e.getMessage()));
    }
}
```

## 6. 测试规范

### 6.1 单元测试
```java
@SpringBootTest
class HeroServiceTest {
    
    @Autowired
    private HeroService heroService;
    
    @Test
    void testCreateHero() {
        CreateHeroRequest request = CreateHeroRequest.builder()
            .name("测试英雄")
            .strength(15)
            .agility(12)
            .intelligence(10)
            .build();
        
        Hero hero = heroService.createHero(request);
        
        assertNotNull(hero.getId());
        assertEquals("测试英雄", hero.getName());
        assertEquals(40, hero.getAttackPower());  // 15*2 + 12*0.5 + 10 = 46
    }
}
```

## 7. OpenAPI 文档规范

### 7.1 Controller 文档化
```java
@Tag(name = "英雄管理", description = "英雄相关的API接口")
@RestController
@RequestMapping("/heroes")
public class HeroController {
    
    @Operation(summary = "创建英雄", description = "创建一个新的英雄角色")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "创建成功"),
        @ApiResponse(responseCode = "400", description = "请求参数错误")
    })
    @PostMapping
    public ResponseEntity<HeroResponse> createHero(
        @RequestBody @Valid CreateHeroRequest request
    ) {
        // 实现
    }
}
```

## 8. 代码质量要求

### 8.1 禁止的代码模式
- ❌ 不使用 `System.out.println`，使用 `log.info/debug/error`
- ❌ 不使用魔法数字，使用常量或配置
- ❌ 不使用 `TODO` 或 `FIXME` 注释
- ❌ 不使用过度嵌套（最多 3 层）

### 8.2 必须遵守的规则
- ✅ 每个 Service 方法必须有对应的单元测试
- ✅ 修改 Entity 必须同时更新 OpenAPI 文档
- ✅ 所有 API 必须有完整的文档注解
- ✅ 关键业务逻辑必须有日志记录
- ✅ 数据库操作必须有事务管理

## 9. Git 提交规范

```
[backend-dev] feat: Implement hero creation system

- Add Hero entity with attributes
- Add HeroService with CRUD operations
- Add HeroController with REST API
- Add unit tests for HeroService
- Update OpenAPI specification

Estimated lines: 350
```

## 10. 性能优化要点

- 使用 Redis 缓存热点数据
- 批量操作使用 `@Batch` 注解
- 避免 N+1 查询问题，使用 `@EntityGraph`
- 大数据量使用分页查询
- 异步处理耗时操作
