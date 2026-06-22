# Resonant-Soul 优化版 (MindMate Pro) - 项目开发指南

> 本文档为 Resonant-Soul 优化版项目的完整开发流程指南，包含技术栈、架构设计、开发规范、部署方案等所有开发所需信息。

***

## 目录

- [1. 项目概述](#1-项目概述)
- [2. 技术栈清单](#2-技术栈清单)
- [3. 项目目录结构](#3-项目目录结构)
- [4. 数据库设计](#4-数据库设计)
- [5. API接口设计](#5-api接口设计)
- [6. 安全设计](#6-安全设计)
- [7. 开发规范](#7-开发规范)
- [8. 测试策略](#8-测试策略)
- [9. 部署方案](#9-部署方案)
- [10. 开发计划](#10-开发计划)
- [11. 验收标准](#11-验收标准)

***

## 1. 项目概述

### 1.1 项目信息

| 项目名称 | 心灵伙伴 Pro (MindMate Pro)                                                                 |
| ---- | --------------------------------------------------------------------------------------- |
| 项目定位 | 面向大学生的AI心理健康陪伴平台                                                                        |
| 核心价值 | 提供7×24小时AI心理咨询、情绪分析、心理评估、放松训练等一站式服务                                                     |
| 目标用户 | 大学生、心理咨询需求者                                                                             |
| 版本   | V2.0 (优化版)                                                                              |
| 源码地址 | [https://github.com/hhjk21/resonantsoul](https://github.com/yourusername/resonant-soul) |

### 1.2 核心功能模块

| 模块       | 功能描述                       | 优先级 |
| -------- | -------------------------- | --- |
| **智能对话** | 基于Camel-AI的AI心理咨询对话，实时情绪识别 | P0  |
| **情绪分析** | 关键词匹配+LLM识别用户情绪，生成可视化图表    | P0  |
| **心理评估** | SAS焦虑自评量表，支持评估历史追踪         | P0  |
| **放松训练** | 呼吸放松、渐进性肌肉放松、正念冥想指导        | P1  |
| **统计分析** | 用户使用数据可视化，心理健康趋势分析         | P1  |
| **用户管理** | 注册登录、密码修改、管理员后台            | P0  |
| **放松指导** | 个性化放松方案推荐                  | P2  |

### 1.3 用户故事 (User Stories)

#### 1.3.1 用户认证

- **US-001**: 作为新用户，我希望能注册账号，以便使用个性化服务
- **US-002**: 作为已注册用户，我希望能登录系统，以便访问我的数据
- **US-003**: 作为用户，我希望修改密码，以便保护账户安全
- **US-004**: 作为管理员，我希望能管理用户，以便维护平台秩序

#### 1.3.2 智能对话

- **US-010**: 作为用户，我希望能与AI对话，以便获得心理支持
- **US-011**: 作为用户，我希望系统能识别我的情绪，以便获得针对性帮助
- **US-012**: 作为用户，我希望查看对话历史，以便回顾我的咨询记录

#### 1.3.3 心理评估

- **US-020**: 作为用户，我希望完成SAS评估，以便了解焦虑水平
- **US-021**: 作为用户，我希望查看评估历史，以便追踪心理状态变化
- **US-022**: 作为用户，我希望获得专业建议，以便改善心理健康

#### 1.3.4 情绪管理

- **US-030**: 作为用户，我希望记录情绪日记，以便了解情绪变化
- **US-031**: 作为用户，我希望查看情绪统计，以便了解情绪趋势

### 1.4 竞品分析

| 竞品     | 优点               | 缺点      |
| ------ | ---------------- | ------- |
| Wysa   | AI对话体验好，用户量大     | 免费功能有限  |
| Woebot | 情绪跟踪功能完善         | 对话灵活性不足 |
| 我们的优势  | 开源可定制、功能完整、中文支持好 | 品牌知名度不足 |

***

## 2. 技术栈清单

### 2.1 后端技术

| 层级          | 技术选型                | 版本     | 说明              |
| ----------- | ------------------- | ------ | --------------- |
| **编程语言**    | Python              | 3.10+  | 主力语言            |
| **Web框架**   | FastAPI             | 0.104+ | 高性能API框架        |
| **异步框架**    | Uvicorn             | 0.24+  | ASGI服务器         |
| **LLM框架**   | Camel-AI            | 0.2.72 | 角色扮演对话          |
| **数据库**     | SQLite / PostgreSQL | -      | 开发用SQLite，生产用PG |
| **ORM**     | SQLAlchemy          | 2.0+   | 强大的ORM功能        |
| **任务队列**    | Celery + Redis      | -      | 异步任务处理          |
| **缓存**      | Redis               | 7.0+   | 会话缓存、限流         |
| **配置管理**    | Pydantic Settings   | 2.0+   | 类型安全配置          |
| **数据验证**    | Pydantic            | 2.0+   | 请求/响应验证         |
| **日志**      | Loguru              | 0.7+   | 结构化日志           |
| **加密**      | Cryptography        | 41.0+  | API Key加密       |
| **HTTP客户端** | httpx               | 0.25+  | 异步HTTP请求        |

### 2.2 前端技术

| 层级          | 技术选型               | 版本    | 说明      |
| ----------- | ------------------ | ----- | ------- |
| **核心框架**    | React              | 18.2+ | 主流前端框架  |
| **UI框架**    | Ant Design         | 5.0+  | 企业级组件库  |
| **状态管理**    | Zustand            | 4.4+  | 轻量级状态管理 |
| **图表库**     | ECharts / Recharts | -     | 数据可视化   |
| **构建工具**    | Vite               | 5.0+  | 快速构建    |
| **HTTP客户端** | Axios              | 1.6+  | API请求   |
| **路由**      | React Router       | 6.0+  | 前端路由    |
| **样式**      | Tailwind CSS       | 3.0+  | 原子化CSS  |

### 2.3 DevOps技术

| 类别        | 技术选型                    | 说明     |
| --------- | ----------------------- | ------ |
| **容器化**   | Docker + Docker Compose | 一键部署   |
| **CI/CD** | GitHub Actions          | 自动化构建  |
| **反向代理**  | Nginx                   | 生产环境部署 |
| **云服务**   | 阿里云/腾讯云                 | 可选     |

### 2.4 核心依赖 (pyproject.toml)

```toml
[project]
name = "mindmate-pro"
version = "2.0.0"
description = "AI心理健康助手 - 面向大学生的智能心理咨询平台"
requires-python = ">=3.10"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]

dependencies = [
    # Web框架
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    
    # LLM框架
    "camel-ai[all]==0.2.72",
    
    # 数据库
    "sqlalchemy>=2.0.0",
    "alembic>=1.12.0",
    "asyncpg>=0.29.0",
    "aiosqlite>=0.19.0",
    
    # 配置与验证
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "python-dotenv>=1.0.0",
    
    # 安全
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "cryptography>=41.0.0",
    
    # 缓存与队列
    "redis>=5.0.0",
    "celery>=5.3.0",
    
    # 工具
    "loguru>=0.7.0",
    "httpx>=0.25.0",
    "python-multipart>=0.0.6",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "mypy>=1.6.0",
    "black>=23.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.mypy]
python_version = "3.10"
strict = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

***

## 3. 项目目录结构

```
mindmate-pro/
├── backend/                          # 后端项目
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI入口
│   │   ├── config.py                 # 配置管理
│   │   ├── database.py               # 数据库连接
│   │   ├── deps.py                   # 依赖注入
│   │   │
│   │   ├── api/                      # API路由
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py         # 路由汇总
│   │   │   │   ├── auth.py           # 认证接口
│   │   │   │   ├── users.py          # 用户接口
│   │   │   │   ├── chat.py           # 对话接口
│   │   │   │   ├── emotion.py        # 情绪接口
│   │   │   │   ├── assessment.py     # 评估接口
│   │   │   │   └── statistics.py     # 统计接口
│   │   │   └── deps.py               # API依赖
│   │   │
│   │   ├── core/                     # 核心模块
│   │   │   ├── __init__.py
│   │   │   ├── config.py            # 配置类
│   │   │   ├── security.py          # 安全工具
│   │   │   ├── jwt.py               # JWT工具
│   │   │   ├── encryption.py        # 加密工具
│   │   │   └── exceptions.py        # 自定义异常
│   │   │
│   │   ├── models/                   # SQLAlchemy模型
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # 基础模型
│   │   │   ├── user.py              # 用户模型
│   │   │   ├── emotion.py           # 情绪模型
│   │   │   ├── conversation.py      # 对话模型
│   │   │   └── assessment.py        # 评估模型
│   │   │
│   │   ├── schemas/                  # Pydantic模型
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # 基础Schema
│   │   │   ├── user.py              # 用户Schema
│   │   │   ├── auth.py              # 认证Schema
│   │   │   ├── chat.py              # 对话Schema
│   │   │   ├── emotion.py           # 情绪Schema
│   │   │   ├── assessment.py        # 评估Schema
│   │   │   └── response.py         # 响应Schema
│   │   │
│   │   ├── services/                 # 业务逻辑
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py      # 认证服务
│   │   │   ├── user_service.py      # 用户服务
│   │   │   ├── chat_service.py      # 对话服务
│   │   │   ├── emotion_service.py   # 情绪服务
│   │   │   ├── assessment_service.py # 评估服务
│   │   │   └── llm_service.py       # LLM服务
│   │   │
│   │   └── utils/                    # 工具函数
│   │       ├── __init__.py
│   │       ├── emotion_analyzer.py   # 情绪分析器
│   │       ├── llm_client.py         # LLM客户端
│   │       └── chart_generator.py    # 图表生成器
│   │
│   ├── tests/                        # 测试目录
│   │   ├── __init__.py
│   │   ├── conftest.py              # pytest配置
│   │   ├── fixtures/                # 测试数据
│   │   ├── unit/                   # 单元测试
│   │   │   ├── test_auth.py
│   │   │   ├── test_user.py
│   │   │   └── test_emotion.py
│   │   └── integration/             # 集成测试
│   │       ├── test_api_auth.py
│   │       └── test_api_chat.py
│   │
│   ├── alembic/                      # 数据库迁移
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/                # 迁移版本
│   │
│   ├── .env.example                 # 环境变量示例
│   ├── pyproject.toml
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── frontend/                         # 前端项目
│   ├── src/
│   │   ├── api/                     # API调用
│   │   │   ├── client.ts           # Axios配置
│   │   │   ├── auth.ts             # 认证API
│   │   │   ├── chat.ts            # 对话API
│   │   │   ├── emotion.ts         # 情绪API
│   │   │   └── user.ts            # 用户API
│   │   │
│   │   ├── components/              # 公共组件
│   │   │   ├── common/             # 通用组件
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   └── Modal.tsx
│   │   │   ├── layout/            # 布局组件
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Footer.tsx
│   │   │   └── charts/           # 图表组件
│   │   │       ├── EmotionPieChart.tsx
│   │   │       ├── ActivityLineChart.tsx
│   │   │       └── AssessmentBarChart.tsx
│   │   │
│   │   ├── pages/                  # 页面组件
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   ├── Chat.tsx
│   │   │   ├── Assessment.tsx
│   │   │   ├── EmotionDiary.tsx
│   │   │   ├── Statistics.tsx
│   │   │   ├── Profile.tsx
│   │   │   └── Admin.tsx
│   │   │
│   │   ├── stores/                # 状态管理
│   │   │   ├── authStore.ts
│   │   │   ├── chatStore.ts
│   │   │   └── userStore.ts
│   │   │
│   │   ├── hooks/                 # 自定义Hook
│   │   │   ├── useAuth.ts
│   │   │   ├── useChat.ts
│   │   │   └── useStatistics.ts
│   │   │
│   │   ├── utils/                 # 工具函数
│   │   │   ├── request.ts
│   │   │   ├── storage.ts
│   │   │   └── validation.ts
│   │   │
│   │   ├── styles/               # 样式文件
│   │   │   ├── global.css
│   │   │   └── variables.css
│   │   │
│   │   ├── types/                # TypeScript类型
│   │   │   ├── user.ts
│   │   │   ├── chat.ts
│   │   │   └── api.ts
│   │   │
│   │   ├── router/               # 路由配置
│   │   │   └── index.tsx
│   │   │
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── docs/                           # 项目文档
│   ├── images/                    # 文档图片
│   ├── PRD.md                    # 产品需求文档
│   ├── SPEC.md                   # 技术规格文档
│   ├── API.md                    # API接口文档
│   ├── DATABASE.md               # 数据库设计文档
│   ├── DEPLOY.md                 # 部署文档
│   └── CHANGELOG.md              # 更新日志
│
├── docker-compose.yml             # 总体编排
├── .gitignore
├── LICENSE
└── README.md
```

***

## 4. 数据库设计

### 4.1 数据库选型

| 环境   | 数据库        | 版本  | 说明         |
| ---- | ---------- | --- | ---------- |
| 开发环境 | SQLite     | 3.x | 轻量级，无需安装   |
| 生产环境 | PostgreSQL | 15+ | 高性能，支持JSON |

### 4.2 ER图

```
┌─────────────┐       ┌─────────────────┐
│    users    │       │    emotions     │
├─────────────┤       ├─────────────────┤
│ id (PK)     │──────<│ id (PK)         │
│ username    │       │ user_id (FK)    │
│ email      │       │ emotions (JSON) │
│ password   │       │ user_input      │
│ nickname   │       │ created_at      │
│ is_admin   │       └─────────────────┘
│ status     │              │
│ created_at │              │
└─────────────┘              │
        │                   │
        │            ┌──────┴──────┐
        │            │             │
        ▼            ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌───────────────┐
│conversations│ │ assessments │ │relaxation_logs│
├─────────────┤ ├─────────────┤ ├───────────────┤
│ id (PK)     │ │ id (PK)     │ │ id (PK)       │
│ user_id(FK) │ │ user_id(FK) │ │ user_id (FK)  │
│ user_input  │ │ type        │ │ type          │
│ ai_response │ │ scores(J)   │ │ duration      │
│ emotions    │ │ total_score │ │ created_at    │
│ created_at  │ │ result      │ └───────────────┘
└─────────────┘ │ created_at  │
                └─────────────┘
```

### 4.3 表结构设计

#### 4.3.1 users (用户表)

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nickname VARCHAR(50),
    avatar_url VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE,
    status SMALLINT DEFAULT 1,  -- 1: 正常, 0: 禁用
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);
```

#### 4.3.2 emotions (情绪记录表)

```sql
CREATE TABLE emotions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    emotions JSONB NOT NULL,  -- ["焦虑", "压力"]
    user_input TEXT,
    intensity INTEGER,  -- 情绪强度 1-10
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_emotions_user_id ON emotions(user_id);
CREATE INDEX idx_emotions_created_at ON emotions(created_at);
CREATE INDEX idx_emotions_user_created ON emotions(user_id, created_at);
```

#### 4.3.3 conversations (对话记录表)

```sql
CREATE TABLE conversations (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user_input TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    emotions JSONB,
    tokens_used INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at);
```

#### 4.3.4 assessments (评估记录表)

```sql
CREATE TABLE assessments (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assessment_type VARCHAR(20) NOT NULL,  -- 'SAS', 'PHQ-9', 'SDS'
    scores JSONB NOT NULL,
    total_score INTEGER NOT NULL,
    result VARCHAR(100) NOT NULL,
    advice TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_assessments_user_id ON assessments(user_id);
CREATE INDEX idx_assessments_type ON assessments(assessment_type);
CREATE INDEX idx_assessments_user_created ON assessments(user_id, created_at);
```

#### 4.3.5 relaxation\_logs (放松训练记录表)

```sql
CREATE TABLE relaxation_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    relaxation_type VARCHAR(50) NOT NULL,  -- 'breathing', 'muscle', 'meditation'
    duration_seconds INTEGER,
    completed BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_relaxation_user_id ON relaxation_logs(user_id);
```

### 4.4 Alembic迁移配置

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.models.base import Base
from app.models.user import User
from app.models.emotion import Emotion
from app.models.conversation import Conversation
from app.models.assessment import Assessment

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
```

***

## 5. API接口设计

### 5.1 API规范

#### 5.1.1 基础规范

| 项目    | 规范               |
| ----- | ---------------- |
| 协议    | HTTPS            |
| 认证方式  | JWT Bearer Token |
| API版本 | /api/v1/         |
| 请求格式  | JSON             |
| 响应格式  | JSON             |
| 字符编码  | UTF-8            |

#### 5.1.2 响应格式

```json
{
    "code": 200,           // 状态码
    "message": "success",  // 消息
    "data": {},           // 数据
    "timestamp": 1234567890  // 时间戳
}
```

#### 5.1.3 错误码定义

| 错误码 | 说明     |
| --- | ------ |
| 200 | 成功     |
| 400 | 请求参数错误 |
| 401 | 未认证    |
| 403 | 无权限    |
| 404 | 资源不存在  |
| 422 | 验证错误   |
| 500 | 服务器错误  |

### 5.2 认证接口

#### POST /api/v1/auth/register - 用户注册

**请求参数**:

```json
{
    "username": "string",      // 必填，4-20位字母数字
    "email": "string",         // 可选，邮箱格式
    "password": "string",      // 必填，8-20位
    "nickname": "string"       // 可选，默认用username
}
```

**响应**:

```json
{
    "code": 200,
    "message": "注册成功",
    "data": {
        "id": 1,
        "username": "test",
        "nickname": "test",
        "token": "eyJ..."
    }
}
```

#### POST /api/v1/auth/login - 用户登录

**请求参数**:

```json
{
    "username": "string",
    "password": "string"
}
```

**响应**:

```json
{
    "code": 200,
    "message": "登录成功",
    "data": {
        "id": 1,
        "username": "test",
        "nickname": "test",
        "is_admin": false,
        "token": "eyJ...",
        "expires_in": 86400
    }
}
```

#### GET /api/v1/auth/me - 获取当前用户

**请求头**:

```
Authorization: Bearer <token>
```

**响应**:

```json
{
    "code": 200,
    "data": {
        "id": 1,
        "username": "test",
        "email": "test@example.com",
        "nickname": "test",
        "avatar_url": null,
        "is_admin": false,
        "created_at": "2024-01-01T00:00:00Z"
    }
}
```

### 5.3 对话接口

#### POST /api/v1/chat - 发送消息

**请求头**:

```
Authorization: Bearer <token>
```

**请求参数**:

```json
{
    "message": "string",      // 用户输入
    "chat_history": []        // 可选，历史消息
}
```

**响应**:

```json
{
    "code": 200,
    "data": {
        "response": "你好，我是心灵伙伴...",  // AI回复
        "emotions": ["焦虑", "压力"],        // 检测到的情绪
        "chat_id": 123
    }
}
```

#### GET /api/v1/chat/history - 获取对话历史

**请求参数**:

```
?page=1&page_size=20&start_date=2024-01-01&end_date=2024-01-31
```

**响应**:

```json
{
    "code": 200,
    "data": {
        "items": [
            {
                "id": 1,
                "user_input": "我最近压力很大",
                "ai_response": "我能理解你的感受...",
                "emotions": ["焦虑"],
                "created_at": "2024-01-01T10:00:00Z"
            }
        ],
        "total": 100,
        "page": 1,
        "page_size": 20
    }
}
```

### 5.4 情绪接口

#### POST /api/v1/emotions - 记录情绪

**请求参数**:

```json
{
    "emotions": ["焦虑", "压力"],
    "intensity": 7,
    "note": "今天工作很累"
}
```

**响应**:

```json
{
    "code": 200,
    "message": "记录成功",
    "data": {
        "id": 1,
        "emotions": ["焦虑", "压力"],
        "created_at": "2024-01-01T10:00:00Z"
    }
}
```

#### GET /api/v1/emotions/statistics - 获取情绪统计

**请求参数**:

```
?days=7&user_id=1
```

**响应**:

```json
{
    "code": 200,
    "data": {
        "total_distribution": {
            "焦虑": 15,
            "压力": 12,
            "积极": 8
        },
        "daily_distribution": {
            "2024-01-01": {"焦虑": 3, "压力": 2},
            "2024-01-02": {"焦虑": 2, "压力": 1}
        }
    }
}
```

### 5.5 评估接口

#### POST /api/v1/assessments/sas - 提交SAS评估

**请求参数**:

```json
{
    "scores": [2, 3, 2, 1, 4, 2, 3, 1, 2, 2, 1, 3, 2, 1, 2, 3, 2, 1, 2, 1, 2, 3, 1, 2, 3, 1, 2, 3, 2, 1, 2, 1, 3, 2, 1, 2, 3, 1, 2, 3]
}
```

**响应**:

```json
{
    "code": 200,
    "data": {
        "total_score": 65,
        "result": "中度焦虑",
        "advice": "建议寻求专业心理咨询...",
        "created_at": "2024-01-01T10:00:00Z"
    }
}
```

### 5.6 用户管理接口 (管理员)

#### GET /api/v1/users - 获取用户列表

**请求参数**:

```
?page=1&page_size=20&status=1
```

#### PUT /api/v1/users/{id}/status - 更新用户状态

**请求参数**:

```json
{
    "status": 0  // 0: 禁用, 1: 启用
}
```

#### DELETE /api/v1/users/{id} - 删除用户

***

## 6. 安全设计

### 6.1 认证与授权

```python
# app/core/jwt.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel

class TokenData(BaseModel):
    user_id: int
    username: str
    is_admin: bool

class JWTHandler:
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire = settings.REFRESH_TOKEN_EXPIRE_DAYS
    
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire)
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire)
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return TokenData(**payload)
        except JWTError:
            raise credentials_exception
```

### 6.2 密码安全

```python
# app/core/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """密码哈希"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """密码验证"""
    return pwd_context.verify(plain_password, hashed_password)

def validate_password_strength(password: str) -> tuple[bool, str]:
    """密码强度验证"""
    if len(password) < 8:
        return False, "密码长度至少8位"
    if not re.search(r"[A-Za-z]", password):
        return False, "密码必须包含字母"
    if not re.search(r"\d", password):
        return False, "密码必须包含数字"
    return True, "密码强度合格"
```

### 6.3 API Key加密

```python
# app/core/encryption.py
from cryptography.fernet import Fernet
from pathlib import Path

class EncryptionManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            key_path = Path("conf/encryption_key.key")
            if key_path.exists():
                with open(key_path, 'rb') as f:
                    self.cipher = Fernet(f.read())
            else:
                key = Fernet.generate_key()
                key_path.parent.mkdir(parents=True, exist_ok=True)
                with open(key_path, 'wb') as f:
                    f.write(key)
                self.cipher = Fernet(key)
        return self._instance
    
    def encrypt(self, data: str) -> str:
        """加密数据"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """解密数据"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
```

### 6.4 速率限制

```python
# app/core/rate_limit.py
from fastapi import Request, HTTPException
from redis import Redis
import time

class RateLimiter:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
    
    async def check_rate_limit(self, request: Request, limit: int = 60, window: int = 60):
        """检查速率限制"""
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        
        current = self.redis.get(key)
        if current is None:
            self.redis.setex(key, window, 1)
            return True
        
        if int(current) >= limit:
            raise HTTPException(status_code=429, detail="请求过于频繁")
        
        self.redis.incr(key)
        return True
```

***

## 7. 开发规范

### 7.1 代码风格

#### Python代码规范 (PEP 8 + Ruff)

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py310"
select = ["E", "F", "W", "I", "N", "UP", "B", "C4"]
ignore = ["E501"]

[tool.black]
line-length = 100
target-version = ["py310"]
```

#### TypeScript代码规范

```json
// tsconfig.json
{
    "compilerOptions": {
        "target": "ES2020",
        "module": "ESNext",
        "lib": ["ES2020", "DOM"],
        "jsx": "react-jsx",
        "strict": true,
        "esModuleInterop": true,
        "skipLibCheck": true,
        "forceConsistentCasingInFileNames": true,
        "resolveJsonModule": true,
        "isolatedModules": true,
        "noEmit": true,
        "baseUrl": ".",
        "paths": {
            "@/*": ["src/*"]
        }
    }
}
```

### 7.2 Git提交规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type类型**:

- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式（不影响功能）
- refactor: 重构
- test: 测试相关
- chore: 构建或辅助工具

**示例**:

```
feat(auth): 添加用户注册功能

- 支持用户名密码注册
- 添加邮箱验证
- 返回JWT Token

Closes #123
```

### 7.3 分支管理

| 分支      | 说明       | 命名                 |
| ------- | -------- | ------------------ |
| main    | 主分支，稳定版本 | main               |
| develop | 开发分支     | develop            |
| feature | 功能分支     | feature/user-auth  |
| bugfix  | 修复分支     | bugfix/login-error |
| release | 发布分支     | release/v2.0.0     |

### 7.4 代码审查清单

- [ ] 代码符合PEP 8规范
- [ ] 有适当的单元测试
- [ ] 没有硬编码的敏感信息
- [ ] API有适当的错误处理
- [ ] 数据库操作使用了事务
- [ ] 关键代码有注释
- [ ] 功能与需求文档一致

***

## 8. 测试策略

### 8.1 测试金字塔

```
           ┌─────────┐
           │   E2E   │  少量关键流程测试 (5%)
           │  Tests  │
           ├─────────┤
           │  API    │  接口测试 (25%)
           │  Tests  │
           ├─────────┤
           │ Service │  业务逻辑测试 (30%)
           │  Tests  │
           ├─────────┤
           │  Unit   │  单元测试 (40%)
           │  Tests  │
           └─────────┘
```

### 8.2 测试覆盖率目标

| 模块       | 覆盖率目标 |
| -------- | ----- |
| Core模块   | >90%  |
| Services | >80%  |
| API路由    | >70%  |
| 整体       | >70%  |

### 8.3 pytest配置

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.core.security import hash_password

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db):
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=hash_password("testpass123"),
        nickname="Test User"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

### 8.4 测试示例

```python
# tests/unit/test_auth.py
import pytest
from app.core.security import hash_password, verify_password

class TestPasswordHashing:
    def test_hash_password(self):
        password = "testpassword123"
        hashed = hash_password(password)
        assert hashed != password
        assert len(hashed) > 0
    
    def test_verify_password_correct(self):
        password = "testpassword123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        password = "testpassword123"
        hashed = hash_password(password)
        assert verify_password("wrongpassword", hashed) is False

# tests/integration/test_api_auth.py
class TestAuthAPI:
    def test_register_success(self, client):
        response = client.post("/api/v1/auth/register", json={
            "username": "newuser",
            "password": "testpass123",
            "nickname": "New User"
        })
        assert response.status_code == 200
        assert response.json()["code"] == 200
        assert "token" in response.json()["data"]
    
    def test_register_duplicate_username(self, client, test_user):
        response = client.post("/api/v1/auth/register", json={
            "username": "testuser",
            "password": "testpass123"
        })
        assert response.status_code == 400
        assert response.json()["code"] == 400
```

### 8.5 测试命令

```bash
# 运行所有测试
pytest

# 带覆盖率报告
pytest --cov=app --cov-report=html --cov-report=term

# 运行特定目录
pytest tests/unit/
pytest tests/integration/

# 运行特定文件
pytest tests/unit/test_auth.py

# 运行标记的测试
pytest -m "unit"
pytest -m "integration"
pytest -m "slow"

# 详细输出
pytest -v
pytest -vv
```

***

## 9. 部署方案

### 9.1 Docker Compose 配置

```yaml
# docker-compose.yml
version: '3.8'

services:
  # 后端API
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: mindmate-api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - LLM_API_KEY=${LLM_API_KEY}
    depends_on:
      - db
      - cache
    restart: unless-stopped
    networks:
      - backend

  # 前端
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: mindmate-frontend
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - api
    restart: unless-stopped
    networks:
      - backend

  # PostgreSQL
  db:
    image: postgres:15-alpine
    container_name: mindmate-db
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./backend/alembic/migrations:/docker-entrypoint-initdb.d
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    restart: unless-stopped
    networks:
      - backend

  # Redis
  cache:
    image: redis:7-alpine
    container_name: mindmate-cache
    volumes:
      - redisdata:/data
    command: redis-server --appendonly yes
    restart: unless-stopped
    networks:
      - backend

  # Celery Worker
  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: mindmate-celery
    command: celery -A app.celery worker --loglevel=info
    depends_on:
      - db
      - cache
    restart: unless-stopped
    networks:
      - backend

  # Celery Beat (定时任务)
  celery_beat:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: mindmate-celery-beat
    command: celery -A app.celery beat --loglevel=info
    depends_on:
      - db
      - cache
    restart: unless-stopped
    networks:
      - backend

networks:
  backend:
    driver: bridge

volumes:
  pgdata:
  redisdata:
```

### 9.2 后端Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY pyproject.toml ./

# 安装Python依赖
RUN pip install --no-cache-dir uv && \
    uv sync --frozen --no-dev

# 复制应用代码
COPY . .

# 创建非root用户
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 运行命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 9.3 前端Dockerfile

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# 生产镜像
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 9.4 Nginx配置

```nginx
# frontend/nginx.conf
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://api:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /ws/ {
        proxy_pass http://api:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 9.5 环境变量

```bash
# .env
# 数据库
DATABASE_URL=postgresql://mindmate:your_password@db:5432/mindmate
POSTGRES_DB=mindmate
POSTGRES_USER=mindmate
POSTGRES_PASSWORD=your_password

# Redis
REDIS_URL=redis://cache:6379/0

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# LLM
LLM_API_KEY=your-api-key
LLM_MODEL_TYPE=Qwen/Qwen2.5-7B-Instruct
LLM_MODEL_URL=https://api-inference.modelscope.cn/v1/

# CORS
CORS_ORIGINS=http://localhost,http://localhost:80
```

### 9.6 部署命令

```bash
# 开发环境启动
docker-compose up -d

# 生产环境启动
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# 查看日志
docker-compose logs -f

# 进入容器
docker-compose exec api /bin/bash

# 数据库迁移
docker-compose exec api alembic upgrade head

# 停止服务
docker-compose down
```

***

## 10. 开发计划

### 10.1 阶段划分

| 阶段          | 周期 | 主要任务        | 交付物         |
| ----------- | -- | ----------- | ----------- |
| **Phase 1** | 1周 | 项目初始化、架构设计  | 项目框架、技术选型确认 |
| **Phase 2** | 1周 | 数据库设计、API框架 | 数据模型、API文档  |
| **Phase 3** | 2周 | 认证模块开发      | 注册登录、JWT认证  |
| **Phase 4** | 2周 | 核心功能开发      | 对话、情绪分析、评估  |
| **Phase 5** | 1周 | 前端开发        | 完整UI界面      |
| **Phase 6** | 1周 | 测试与优化       | 测试报告、性能优化   |
| **Phase 7** | 1周 | 部署上线        | 生产环境部署      |

### 10.2 详细任务分解

#### Phase 1: 项目初始化 (Day 1-7)

- [ ] 项目仓库初始化
- [ ] 技术选型评审
- [ ] 开发环境搭建
- [ ] 项目目录结构创建
- [ ] Git分支策略制定
- [ ] CI/CD流程配置

#### Phase 2: 数据库设计 (Day 8-14)

- [ ] 数据模型设计
- [ ] Alembic迁移脚本
- [ ] 数据库连接配置
- [ ] Redis连接配置
- [ ] API响应格式定义

#### Phase 3: 认证模块 (Day 15-28)

- [ ] 用户注册接口
- [ ] 用户登录接口
- [ ] JWT Token生成与验证
- [ ] 密码加密存储
- [ ] 管理员功能
- [ ] 单元测试编写

#### Phase 4: 核心功能 (Day 29-56)

- [ ] LLM服务集成
- [ ] Camel-AI对话集成
- [ ] 情绪分析器开发
- [ ] SAS评估逻辑
- [ ] 对话历史管理
- [ ] 情绪统计功能
- [ ] 图表生成服务

#### Phase 5: 前端开发 (Day 57-77)

- [ ] 项目初始化
- [ ] 登录/注册页面
- [ ] 主对话页面
- [ ] 评估页面
- [ ] 统计页面
- [ ] 管理后台
- [ ] 响应式适配

#### Phase 6: 测试优化 (Day 78-84)

- [ ] 接口测试
- [ ] 集成测试
- [ ] 性能测试
- [ ] 安全审计
- [ ] 代码优化

#### Phase 7: 部署上线 (Day 85-91)

- [ ] Docker配置
- [ ] 生产环境部署
- [ ] 域名配置
- [ ] SSL证书
- [ ] 监控配置
- [ ] 文档完善

### 10.3 里程碑

```
Week 1 ─────── Week 2 ─────── Week 4 ─────── Week 8 ─────── Week 11 ─────── Week 12 ──── Week 13
    │             │             │             │             │             │             │
    ▼             ▼             ▼             ▼             ▼             ▼             ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ Phase 1 │→│ Phase 2 │→│ Phase 3 │→│ Phase 4 │→│ Phase 5 │→│ Phase 6 │→│ Phase 7 │
│ 项目初始化│ │ 数据库设计│ │ 认证模块│ │ 核心功能 │ │ 前端开发 │ │ 测试优化 │ │ 部署上线 │
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
                                                                                    
                │                          │                        │              
                ▼                          ▼                        ▼              
           API可用                    功能完整                  正式上线            
```

***

## 11. 验收标准

### 11.1 功能验收

| 功能模块      | 验收标准                  | 测试用例                 |
| --------- | --------------------- | -------------------- |
| **用户注册**  | 可以成功注册新用户，用户名重复时提示错误  | 注册成功、用户名重复、密码强度不足    |
| **用户登录**  | 正确的用户名密码可以登录，错误时提示    | 登录成功、密码错误、用户不存在、账号禁用 |
| **AI对话**  | 输入消息后5秒内获得AI回复        | 正常对话、情绪识别、历史记录       |
| **情绪分析**  | 自动识别用户情绪并保存           | 多种情绪识别、无情绪识别、统计图表    |
| **SAS评估** | 可以完成评估并查看结果和建议        | 正常评估、分数计算、历史查看       |
| **管理员后台** | 可以查看用户列表、禁用/启用用户、删除用户 | 用户列表、禁用用户、删除用户、保护管理员 |
| **放松训练**  | 可以选择不同类型的放松训练         | 呼吸放松、肌肉放松、冥想         |

### 11.2 非功能验收

| 指标      | 目标值          | 测量方法         |
| ------- | ------------ | ------------ |
| API响应时间 | <500ms (P95) | 性能测试         |
| 页面加载时间  | <3s          | Lighthouse   |
| 测试覆盖率   | >70%         | pytest --cov |
| 可用性     | 99.9%        | 监控统计         |
| 并发用户    | >100         | 压力测试         |

### 11.3 安全验收

| 检查项    | 要求   |
| ------ | ---- |
| SQL注入  | 无漏洞  |
| XSS攻击  | 无漏洞  |
| CSRF攻击 | 有防护  |
| 密码强度   | 强制要求 |
| API认证  | 必须   |
| 敏感信息   | 不暴露  |

### 11.4 文档验收

- [ ] README.md 完整
- [ ] API文档完整
- [ ] 部署文档完整
- [ ] 代码注释完整
- [ ] 有CHANGELOG

***

## 附录

### A. 参考资源

- [FastAPI文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy文档](https://docs.sqlalchemy.org/)
- [React文档](https://react.dev/)
- [Ant Design文档](https://ant.design/)
- [Camel-AI文档](https://www.camel-ai.org/)

### B. 联系方式

- 项目负责人: \[Your Name]
- 邮箱: \[<your.email@example.com>]
- GitHub: <https://github.com/yourusername>

### C. 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

***

> 文档版本: V1.0\
> 最后更新: 2024年\
> 维护者: Your Name

