# 心灵伙伴（Resonant-Soul）——AI 心理健康助手

> 基于 Gradio + camel-ai 构建的大学生心理健康智能对话平台，提供 7×24 小时温暖陪伴。

---

## 一、项目概览

心灵伙伴是一个面向大学生的 AI 心理健康助手，集成了 **智能对话**、**心理评估**、**放松训练**、**情绪追踪** 四大核心功能模块。项目使用大语言模型（LLM）作为对话引擎，以 Gradio 构建 Web 界面，Peewee ORM 管理本地数据库。

|项目 | 说明 |
|------|------|
|**名称** |共鸣灵（心灵伙伴） |
|**定位** |AI 心理健康助手 |
|**目标用户** | 在校大学生 |
|**技术栈** |Python 3.10 + Gradio 5.x + Camel-ai + Peewee |
|**LLM 支持** | 兼容 OpenAI 接口的任意模型（默认 Qwen3-8B） |
|**数据库** |SQLite（本地） |

---

## 二、功能模块

### 2.1 智能对话

-用户输入文字后，AI 以温暖共情的语气进行心理咨询对话
-自动分析用户情绪（焦虑/抑郁/愤怒/积极/平静），并记录到数据库
-支持多轮对话，上下文记忆
-情绪趋势图（饼图）可视化展示

### 2.2 心理评估（SAS 焦虑自评量表）

-标准 20 题 SAS 量表，分 4 页展示，每题 1-4 分
-包含 5 道反向计分题（自动处理）
-自动计算总分并给出焦虑等级评估：
  -正常（<50 分） / 轻度焦虑（50-59） / 中度焦虑（60-69） / 重度焦虑（≥70）
-评估结果保存到数据库，支持历史记录查看

### 2.3 放松训练

- **呼吸放松**：4-4-6 呼吸法指导
- **渐进性肌肉放松**：全身逐部位放松指导
- **正念冥想**：专注当下冥想指导
-训练记录保存，个人统计面板

### 2.4 情绪日记

-对话自动生成情绪记录
-日记列表分页浏览
-按日期查看情绪变化

### 2.5 用户系统

-登录/注册/密码修改
-管理员面板：用户管理（查看/启用/禁用/删除）
-统计面板：系统使用数据可视化

---

## 三、项目结构

```
共鸣灵魂主/
├── Resontsoul/
│   ├── app.py                    # 主入口，Gradio 界面定义
│   ├── conf/
│   │   └── service_conf.yaml     # 配置文件（LLM、管理员账号）
│ ├── 静电/
│   │   └── custom.css            # 自定义样式
│   ├── api/
│   │   ├── __init__.py           # 启动引导（bootstrap）
│   │   ├── settings.py           # 全局设置、模型初始化
│   │   ├── constants.py          # 常量定义
│   │   ├── apps/
│ │ ├── __init__.py
│   │   │       ├── conversation_service.py
│   │   │       ├── assessment_service.py
│ │ └── relaxation_service.py
│   │   └── utils/
│   │       ├── __init__.py           # 工具函数（get_base_config 等）
│   │       ├── file_utils.py         # 文件路径工具
│   │       ├── log_utils.py          # 日志工具
│   │       └── t_crypt.py            # AES 加解密
│ ├── 测试/
│   │   ├── test_emotion_app.py
│   │   ├── test_sas_app.py
│   │   └── test_user_service.py
│   ├── .venv/                    # 虚拟环境
│   ├── requirements.txt          # 依赖列表
│   └── pyproject.toml            # 项目配置
└── PROJECT_INTRO.md              # 本文档
```

---

## 四、数据库设计

使用 SQLite 本地数据库，Peewee ORM 管理，包含以下表：

|表名 | 说明 |
|------|------|
| 'user' | 用户信息（用户名、昵称、密码哈希、角色、状态） |
| 'emotion_record' | 情绪记录（时间、情绪标签 JSON、用户输入） |
| 'conversation' | 对话记录（用户输入、AI 回复、时间） |
| “sas_assessment” |SAS 评估记录（总分、各级分数、时间） |
| 'relaxation_record' | 放松训练记录（训练类型、时长、时间） |

---

## 五、配置说明

配置文件位于 'resontsoul/conf/service_conf.yaml'：

```YAML音乐
法学图书馆学：
  model_type：“Qwen/Qwen3-8B” # 模型名称
  model_url： 'https://api.siliconflow.cn/v1' # API 地址
  api_key： 'sk-xxxxxxxx' # API Key（支持明文或 AES 加密）

管理员：
  用户名：'admin' # 管理员用户名
  密码：“admin@123” # 管理员密码
  name_nick： '系统管理员' # 管理员昵称
```

- `api_key' 支持明文直接填写，也支持 AES-256-CBC 加密后的 Base64 编码
- 模型 URL 兼容任意 OpenAI 兼容接口（SiliconFlow、ModelScope、OpenAI 等）

---

## 六、运行方式

### 环境要求

- Python 3.10+
- 虚拟环境（推荐 uv）

### 安装依赖

“砰
CD Resontsoul
PIP install -r requirements.txt
```

### 配置 API Key

编辑 'conf/service_conf.yaml'，填入你的模型 API Key。

### 启动服务

“砰
CD Resontsoul
Python app.py
```

服务默认运行在 'http://localhost:7861'。

### 登录

默认管理员账号：'admin' / 'admin@123'（首次登录后建议修改密码）。

---

## 七、技术架构

```
┌─────────────────────────────────────────┐
│ Gradio 网页界面 │
│ （app.py - 界面定义 + 事件绑定） │
├─────────────────────────────────────────┤
│ API/apps/ （业务逻辑层） │
│对话 |情感 |SAS |用户......│
├─────────────────────────────────────────┤
│ API/db/ （数据持久层） │
│  Peewee ORM + SQLite                    │
├─────────────────────────────────────────┤
│ API/settings.py （模型层） │
│ Camel → OpenAI SDK → LLM API │
└─────────────────────────────────────────┘
```

- **前端**：Gradio 5.x Blocks，自定义 CSS 样式
- **后端**:P ython 模块化架构，api/apps 作为业务逻辑层
- **模型调用**：camel-ai 封装 OpenAI SDK，支持 OpenAI 兼容接口
- **数据存储**:P eewee ORM + SQLite 本地数据库

---

## 八、核心依赖

|依赖 |用途 |版本 |
|------|------|------|
|Gradio |Web UI 框架 |5.38 |
|骆驼爱 |LLM 模型封装 |0.2.72 |
|OpenAI |API 客户端 |1.97 |
|皮维 |ORM 数据库 |3.18 |
|matplotlib |图表生成 |3.10 |
|密码学 |AES 加解密 |45.0 |
|Loguru |日志管理 |0.7.3 |

---

## 九、已知问题与注意事项

1. **代理绕过**：代码中已通过 monkey-patch 强制 httpx 'trust_env=False'，避免系统代理干扰
2. **默认密码**：管理员默认密码 'admin@123'，首次登录后建议立即修改
3. **队列错误**：Gradio 5.x 在沙箱环境中的 WebSocket 队列错误（'ERR_ABORTED queue/data'）不影响核心功能
4. **SAS 计分**：量表包含 5 道反向计分题（第 5、9、13、17、19 题），代码已自动处理
