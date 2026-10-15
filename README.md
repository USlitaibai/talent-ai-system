# Talent AI System

> 🚀 基于本地大模型（Ollama + Qwen3）与向量检索的**智能人才知识库系统**

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.139-009688)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-green)
![Qwen3](https://img.shields.io/badge/Qwen3-4B-orange)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Store-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 项目简介

Talent AI System 是一个面向企业招聘场景的本地化 AI 系统。

系统自动读取简历与岗位 JD（TXT / DOCX / PDF，支持 ZIP 批量导入），调用本地部署的
Qwen3 模型抽取结构化人才信息，写入 MySQL 与 FAISS 向量库，并提供：

- **RAG 知识库问答**：双路检索 + 重排，回答"谁熟悉 Python"这类人才查询
- **简历 × 岗位智能匹配**：技能 / 专业 / 学历加权评分
- **人才数据分析**：Dashboard、人才画像、图表数据和完整分析报告
- **人工审核**：HR 修改简历后自动同步知识库
- **数据导出**：一键导出 Excel 人才表

**全程本地运行，不调用任何外部大模型 API**，数据不出内网，适合隐私敏感的招聘场景。

---

## 已实现功能

### 1. 简历解析与入库

| 功能 | 说明 |
|------|------|
| 多格式解析 | TXT / DOCX / PDF，自动识别后缀（PyMuPDF + python-docx） |
| AI 信息抽取 | Qwen3 抽取：姓名、学校、专业、研究方向、技能、论文 |
| 单份上传 | `POST /resume/upload` |
| 多文件批量上传 | `POST /resume/batch-upload`，同名文件自动重命名 |
| ZIP 异步导入 | `POST /resume/zip-upload`，后台任务 + 进度轮询，递归扫描目录 |
| 重复检测 | 按「姓名 + 学校 + 专业」去重 |
| 自动入库 | 结构化数据写入 MySQL，同时生成知识文本写入向量库 |

### 2. 知识库 / RAG 问答

| 功能 | 说明 |
|------|------|
| 文本向量化 | Ollama `nomic-embed-text`（768 维） |
| 向量库 | FAISS `IndexFlatL2` + JSON 元数据，落盘到 `data/vectors/` |
| 关键词检索 | BM25 + jieba 中文分词 |
| 混合检索 | FAISS 与 BM25 各取 `max(top_k*4, 10)` → 合并去重 → 重排 |
| 二次重排 | `BAAI/bge-reranker-v2-m3` CrossEncoder 精排 |
| 上下文压缩 | 去重 + 截断至 8 行，控制 Prompt 体积 |
| 双层缓存 | L1 精确缓存（LRU 100）+ L2 语义缓存（余弦阈值 0.85） |
| 防幻觉 Prompt | 强制"仅依据知识回答"，知识不足时固定回答"知识库中暂无相关信息。" |

### 3. 岗位 JD

上传 JD（TXT / DOCX / PDF）→ AI 抽取 9 个字段（岗位、公司、学历、专业、经验、
技能、薪资、城市、描述）→ 去重入库 → 自动写入知识库。支持列表与详情查询。

### 4. 人才检索与匹配

| 功能 | 说明 |
|------|------|
| 关键词搜索 | 姓名 / 学校 / 专业 / 研究方向 / 技能 / 论文 六字段模糊匹配 |
| 人才排序 | 按技能交集比例对候选人降序排名 |
| AI 推荐报告 | 针对「简历 + 岗位」生成优势、劣势、总结与推荐结论 |
| 简历×岗位匹配 | 技能 70% + 专业 20% + 学历 10% 加权评分，附缺失技能提示 |

### 5. 数据分析

- **Dashboard**：简历数 / 岗位数 + Top 学校 / 专业 / 技能 / 公司 / 岗位 / 城市
- **人才画像**：最高频学校、专业、技能、公司、岗位
- **统计分析**：学校、专业、技能、研究方向、公司、岗位、城市、
  学历分布、薪资分布、岗位技能分布
- **完整报告**：`generated_at` + dashboard + summary + profile + charts + AI 摘要

### 6. 人工审核

简历列表 / 详情 / 修改 / 删除 / 计数。**修改或删除简历时自动同步向量库**，
保证知识库与数据库一致。

### 7. 数据导出

一键导出 Excel（openpyxl），支持导出全部或按 ID 导出指定简历，带表头样式与列宽。

### 8. 系统与运维

- **用户系统**：注册 / 登录 / 查询，密码 bcrypt 哈希，JWT（HS256，24 小时）鉴权
- **统一响应**：`{code, message, data}` 全局一致
- **日志**：控制台 + `app.log`（5MB × 5 轮转）+ `error.log`（仅 ERROR）
- **指标埋点**：LLM / Embedding 调用次数与耗时、缓存命中率、RAG 耗时
- **自动建表**：启动时 `Base.metadata.create_all()`

---

## 系统架构

### 分层结构

```
                    接入层   app/server.py  (FastAPI，/docs 自动生成)
                                  │  统一响应 app/common/response.py
   ┌────────┬────────┬─────────┬──┴──────┬─────────┬────────┬────────┐
 Resume    Talent     JD     Knowledge  Analysis  Review   Export   System
 简历域    人才域    岗位域   知识/RAG域   分析域    审核域   导出域   用户域
   └────────┴────────┴─────────┴─────────┴─────────┴────────┴────────┘
        API  →  Service  →  Repository  →  Model / 向量库     （各域四层同构）
   ┌──────────────────────────────────────────────────────────────┐
   │ 共享底座 core：config(.env) · database(MySQL) · logger(轮转)   │
   │ 共享能力 ai ：llm · prompt · parser · cache · reranker        │
   └──────────────────────────────────────────────────────────────┘
   存储：MySQL(resume/job/user) + FAISS(data/vectors) + 内存缓存/任务表
```

### 四条核心数据流

**① 简历入库**

```
TXT/DOCX/PDF/ZIP
      │  Parser 解析文本
      ▼
Qwen3 结构化抽取 → 重复检测 → MySQL
      │
      ▼  拼接知识文本
Embedding(768维) → FAISS + 元数据
```

**② RAG 问答**

```
用户问题
   │
   ├─→ L1 精确缓存 ──命中──→ 直接返回
   ▼
Embedding
   │
   ├─→ L2 语义缓存(余弦≥0.85) ──命中──→ 直接返回
   ▼
FAISS 检索 ⊕ BM25 检索 → 合并去重 → CrossEncoder 重排 → 上下文压缩
   │
   ▼
防幻觉 Prompt → Qwen3 → 答案 → 回写 L1 + L2 缓存
```

**③ 简历 × 岗位匹配**

```
resume_id + job_id
      │
      ├─ 技能匹配（70%）
      ├─ 专业匹配（20%）
      └─ 学历匹配（10%）
      ▼
加权评分 + 分档摘要 + 缺失技能提示
```

**④ 人工审核联动**

```
HR 修改简历 → 更新 MySQL → 重建知识文本 → 定位向量条目 → 更新向量库
HR 删除简历 → 删除 MySQL → 定位向量条目 → 删除向量库
```

---

## 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.12 | 项目开发 |
| FastAPI + Uvicorn | Web 接口与 ASGI 服务 |
| SQLAlchemy 2.0 | ORM / 数据访问 |
| MySQL | 结构化数据存储 |
| Ollama | 本地大模型运行时 |
| Qwen3 4B | 信息抽取与 RAG 生成 |
| nomic-embed-text | 文本向量化（768 维） |
| FAISS | 本地向量数据库 |
| BM25 (rank-bm25) + jieba | 中文关键词检索 |
| sentence-transformers | CrossEncoder 重排 |
| PyMuPDF / python-docx | PDF / DOCX 解析 |
| openpyxl | Excel 导出 |
| JWT (python-jose) + passlib | 认证与密码哈希 |
| python-dotenv | 环境变量配置 |
| Docker + Docker Compose | 一键部署（MySQL + Ollama + 应用） |

---

## 项目结构

```
talent-ai-system
│
├── app/
│   ├── server.py            # 唯一启动入口，注册所有 Router
│   ├── create_tables.py     # 手动建表脚本
│   │
│   ├── core/                # 共享底座
│   │   ├── config.py        # 统一配置（读取 .env）
│   │   ├── database.py      # MySQL 引擎与会话
│   │   └── logger.py        # 日志（轮转 + 错误单独文件）
│   │
│   ├── common/
│   │   └── response.py      # 统一 API 返回格式
│   │
│   ├── models/              # ORM 模型
│   │   ├── resume.py        # 简历表
│   │   ├── jd.py            # 岗位表
│   │   └── user.py          # 用户表
│   │
│   ├── ai/                  # 共享 AI 能力
│   │   ├── llm.py           # Ollama 调用与抽取
│   │   ├── prompt.py        # Prompt 模板
│   │   ├── parser.py        # AI 返回 JSON 清洗解析
│   │   ├── cache.py         # 双层缓存（L1 + 语义）
│   │   └── reranker.py      # CrossEncoder 重排
│   │
│   ├── resume/              # 简历域
│   │   ├── api.py           # 上传 / 批量 / ZIP / 列表 / 详情
│   │   ├── service.py       # 业务编排
│   │   ├── parser.py        # 三格式解析
│   │   ├── repository.py    # 简历数据访问
│   │   ├── zip_import.py    # ZIP 解压与扫描
│   │   ├── tagger.py        # 技能标签规则
│   │   └── batch_parser.py  # 目录级批处理
│   │
│   ├── jd/                  # 岗位域
│   │   ├── api.py  service.py  parser.py  repository.py  schema.py
│   │
│   ├── knowledge/           # 知识库 / RAG 域
│   │   ├── api.py           # 增删查 / 问答 / 计数
│   │   ├── service.py       # RAG 主流程
│   │   ├── vector_store.py  # FAISS 向量库
│   │   ├── embedding.py     # 向量化
│   │   ├── bm25.py          # BM25 检索
│   │   ├── hybrid.py        # 混合检索
│   │   ├── retriever.py     # 检索入口
│   │   ├── compressor.py    # 上下文压缩
│   │   ├── repository.py    # 知识数据访问
│   │   └── schema.py
│   │
│   ├── talent/              # 人才域
│   │   ├── api.py  service.py  search.py  ranking.py
│   │   ├── matcher.py  recommender.py  filter.py
│   │   └── favorite.py  interview.py  offer.py
│   │
│   ├── analysis/            # 分析域
│   │   ├── api.py  service.py  analysis.py
│   │   ├── dashboard.py  statistics.py  matcher.py
│   │   ├── report.py
│   │
│   ├── review/              # 人工审核域
│   │   ├── api.py  service.py  repository.py  schema.py  review.py
│   │
│   ├── export/              # 导出域
│   │   ├── api.py  service.py  excel.py  pdf.py  word.py
│   │
│   └── system/              # 用户域
│       ├── api.py  service.py  repository.py  schema.py
│       ├── auth.py          # JWT + 密码哈希
│       ├── user.py          # 当前用户依赖
│       └── metrics.py       # 运行指标
│
├── data/
│   ├── resumes/             # 测试简历
│   ├── uploads/             # 上传文件
│   ├── output/              # 导出的 Excel
│   └── vectors/             # FAISS 索引 + 元数据
│
├── app/logs/                # 运行日志
├── docker/                  # Docker 运行期数据（卷挂载）
├── scripts/init_db.py       # 数据库初始化
├── Dockerfile               # 应用镜像
├── docker-compose.yml       # 三服务编排
├── .dockerignore            # 构建上下文排除（关键：排除 venv）
├── .env.example             # 环境变量模板
├── requirements.txt
└── README.md
```

---

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/USlitaibai/talent-ai-system.git
cd talent-ai-system
```

### 2. 创建虚拟环境

Windows：

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS：

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 安装并启动 Ollama

下载安装：https://ollama.com/

```bash
ollama pull qwen3:4b
ollama pull nomic-embed-text
ollama serve
```

### 5. 配置数据库

创建数据库：

```sql
CREATE DATABASE talent_ai_system DEFAULT CHARSET utf8mb4;
```

在项目根目录创建 `.env`：

```ini
# ==========================
# MySQL
# ==========================
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=你的密码
DB_NAME=talent_ai_system

# ==========================
# Ollama
# ==========================
OLLAMA_MODEL=qwen3:4b
OLLAMA_EMBED_MODEL=nomic-embed-text:latest

# ==========================
# 可选：开发时回显 SQL
# ==========================
DEBUG_SQL=false
```

### 6. 初始化数据库表

```bash
python -m scripts.init_db
```

也可以直接启动服务，`app/server.py` 会自动建表。

### 7. 启动服务

```bash
python app/server.py
```

服务地址：

- 接口文档（Swagger UI）：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/

> ⚠️ 重排模型 `BAAI/bge-reranker-v2-m3`（约 2GB）采用**懒加载**：
> 服务启动本身只需几秒，只有**首次调用检索/问答**时才加载模型，
> 此时会从 HuggingFace 下载，请保证网络可用；之后走本地缓存。
> 若不想下载该模型，可在 `.env` 中设置 `RERANK_ENABLED=false`，
> 系统会自动改用 RRF 排名融合兜底。

### 8. 快速验证

```bash
# 上传一份简历
curl -X POST http://127.0.0.1:8000/resume/upload -F "file=@resume.pdf"

# 看简历列表
curl http://127.0.0.1:8000/resume/

# 知识库问答
curl -X POST "http://127.0.0.1:8000/knowledge/chat?question=谁熟悉Python开发？"

# 人才统计
curl http://127.0.0.1:8000/analysis/dashboard
```

---

## Docker 部署（推荐）

不想手动装 MySQL 和 Ollama？用 Docker Compose 一条命令拉起整套系统。

### 前置要求

- 安装 [Docker Desktop](https://www.docker.com/products/docker-desktop/)（Windows / macOS）
- 建议预留 **10GB 以上磁盘空间**（镜像 + MySQL 数据 + Ollama 模型）

### 一键启动

```bash
docker compose up -d
```

这会启动三个服务：

| 服务 | 说明 | 宿主机端口 |
|------|------|-----------|
| `mysql` | 数据库，数据持久化在命名卷 `mysql_data` | **3307** → 容器内 3306 |
| `ollama` | 本地大模型服务，模型持久化在 `ollama_data` | 11434 |
| `app` | 本系统，依赖前两者就绪后启动 | 8000 |

> ⚠️ **为什么 MySQL 映射到 3307 而不是 3306？**
> 很多开发者本机已安装 MySQL 并占用 3306，直接映射会导致
> `bind: Only one usage of each socket address` 启动失败。
> 因此默认改用 3307，容器内部始终是 3306，应用通过服务名
> `mysql` 连接，完全不受影响。
> 如需修改，在 `.env` 中设置 `DB_HOST_PORT=xxxx`。

### 初始化（拉取模型，只需一次）

镜像已就绪，但**容器内的 Ollama 需要拉取模型**（约 2.4GB）：

```bash
# Linux / macOS
bash scripts/docker-init.sh

# Windows PowerShell
powershell -ExecutionPolicy Bypass -File scripts\docker-init.ps1
```

脚本会依次等待服务就绪、拉取 `nomic-embed-text` 与 `qwen3:4b`、
并做健康检查。也可以手动执行：

```bash
docker compose exec ollama ollama pull nomic-embed-text
docker compose exec ollama ollama pull qwen3:4b
```

### 访问

- 接口文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/

### 常用命令

```bash
docker compose ps          # 查看状态
docker compose logs -f app # 查看应用日志
docker compose down        # 停止（保留数据）
docker compose down -v     # 停止并删除数据卷
```

### 关于重排模型

容器中默认设置 `RERANK_ENABLED=false`，**不加载** CrossEncoder 重排模型，
改用 **RRF（Reciprocal Rank Fusion）排名融合**兜底：

- 优点：无需下载约 2GB 模型，服务秒级启动，镜像更可控
- 代价：精排效果略降

想启用完整精排，改 `docker-compose.yml` 中：

```yaml
RERANK_ENABLED: "true"
```

首次检索时会自动下载模型（约 2GB），之后缓存在容器内。

### 说明

- 镜像基于 `python:3.12-slim`，但依赖中含 `torch` / `sentence-transformers`，
  因此**首次构建较慢、镜像较大**（实测约 **9.4GB**，含 Linux 版 CUDA 运行时），
  属预期现象；关闭 `RERANK_ENABLED` 不会减小镜像，因为 `torch`
  是 `requirements.txt` 中的固定依赖
- 向量库已预置于 `docker/vectors/`，容器启动即有知识可检索；
  该目录以卷挂载，新增知识会持久化到宿主机
- 若只想改代码快速验证，仍推荐本地方式（上文步骤 1~8）

---

## API 一览

共 35 个接口，全部可在 `/docs` 中交互调试。

### 简历 `/resume`

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/resume/upload` | 上传单份简历 |
| POST | `/resume/batch-upload` | 批量上传多份简历 |
| POST | `/resume/zip-upload` | ZIP 批量导入（异步，返回 task_id） |
| GET | `/resume/import-status/{task_id}` | 查询导入进度与结果 |
| GET | `/resume/import-tasks` | 查看所有导入任务 |
| GET | `/resume/` | 简历列表 |
| GET | `/resume/{resume_id}` | 简历详情 |

### 岗位 `/jd`

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/jd/upload` | 上传 JD 并 AI 解析入库 |
| GET | `/jd/` | 岗位列表 |
| GET | `/jd/{job_id}` | 岗位详情 |

### 知识库 `/knowledge`

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/knowledge/add` | 新增知识 |
| GET | `/knowledge/search` | 混合检索（FAISS + BM25 + 重排） |
| POST | `/knowledge/chat` | RAG 问答 |
| DELETE | `/knowledge/delete/{knowledge_id}` | 删除知识 |
| GET | `/knowledge/count` | 知识数量 |

### 人才 `/talent`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/talent/search` | 关键词搜索人才 |
| POST | `/talent/ranking` | 按岗位要求排序人才 |
| POST | `/talent/recommend` | 生成 AI 推荐报告 |

### 分析 `/analysis`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/analysis/dashboard` | Dashboard 数据 |
| GET | `/analysis/summary` | 首页摘要 |
| GET | `/analysis/profile` | 人才画像 |
| GET | `/analysis/chart` | 图表数据 |
| GET | `/analysis/report` | 完整分析报告 |
| POST | `/analysis/match` | 简历 × 岗位匹配 |

### 审核 `/review`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/review/list` | 待审核简历列表 |
| GET | `/review/count` | 简历数量 |
| GET | `/review/{resume_id}` | 简历详情 |
| PUT | `/review/{resume_id}` | 修改简历（自动同步知识库） |
| DELETE | `/review/{resume_id}` | 删除简历（自动同步知识库） |

### 导出 `/export`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/export/excel` | 导出 Excel（可传 `ids` 指定简历） |

### 用户 `/system`

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/system/register` | 注册 |
| POST | `/system/login` | 登录，返回 JWT |
| GET | `/system/users` | 用户列表（需登录） |
| GET | `/system/users/{user_id}` | 用户详情（需登录） |

---

## 关键设计说明

**为什么用「向量 + 关键词」双路检索？**
纯向量检索对「Python」「FastAPI」这类专有名词的精确匹配不够稳，纯关键词又抓不住
语义相近的表达。两路各取候选后合并去重，再用 CrossEncoder 精排，召回和准确率都更好。

**为什么要做两层缓存？**
「谁熟悉 Python」和「谁会 Python 开发」语义相同但字面不同。L1 精确缓存拦重复提问，
L2 语义缓存（余弦 ≥ 0.85）拦换句话问同一件事的情况，能显著减少 LLM 调用。

**为什么加防幻觉 Prompt？**
RAG 最大的风险是模型在知识不足时编造答案。Prompt 中强制"只能依据知识回答"，
并在上下文为空时直接返回固定话术，不走 LLM。

**重排模型什么时候加载？**
采用懒加载：进程启动时不加载（启动仅需数秒），首次调用检索时才加载并常驻。
模型不可用时会自动降级为 RRF 排名融合，保证检索功能不中断。

---

## 当前进度与已知限制

项目仍在迭代中，以下为当前状态，便于后续开发对照：

**待改进**

- `data/vectors/resume.metadata.json` 中存在早期版本写入的历史条目
  （缺少 `id` / `resume_id` 字段），当前代码已能自动回填兼容，
  如需干净数据可删除该文件后重新导入简历
- 上传接口尚未限制文件体积与解压规模，生产环境需补充校验
- JWT 密钥目前写在代码中，生产环境应改为读取环境变量
- 除 `/system/users` 外，其余业务接口暂未挂鉴权
- 依赖中含 `torch` / `sentence-transformers`，导致镜像与安装体积较大；
  若关闭 `RERANK_ENABLED` 可省去这部分依赖（需自行精简 requirements）
- 尚缺少单元测试

**规划中**

- 人才流程：收藏 / 面试 / Offer 状态机（已有模块骨架，待接入数据库与接口）
- 岗位与简历的向量化匹配（当前匹配为规则加权评分）
- 技能标签自动生成接入主流程（`talent/tagger` 规则已就绪）
- RAG 召回效果评估脚本
- Web 管理后台

**已完成**

- ✅ Docker Compose 一键部署（MySQL + Ollama + 应用）

---

## 开发环境

| 软件 | 版本 |
|------|------|
| Windows | 11 |
| Python | 3.12 |
| MySQL | 8.x |
| Ollama | 0.31.1 |
| Qwen3 | 4B |
| VS Code | Latest |

---

## License

MIT License

---

> 本项目用于学习本地大模型应用开发、RAG 系统工程化及企业级 AI 系统设计，将持续迭代完善。
