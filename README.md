<div align="center">

# 📚 DocSyncForge

**智能文档同步引擎 | Lightweight Intelligent Documentation Sync Engine**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Zero%20Dependencies-✓-brightgreen.svg)](#)
[![GitHub Stars](https://img.shields.io/github/stars/gitstq/DocSyncForge?style=social)](https://github.com/gitstq/DocSyncForge)

<p align="center">
  <a href="#简体中文">简体中文</a> •
  <a href="#繁體中文">繁體中文</a> •
  <a href="#english">English</a>
</p>

</div>

---

<a name="简体中文"></a>
## 🎉 项目介绍

**DocSyncForge** 是一款轻量级智能文档同步引擎，专为解决开发者「代码更新了，文档却滞后」的痛点而设计。

### 💡 灵感来源

在日常开发中，我们经常面临这样的困扰：
- 代码已经迭代了多个版本，API文档还是旧的
- 新功能上线很久，使用文档却没有同步更新
- 多人协作时，文档散落在各个平台，难以统一管理

DocSyncForge 通过**自动检测代码变更** → **智能分析影响范围** → **生成文档更新建议** → **多平台同步发布**的完整工作流，让文档维护变得轻松高效。

### ✨ 核心特性

| 特性 | 描述 | 状态 |
|------|------|------|
| 🔍 **智能变更检测** | 基于Git diff自动识别代码变更，支持多语言解析 | ✅ |
| 🧠 **AST代码分析** | 解析Python/JavaScript/TypeScript/Java/Go/Rust代码结构 | ✅ |
| 📝 **文档生成建议** | 自动为新函数/类生成文档模板 | ✅ |
| 🔄 **多平台同步** | 支持GitHub Wiki、ReadTheDocs、Notion、Confluence | 🚧 |
| 📊 **同步报告** | 生成详细的Markdown格式同步报告 | ✅ |
| 🎯 **零依赖核心** | 核心功能仅使用Python标准库 | ✅ |
| 🖥️ **精美TUI** | 终端交互界面，操作直观便捷 | ✅ |
| ⚙️ **灵活配置** | JSON配置文件，自定义同步规则 | ✅ |

### 🚀 快速开始

#### 环境要求

- Python 3.8 或更高版本
- Git 仓库（用于变更检测）

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/DocSyncForge.git
cd DocSyncForge

# 直接运行（零依赖）
python docsyncforge.py --help

# 或安装可选依赖（推荐）
pip install -r requirements.txt
```

#### 基础用法

```bash
# 初始化配置文件
python docsyncforge.py init

# 扫描代码变更
python docsyncforge.py scan

# 生成同步报告
python docsyncforge.py report

# 分析特定文件
python docsyncforge.py analyze src/main.py
```

### 📖 详细使用指南

#### 1️⃣ 初始化项目

```bash
python docsyncforge.py init
```

这会创建一个 `.docsyncforge.json` 配置文件：

```json
{
  "source_dirs": ["src", "lib", "app"],
  "doc_dirs": ["docs", "README.md"],
  "ignore_patterns": ["*.pyc", "node_modules/*", ".git/*"],
  "watch_extensions": [".py", ".js", ".ts", ".java", ".go", ".rs"],
  "sync_targets": ["local"],
  "auto_sync": false
}
```

#### 2️⃣ 扫描代码变更

```bash
# 扫描最近1次提交的变更
python docsyncforge.py scan

# 扫描最近5次提交
python docsyncforge.py scan --since HEAD~5

# 导出JSON格式结果
python docsyncforge.py scan --output changes.json
```

#### 3️⃣ 生成同步报告

```bash
python docsyncforge.py report --output sync-report.md
```

报告示例：

```markdown
# DocSyncForge 同步报告

**生成时间**: 2025-01-09T10:30:00
**总变更数**: 3
**需处理变更**: 2

## 变更文件列表

- ➕ `src/auth.py` (added)
- ✏️ `src/utils.py` (modified)

## 文档更新建议

### 新增函数: authenticate_user

**来源文件**: `src/auth.py`

建议添加以下文档：
```python
def authenticate_user(username: str, password: str) -> bool:
    """
    验证用户凭据
    
    Args:
        username: 用户名
        password: 密码
        
    Returns:
        验证成功返回True，否则返回False
    """
```
```

#### 4️⃣ 代码分析

```bash
python docsyncforge.py analyze src/main.py
```

输出示例：

```
语言: python
总行数: 156

函数 (8):
  • main
  • setup_config
  • process_data
  ...

类 (2):
  • DataProcessor
  • ConfigManager
```

### 💡 设计思路与迭代规划

#### 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                    DocSyncForge 架构                        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Git变更检测  │→│ AST代码分析  │→│ 文档生成器   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↓                 ↓                 ↓               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              文档同步引擎 (DocSyncEngine)            │   │
│  └─────────────────────────────────────────────────────┘   │
│         ↓                 ↓                 ↓               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ GitHub Wiki  │  │ ReadTheDocs  │  │   Notion     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

#### 技术选型原因

- **纯Python实现**：无需额外运行时，部署简单
- **零依赖核心**：降低安装门槛，避免依赖冲突
- **正则AST解析**：轻量级代码分析，无需复杂解析器
- **Git原生集成**：直接读取Git历史，准确追踪变更

#### 后续迭代计划

- [ ] v1.1.0 - 支持更多编程语言（C/C++、C#、PHP）
- [ ] v1.2.0 - 集成LLM API，智能生成文档内容
- [ ] v1.3.0 - 多平台同步功能（Notion、Confluence）
- [ ] v1.4.0 - Web界面，可视化配置与管理
- [ ] v2.0.0 - CI/CD插件，自动化文档流水线

### 📦 打包与部署

#### 作为命令行工具使用

```bash
# 添加到PATH
chmod +x docsyncforge.py
sudo ln -s $(pwd)/docsyncforge.py /usr/local/bin/docsyncforge

# 全局使用
docsyncforge --help
docsyncforge scan
docsyncforge report
```

#### 作为Python模块导入

```python
from docsyncforge import DocSyncEngine, SyncConfig

# 创建引擎实例
engine = DocSyncEngine()

# 扫描变更
result = engine.scan_changes()

# 生成报告
report = engine.generate_report()
```

### 🤝 贡献指南

我们欢迎所有形式的贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

<a name="繁體中文"></a>
## 🎉 專案介紹

**DocSyncForge** 是一款輕量級智能文件同步引擎，專為解決開發者「程式碼更新了，文件卻滯後」的痛點而設計。

### 💡 靈感來源

在日常開發中，我們經常面臨這樣的困擾：
- 程式碼已經迭代了多個版本，API文件還是舊的
- 新功能上線很久，使用文件卻沒有同步更新
- 多人協作時，文件散落在各個平台，難以統一管理

DocSyncForge 透過**自動檢測程式碼變更** → **智能分析影響範圍** → **生成文件更新建議** → **多平台同步發布**的完整工作流，讓文件維護變得輕鬆高效。

### ✨ 核心特性

| 特性 | 描述 | 狀態 |
|------|------|------|
| 🔍 **智能變更檢測** | 基於Git diff自動識別程式碼變更，支援多語言解析 | ✅ |
| 🧠 **AST程式碼分析** | 解析Python/JavaScript/TypeScript/Java/Go/Rust程式碼結構 | ✅ |
| 📝 **文件生成建議** | 自動為新函數/類別生成文件範本 | ✅ |
| 🔄 **多平台同步** | 支援GitHub Wiki、ReadTheDocs、Notion、Confluence | 🚧 |
| 📊 **同步報告** | 生成詳細的Markdown格式同步報告 | ✅ |
| 🎯 **零依賴核心** | 核心功能僅使用Python標準函式庫 | ✅ |
| 🖥️ **精美TUI** | 終端機互動介面，操作直觀便捷 | ✅ |
| ⚙️ **靈活配置** | JSON設定檔，自定義同步規則 | ✅ |

### 🚀 快速開始

#### 環境要求

- Python 3.8 或更高版本
- Git 儲存庫（用於變更檢測）

#### 安裝

```bash
# 複製儲存庫
git clone https://github.com/gitstq/DocSyncForge.git
cd DocSyncForge

# 直接執行（零依賴）
python docsyncforge.py --help

# 或安裝選用依賴（推薦）
pip install -r requirements.txt
```

#### 基礎用法

```bash
# 初始化設定檔
python docsyncforge.py init

# 掃描程式碼變更
python docsyncforge.py scan

# 生成同步報告
python docsyncforge.py report

# 分析特定檔案
python docsyncforge.py analyze src/main.py
```

### 📖 詳細使用指南

#### 1️⃣ 初始化專案

```bash
python docsyncforge.py init
```

這會建立一個 `.docsyncforge.json` 設定檔：

```json
{
  "source_dirs": ["src", "lib", "app"],
  "doc_dirs": ["docs", "README.md"],
  "ignore_patterns": ["*.pyc", "node_modules/*", ".git/*"],
  "watch_extensions": [".py", ".js", ".ts", ".java", ".go", ".rs"],
  "sync_targets": ["local"],
  "auto_sync": false
}
```

#### 2️⃣ 掃描程式碼變更

```bash
# 掃描最近1次提交的變更
python docsyncforge.py scan

# 掃描最近5次提交
python docsyncforge.py scan --since HEAD~5

# 匯出JSON格式結果
python docsyncforge.py scan --output changes.json
```

#### 3️⃣ 生成同步報告

```bash
python docsyncforge.py report --output sync-report.md
```

#### 4️⃣ 程式碼分析

```bash
python docsyncforge.py analyze src/main.py
```

### 💡 設計思路與迭代規劃

#### 架構設計

```
┌─────────────────────────────────────────────────────────────┐
│                    DocSyncForge 架構                        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Git變更檢測  │→│ AST程式碼分析│→│ 文件生成器   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↓                 ↓                 ↓               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              文件同步引擎 (DocSyncEngine)            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

#### 技術選型原因

- **純Python實作**：無需額外執行環境，部署簡單
- **零依賴核心**：降低安裝門檻，避免依賴衝突
- **正規表示式AST解析**：輕量級程式碼分析，無需複雜解析器
- **Git原生整合**：直接讀取Git歷史，準確追蹤變更

#### 後續迭代計畫

- [ ] v1.1.0 - 支援更多程式語言（C/C++、C#、PHP）
- [ ] v1.2.0 - 整合LLM API，智能生成文件內容
- [ ] v1.3.0 - 多平台同步功能（Notion、Confluence）
- [ ] v1.4.0 - Web介面，視覺化配置與管理
- [ ] v2.0.0 - CI/CD外掛，自動化文件流水線

### 📦 打包與部署

#### 作為命令列工具使用

```bash
# 新增到PATH
chmod +x docsyncforge.py
sudo ln -s $(pwd)/docsyncforge.py /usr/local/bin/docsyncforge

# 全域使用
docsyncforge --help
docsyncforge scan
docsyncforge report
```

### 🤝 貢獻指南

我們歡迎所有形式的貢獻！請參閱 [CONTRIBUTING.md](CONTRIBUTING.md) 了解詳情。

### 📄 開源協議

本專案採用 [MIT License](LICENSE) 開源協議。

---

<a name="english"></a>
## 🎉 Introduction

**DocSyncForge** is a lightweight intelligent documentation synchronization engine designed to solve the pain point of "code updated, but documentation lagging behind" for developers.

### 💡 Inspiration

In daily development, we often face these challenges:
- Code has iterated through multiple versions, but API documentation remains outdated
- New features have been deployed for a while, but user documentation hasn't been updated
- In collaborative environments, documentation is scattered across various platforms, making unified management difficult

DocSyncForge makes documentation maintenance easy and efficient through a complete workflow of **automatic code change detection** → **intelligent impact analysis** → **documentation update suggestions** → **multi-platform synchronization**.

### ✨ Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| 🔍 **Smart Change Detection** | Automatically identify code changes based on Git diff, supporting multiple languages | ✅ |
| 🧠 **AST Code Analysis** | Parse Python/JavaScript/TypeScript/Java/Go/Rust code structures | ✅ |
| 📝 **Doc Generation Suggestions** | Automatically generate documentation templates for new functions/classes | ✅ |
| 🔄 **Multi-Platform Sync** | Support GitHub Wiki, ReadTheDocs, Notion, Confluence | 🚧 |
| 📊 **Sync Reports** | Generate detailed Markdown format synchronization reports | ✅ |
| 🎯 **Zero Dependencies Core** | Core functionality uses only Python standard library | ✅ |
| 🖥️ **Beautiful TUI** | Terminal interactive interface with intuitive operations | ✅ |
| ⚙️ **Flexible Configuration** | JSON configuration file for custom sync rules | ✅ |

### 🚀 Quick Start

#### Requirements

- Python 3.8 or higher
- Git repository (for change detection)

#### Installation

```bash
# Clone repository
git clone https://github.com/gitstq/DocSyncForge.git
cd DocSyncForge

# Run directly (zero dependencies)
python docsyncforge.py --help

# Or install optional dependencies (recommended)
pip install -r requirements.txt
```

#### Basic Usage

```bash
# Initialize configuration file
python docsyncforge.py init

# Scan code changes
python docsyncforge.py scan

# Generate sync report
python docsyncforge.py report

# Analyze specific file
python docsyncforge.py analyze src/main.py
```

### 📖 Detailed Usage Guide

#### 1️⃣ Initialize Project

```bash
python docsyncforge.py init
```

This creates a `.docsyncforge.json` configuration file:

```json
{
  "source_dirs": ["src", "lib", "app"],
  "doc_dirs": ["docs", "README.md"],
  "ignore_patterns": ["*.pyc", "node_modules/*", ".git/*"],
  "watch_extensions": [".py", ".js", ".ts", ".java", ".go", ".rs"],
  "sync_targets": ["local"],
  "auto_sync": false
}
```

#### 2️⃣ Scan Code Changes

```bash
# Scan changes from last commit
python docsyncforge.py scan

# Scan last 5 commits
python docsyncforge.py scan --since HEAD~5

# Export JSON format results
python docsyncforge.py scan --output changes.json
```

#### 3️⃣ Generate Sync Report

```bash
python docsyncforge.py report --output sync-report.md
```

Report example:

```markdown
# DocSyncForge Sync Report

**Generated**: 2025-01-09T10:30:00
**Total Changes**: 3
**Changes to Process**: 2

## Changed Files

- ➕ `src/auth.py` (added)
- ✏️ `src/utils.py` (modified)

## Documentation Update Suggestions

### New Function: authenticate_user

**Source File**: `src/auth.py`

Suggested documentation:
```python
def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate user credentials
    
    Args:
        username: User name
        password: Password
        
    Returns:
        True if authentication succeeds, False otherwise
    """
```
```

#### 4️⃣ Code Analysis

```bash
python docsyncforge.py analyze src/main.py
```

Example output:

```
Language: python
Total Lines: 156

Functions (8):
  • main
  • setup_config
  • process_data
  ...

Classes (2):
  • DataProcessor
  • ConfigManager
```

### 💡 Design Philosophy & Roadmap

#### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DocSyncForge Architecture                │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Git Change   │→│ AST Code     │→│ Document     │      │
│  │ Detection    │  │ Analysis     │  │ Generator    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↓                 ↓                 ↓               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              DocSyncEngine                          │   │
│  └─────────────────────────────────────────────────────┘   │
│         ↓                 ↓                 ↓               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ GitHub Wiki  │  │ ReadTheDocs  │  │   Notion     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

#### Technical Choices

- **Pure Python Implementation**: No additional runtime required, easy deployment
- **Zero Dependencies Core**: Lower installation barrier, avoid dependency conflicts
- **Regex-based AST Parsing**: Lightweight code analysis without complex parsers
- **Native Git Integration**: Direct Git history access for accurate change tracking

#### Roadmap

- [ ] v1.1.0 - Support more programming languages (C/C++, C#, PHP)
- [ ] v1.2.0 - Integrate LLM API for intelligent document content generation
- [ ] v1.3.0 - Multi-platform sync functionality (Notion, Confluence)
- [ ] v1.4.0 - Web interface for visual configuration and management
- [ ] v2.0.0 - CI/CD plugin for automated documentation pipeline

### 📦 Packaging & Deployment

#### Use as CLI Tool

```bash
# Add to PATH
chmod +x docsyncforge.py
sudo ln -s $(pwd)/docsyncforge.py /usr/local/bin/docsyncforge

# Use globally
docsyncforge --help
docsyncforge scan
docsyncforge report
```

#### Import as Python Module

```python
from docsyncforge import DocSyncEngine, SyncConfig

# Create engine instance
engine = DocSyncEngine()

# Scan changes
result = engine.scan_changes()

# Generate report
report = engine.generate_report()
```

### 🤝 Contributing

We welcome all forms of contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Made with ❤️ by DocSyncForge Team**

[⬆ Back to Top](#-docsyncforge)

</div>
