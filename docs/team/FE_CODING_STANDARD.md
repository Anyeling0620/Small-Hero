# 前端开发编码规范

## 1. 项目结构

```
frontend/src/
├── main.tsx                    # 应用入口
├── App.tsx                     # 根组件
├── assets/                     # 静态资源
│   └── game/                   # 游戏素材库
│       ├── sprites/            # 角色精灵图
│       ├── icons/              # UI 图标
│       ├── backgrounds/        # 背景图
│       ├── effects/            # 特效资源
│       └── animations/         # 动画资源
├── components/                 # 可复用组件
│   ├── ui/                     # 基础 UI 组件
│   ├── game/                   # 游戏组件
│   └── layout/                 # 布局组件
├── pages/                      # 页面组件
│   ├── Home/
│   ├── Combat/
│   ├── Hero/
│   └── Equipment/
├── hooks/                      # 自定义 Hooks
│   ├── useHero.ts
│   ├── useCombat.ts
│   └── useEquipment.ts
├── stores/                     # Zustand 状态管理
│   ├── heroStore.ts
│   ├── combatStore.ts
│   └── uiStore.ts
├── services/                   # API 服务
│   ├── api.ts
│   ├── heroService.ts
│   └── combatService.ts
├── types/                      # TypeScript 类型定义
│   ├── hero.ts
│   ├── combat.ts
│   └── equipment.ts
└── utils/                      # 工具函数
    ├── calculator.ts
    └── formatter.ts
```

## 2. 命名规范

### 2.1 组件命名
- **组件文件**: PascalCase，如 `HeroCard.tsx`, `CombatScene.tsx`
- **组件函数**: 与文件名一致
- **组件文件夹**: 包含 `index.tsx` 和相关文件

```typescript
// HeroCard/index.tsx
export const HeroCard: React.FC<HeroCardProps> = ({ hero }) => {
  return <div>...</div>;
};
```

### 2.2 变量和函数命名
- **变量**: camelCase，如 `heroLevel`, `attackPower`
- **常量**: UPPER_SNAKE_CASE，如 `MAX_LEVEL`, `BASE_ATTACK`
- **函数**: camelCase，动词开头，如 `calculateDamage`, `fetchHeroData`
- **布尔值**: `is/has/can` 前缀，如 `isLoading`, `hasEquipment`

### 2.3 类型命名
- **Interface**: PascalCase + Props/Type，如 `HeroProps`, `CombatState`
- **Enum**: PascalCase，如 `HeroClass`, `EquipmentRarity`

## 3. TypeScript 类型定义

### 3.1 组件 Props
```typescript
interface HeroCardProps {
  hero: Hero;
  onSelect?: (hero: Hero) => void;
  className?: string;
}

export const HeroCard: React.FC<HeroCardProps> = ({ 
  hero, 
  onSelect,
  className 
}) => {
  // 实现
};
```

### 3.2 API 响应类型
```typescript
// types/hero.ts
export interface Hero {
  id: number;
  name: string;
  level: number;
  strength: number;
  agility: number;
  intelligence: number;
  attackPower: number;
  createdAt: string;
  updatedAt: string;
}

export interface CreateHeroRequest {
  name: string;
  strength: number;
  agility: number;
  intelligence: number;
}
```

## 4. 状态管理（Zustand）

### 4.1 Store 定义
```typescript
// stores/heroStore.ts
import { create } from 'zustand';

interface HeroStore {
  heroes: Hero[];
  selectedHero: Hero | null;
  isLoading: boolean;
  
  // Actions
  setHeroes: (heroes: Hero[]) => void;
  selectHero: (hero: Hero | null) => void;
  addHero: (hero: Hero) => void;
  updateHero: (id: number, updates: Partial<Hero>) => void;
}

export const useHeroStore = create<HeroStore>((set) => ({
  heroes: [],
  selectedHero: null,
  isLoading: false,
  
  setHeroes: (heroes) => set({ heroes }),
  selectHero: (hero) => set({ selectedHero: hero }),
  addHero: (hero) => set((state) => ({ 
    heroes: [...state.heroes, hero] 
  })),
  updateHero: (id, updates) => set((state) => ({
    heroes: state.heroes.map(h => 
      h.id === id ? { ...h, ...updates } : h
    )
  })),
}));
```

## 5. API 集成

### 5.1 API 客户端
```typescript
// services/api.ts
import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8080/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 响应拦截器
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);
```

### 5.2 Service 层
```typescript
// services/heroService.ts
import { api } from './api';
import type { Hero, CreateHeroRequest } from '@/types/hero';

export const heroService = {
  async getHeroes(): Promise<Hero[]> {
    return api.get('/heroes');
  },
  
  async getHero(id: number): Promise<Hero> {
    return api.get(`/heroes/${id}`);
  },
  
  async createHero(data: CreateHeroRequest): Promise<Hero> {
    return api.post('/heroes', data);
  },
  
  async updateHero(id: number, data: Partial<Hero>): Promise<Hero> {
    return api.put(`/heroes/${id}`, data);
  },
};
```

### 5.3 使用 React Query
```typescript
// hooks/useHero.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { heroService } from '@/services/heroService';

export const useHeroes = () => {
  return useQuery({
    queryKey: ['heroes'],
    queryFn: heroService.getHeroes,
  });
};

export const useCreateHero = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: heroService.createHero,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['heroes'] });
    },
  });
};
```

## 6. 组件开发规范

