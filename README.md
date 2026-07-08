# Talent AI System

> 🚀 基于 Ollama + Qwen3 的本地智能简历解析系统

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-green)
![Qwen3](https://img.shields.io/badge/Qwen3-4B-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

# 项目简介

Talent AI System 是一个基于本地大语言模型（LLM）的智能简历解析系统。

系统能够自动读取不同格式的简历（TXT、DOCX、PDF），调用本地部署的 Qwen3 模型提取人才信息，并生成标准 JSON 数据，为后续的人才知识库、招聘管理系统、RAG 检索系统等提供数据基础。

整个系统无需调用 OpenAI API，所有数据均在本地完成处理，更适合企业内网部署及隐私场景。

---

# V1 功能

目前已完成的功能：

- ✅ TXT 简历解析
- ✅ DOCX 简历解析
- ✅ PDF 简历解析
- ✅ 自动识别文件格式
- ✅ 本地 Ollama 调用
- ✅ Qwen3 信息抽取
- ✅ JSON 数据导出

示例输出：

```json
{
    "name":"张伟",
    "school":"上海交通大学",
    "major":"计算机科学与技术",
    "research_direction":"人工智能、机器学习",
    "skills":[
        "Python",
        "PyTorch",
        "深度学习"
    ],
    "papers":"3篇"
}
```

---

# 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.12 | 项目开发 |
| Ollama | 本地模型部署 |
| Qwen3 4B | 大语言模型 |
| PyMuPDF | PDF解析 |
| python-docx | Word解析 |
| SQLAlchemy | 数据库（V2） |
| FastAPI | Web接口（V2） |
| Git | 版本管理 |

---

# 项目结构

```text
talent-ai-system
│
├── app/
│   ├── config.py          # 项目配置
│   ├── parser.py          # 简历解析
│   ├── llm.py             # LLM调用
│   ├── exporter.py        # JSON导出
│   ├── review.py          # 数据检查
│   └── main.py            # 程序入口
│
├── data/
│   ├── resumes/
│   │   ├── test.txt
│   │   ├── test.docx
│   │   └── test.pdf
│   │
│   └── output/
│       └── resume.json
│
├── docs/
│
├── tests/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 项目流程

```text
TXT / DOCX / PDF

        │

        ▼

Parser（解析文本）

        │

        ▼

Qwen3（本地LLM）

        │

        ▼

JSON结构化信息

        │

        ▼

保存到本地（V1）

        │

        ▼

MySQL（V2）
```

---

# 快速开始

## 1. 克隆项目

```bash
git clone https://github.com/你的GitHub用户名/talent-ai-system.git
```

进入项目

```bash
cd talent-ai-system
```

---

## 2. 创建虚拟环境

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. 安装依赖

```bash
pip install -r requirements.txt
```

---

## 4. 安装 Ollama

下载：

https://ollama.com/

安装完成后下载模型：

```bash
ollama pull qwen3:4b
```

启动服务：

```bash
ollama serve
```

---

## 5. 运行项目

```bash
python app/main.py
```

程序会：

1. 自动读取简历
2. 调用本地 Qwen3
3. 提取人才信息
4. 输出 JSON
5. 保存到

```
data/output/resume.json
```

---

# 当前版本

## V1（已完成）

- 多格式简历解析
- 本地大模型抽取
- JSON导出
- Git版本管理

---

## V2（开发计划）

预计新增：

- MySQL 数据库存储
- FastAPI 接口
- 批量简历解析
- 上传接口
- 日志系统
- 配置文件优化

---

## V3（规划）

预计新增：

- RAG 人才知识库
- 向量数据库
- 相似人才搜索
- Agent 工作流
- Web 管理后台
- Docker 部署

---

# 项目特点

- 全程本地运行
- 不依赖 OpenAI API
- 支持多种简历格式
- 模块化设计
- 易于扩展
- 面向企业招聘场景

---

# 开发环境

| 软件 | 版本 |
|------|------|
| Windows | 11 |
| Python | 3.12 |
| Ollama | 0.31.1 |
| Qwen3 | 4B |
| VS Code | Latest |

---

# License

MIT License

---

> 本项目用于学习本地大模型应用开发、人才信息抽取及企业级 AI 系统设计，后续将持续迭代完善。