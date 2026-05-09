# 贡献指南

感谢您对 DocSyncForge 的兴趣！我们欢迎各种形式的贡献。

## 如何贡献

### 报告问题

如果您发现了bug或有功能建议，请通过 GitHub Issues 提交：

1. 检查是否已有相关问题
2. 使用对应的 issue 模板
3. 提供详细的复现步骤和环境信息

### 提交代码

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个 Pull Request

### 代码规范

- 遵循 PEP 8 规范
- 添加适当的注释和文档字符串
- 确保代码通过所有测试
- 更新相关文档

### 提交信息规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

## 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/gitstq/docsyncforge.git
cd docsyncforge

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行测试
python -m pytest
```

## 行为准则

- 尊重所有参与者
- 接受建设性批评
- 关注对社区最有利的事情

## 许可证

通过贡献代码，您同意您的贡献将在 MIT 许可证下发布。