### 6.1 函数组件标准结构
```typescript
import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useHeroStore } from '@/stores/heroStore';
import type { Hero } from '@/types/hero';

interface HeroCardProps {
  hero: Hero;
  onSelect?: (hero: Hero) => void;
}

export const HeroCard: React.FC<HeroCardProps> = ({ hero, onSelect }) => {
  // 1. Hooks
  const [isHovered, setIsHovered] = useState(false);
  const { selectHero } = useHeroStore();
  
  // 2. Effects
  useEffect(() => {
    // 初始化逻辑
  }, []);
  
  // 3. 事件处理函数
  const handleClick = () => {
    selectHero(hero);
    onSelect?.(hero);
  };
  
  // 4. 渲染
  return (
    <motion.div
      className="hero-card"
      whileHover={{ scale: 1.05 }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={handleClick}
    >
      <img src={hero.avatar} alt={hero.name} />
      <h3>{hero.name}</h3>
      <p>Level {hero.level}</p>
    </motion.div>
  );
};
```

### 6.2 使用 TailwindCSS
```typescript
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

// 工具函数：合并 Tailwind 类名
export const cn = (...inputs: (string | undefined)[]) => {
  return twMerge(clsx(inputs));
};

// 使用示例
export const Button: React.FC<ButtonProps> = ({ 
  variant = 'primary',
  className,
  ...props 
}) => {
  return (
    <button
      className={cn(
        'px-4 py-2 rounded font-medium transition-colors',
        variant === 'primary' && 'bg-blue-500 text-white hover:bg-blue-600',
        variant === 'secondary' && 'bg-gray-500 text-white hover:bg-gray-600',
        className
      )}
      {...props}
    />
  );
};
```

## 7. 素材管理规范

### 7.1 素材库结构
```
assets/game/
├── sprites/
│   ├── hero-warrior.png        # 战士精灵图
│   ├── hero-mage.png           # 法师精灵图
│   └── monster-goblin.png      # 哥布林精灵图
├── icons/
│   ├── sword-icon.png          # 剑图标
│   ├── shield-icon.png         # 盾图标
│   └── potion-icon.png         # 药水图标
├── backgrounds/
│   ├── dungeon-bg.jpg          # 副本背景
│   └── tavern-bg.jpg           # 酒馆背景
└── effects/
    ├── hit-effect.png          # 攻击特效
    └── level-up.png            # 升级特效
```

### 7.2 素材导入和使用
```typescript
// utils/assets.ts
// 禁止使用 emoji 或简单文字！必须使用真实素材

export const HERO_SPRITES = {
  warrior: new URL('@/assets/game/sprites/hero-warrior.png', import.meta.url).href,
  mage: new URL('@/assets/game/sprites/hero-mage.png', import.meta.url).href,
  archer: new URL('@/assets/game/sprites/hero-archer.png', import.meta.url).href,
};

export const ITEM_ICONS = {
  sword: new URL('@/assets/game/icons/sword-icon.png', import.meta.url).href,
  shield: new URL('@/assets/game/icons/shield-icon.png', import.meta.url).href,
};

// 使用
<img src={HERO_SPRITES.warrior} alt="Warrior" />
```

### 7.3 响应式图片
```typescript
// 使用 2x, 3x 图提升清晰度
<img
  src={heroSprite}
  srcSet={`${heroSprite} 1x, ${heroSprite2x} 2x, ${heroSprite3x} 3x`}
  alt="Hero"
  className="w-32 h-32"
/>
```

## 8. 动画规范

### 8.1 使用 Framer Motion
```typescript
import { motion } from 'framer-motion';

export const CombatScene: React.FC = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
    >
      {/* 战斗场景内容 */}
    </motion.div>
  );
};

// 列表动画
const listVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const itemVariants = {
  hidden: { opacity: 0, x: -20 },
  show: { opacity: 1, x: 0 }
};

<motion.ul variants={listVariants} initial="hidden" animate="show">
  {heroes.map(hero => (
    <motion.li key={hero.id} variants={itemVariants}>
      <HeroCard hero={hero} />
    </motion.li>
  ))}
</motion.ul>
```

## 9. 性能优化

### 9.1 使用 React.memo
```typescript
export const HeroCard = React.memo<HeroCardProps>(({ hero }) => {
  return <div>...</div>;
}, (prevProps, nextProps) => {
  return prevProps.hero.id === nextProps.hero.id;
});
```

### 9.2 懒加载
```typescript
import { lazy, Suspense } from 'react';

const CombatPage = lazy(() => import('@/pages/Combat'));

<Suspense fallback={<LoadingSpinner />}>
  <CombatPage />
</Suspense>
```

## 10. 移动端适配

### 10.1 响应式设计
```typescript
// 使用 Tailwind 响应式类
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* 卡片列表 */}
</div>

// 移动端触摸优化
<button className="touch-manipulation active:scale-95">
  点击
</button>
```

### 10.2 Capacitor 集成
```typescript
import { Haptics, ImpactStyle } from '@capacitor/haptics';

const handleAttack = async () => {
  // 触发震动反馈
  await Haptics.impact({ style: ImpactStyle.Medium });
  
  // 执行攻击逻辑
  combat.attack();
};
```

## 11. 代码质量要求

### 11.1 禁止的模式
- ❌ 不使用 `console.log`（使用正规日志库）
- ❌ 不使用 `any` 类型
- ❌ 不使用内联样式（使用 Tailwind）
- ❌ 不使用 emoji 或文字代替图标
- ❌ 不使用 `TODO` 注释

### 11.2 必须遵守
- ✅ 所有组件必须有 TypeScript 类型
- ✅ 所有 API 调用必须有错误处理
- ✅ 所有素材必须使用真实资源文件
- ✅ 响应式设计支持移动端
- ✅ 关键交互有动画反馈

## 12. Git 提交规范

```
[frontend-dev] feat: Implement hero selection UI

- Create HeroCard component with animation
- Add hero sprite assets (warrior, mage, archer)
- Implement hero selection logic with Zustand
- Add responsive grid layout
- Integrate with backend hero API

Estimated lines: 280
```
