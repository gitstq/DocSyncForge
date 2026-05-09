#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DocSyncForge - 智能文档同步引擎
Lightweight Intelligent Documentation Sync Engine

自动检测代码变更，智能生成文档更新，多平台同步发布
"""

import os
import sys
import json
import re
import subprocess
import argparse
import fnmatch
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime

__version__ = "1.0.0"
__author__ = "DocSyncForge Team"


# =============================================================================
# 数据模型
# =============================================================================

@dataclass
class CodeChange:
    """代码变更数据模型"""
    file_path: str
    change_type: str  # added, modified, deleted
    old_content: Optional[str] = None
    new_content: Optional[str] = None
    diff_content: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class DocSection:
    """文档章节数据模型"""
    title: str
    content: str
    level: int
    source_file: str
    last_updated: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class SyncConfig:
    """同步配置数据模型"""
    source_dirs: List[str]
    doc_dirs: List[str]
    ignore_patterns: List[str]
    watch_extensions: List[str]
    sync_targets: List[str]
    auto_sync: bool = False
    
    def to_dict(self) -> Dict:
        return asdict(self)


# =============================================================================
# 核心引擎类
# =============================================================================

class GitChangeDetector:
    """Git变更检测引擎"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
    
    def _run_git_command(self, args: List[str]) -> Tuple[bool, str]:
        """执行Git命令"""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            if result.returncode == 0:
                return True, result.stdout
            return False, result.stderr
        except Exception as e:
            return False, str(e)
    
    def is_git_repo(self) -> bool:
        """检查是否为Git仓库"""
        success, _ = self._run_git_command(["rev-parse", "--git-dir"])
        return success
    
    def get_changed_files(self, since_ref: str = "HEAD~1") -> List[CodeChange]:
        """获取变更文件列表"""
        success, output = self._run_git_command(
            ["diff", "--name-status", since_ref]
        )
        
        if not success:
            return []
        
        changes = []
        for line in output.strip().split('\n'):
            if not line.strip():
                continue
            
            parts = line.split('\t')
            if len(parts) >= 2:
                change_type = parts[0][0]  # A, M, D, R
                file_path = parts[1]
                
                type_map = {
                    'A': 'added',
                    'M': 'modified',
                    'D': 'deleted',
                    'R': 'renamed'
                }
                
                change = CodeChange(
                    file_path=file_path,
                    change_type=type_map.get(change_type, 'unknown')
                )
                changes.append(change)
        
        return changes
    
    def get_file_diff(self, file_path: str, since_ref: str = "HEAD~1") -> str:
        """获取文件差异内容"""
        success, output = self._run_git_command(
            ["diff", since_ref, "--", file_path]
        )
        return output if success else ""
    
    def get_unstaged_changes(self) -> List[CodeChange]:
        """获取未暂存的变更"""
        success, output = self._run_git_command(
            ["diff", "--name-status"]
        )
        
        if not success:
            return []
        
        changes = []
        for line in output.strip().split('\n'):
            if not line.strip():
                continue
            
            parts = line.split('\t')
            if len(parts) >= 2:
                change_type = 'modified' if parts[0][0] == 'M' else 'added'
                file_path = parts[1]
                
                change = CodeChange(
                    file_path=file_path,
                    change_type=change_type
                )
                changes.append(change)
        
        return changes


class ASTAnalyzer:
    """代码AST分析器"""
    
    SUPPORTED_EXTENSIONS = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.java': 'java',
        '.go': 'go',
        '.rs': 'rust'
    }
    
    def __init__(self):
        self.patterns = {
            'python': {
                'function': r'def\s+(\w+)\s*\(',
                'class': r'class\s+(\w+)',
                'docstring': r'["\']{3}(.+?)["\']{3}',
                'comment': r'#\s*(.+)'
            },
            'javascript': {
                'function': r'function\s+(\w+)|(\w+)\s*=\s*\(|(\w+)\s*:\s*function',
                'class': r'class\s+(\w+)',
                'docstring': r'/\*\*(.+?)\*/',
                'comment': r'//\s*(.+)'
            },
            'typescript': {
                'function': r'function\s+(\w+)|(\w+)\s*[=:]\s*\(',
                'class': r'class\s+(\w+)',
                'interface': r'interface\s+(\w+)',
                'docstring': r'/\*\*(.+?)\*/',
                'comment': r'//\s*(.+)'
            },
            'java': {
                'function': r'(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\(',
                'class': r'class\s+(\w+)',
                'docstring': r'/\*\*(.+?)\*/',
                'comment': r'//\s*(.+)'
            },
            'go': {
                'function': r'func\s+(?:\([^)]+\)\s+)?(\w+)\s*\(',
                'struct': r'type\s+(\w+)\s+struct',
                'comment': r'//\s*(.+)'
            },
            'rust': {
                'function': r'fn\s+(\w+)',
                'struct': r'struct\s+(\w+)',
                'trait': r'trait\s+(\w+)',
                'comment': r'//\s*(.+)'
            }
        }
    
    def detect_language(self, file_path: str) -> Optional[str]:
        """检测文件语言类型"""
        ext = Path(file_path).suffix.lower()
        return self.SUPPORTED_EXTENSIONS.get(ext)
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """分析代码文件"""
        language = self.detect_language(file_path)
        if not language:
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'error': str(e)}
        
        patterns = self.patterns.get(language, {})
        analysis = {
            'language': language,
            'file_path': file_path,
            'total_lines': len(content.split('\n')),
            'functions': [],
            'classes': [],
            'interfaces': [],
            'structs': [],
            'traits': [],
            'docstrings': [],
            'comments': []
        }
        
        # 提取函数
        if 'function' in patterns:
            for match in re.finditer(patterns['function'], content, re.MULTILINE):
                func_name = next((g for g in match.groups() if g), None)
                if func_name:
                    analysis['functions'].append(func_name)
        
        # 提取类
        if 'class' in patterns:
            for match in re.finditer(patterns['class'], content, re.MULTILINE):
                class_name = match.group(1)
                if class_name:
                    analysis['classes'].append(class_name)
        
        # 提取接口
        if 'interface' in patterns:
            for match in re.finditer(patterns['interface'], content, re.MULTILINE):
                interface_name = match.group(1)
                if interface_name:
                    analysis['interfaces'].append(interface_name)
        
        # 提取结构体
        if 'struct' in patterns:
            for match in re.finditer(patterns['struct'], content, re.MULTILINE):
                struct_name = match.group(1)
                if struct_name:
                    analysis['structs'].append(struct_name)
        
        # 提取trait
        if 'trait' in patterns:
            for match in re.finditer(patterns['trait'], content, re.MULTILINE):
                trait_name = match.group(1)
                if trait_name:
                    analysis['traits'].append(trait_name)
        
        # 提取文档字符串
        if 'docstring' in patterns:
            for match in re.finditer(patterns['docstring'], content, re.DOTALL):
                docstring = match.group(1).strip()
                if docstring:
                    analysis['docstrings'].append(docstring[:200])
        
        # 提取注释
        if 'comment' in patterns:
            for match in re.finditer(patterns['comment'], content):
                comment = match.group(1).strip()
                if comment:
                    analysis['comments'].append(comment)
        
        return analysis
    
    def extract_api_changes(self, old_analysis: Dict, new_analysis: Dict) -> Dict:
        """提取API变更"""
        changes = {
            'added_functions': [],
            'removed_functions': [],
            'added_classes': [],
            'removed_classes': [],
            'modified_docstrings': []
        }
        
        old_funcs = set(old_analysis.get('functions', []))
        new_funcs = set(new_analysis.get('functions', []))
        changes['added_functions'] = list(new_funcs - old_funcs)
        changes['removed_functions'] = list(old_funcs - new_funcs)
        
        old_classes = set(old_analysis.get('classes', []))
        new_classes = set(new_analysis.get('classes', []))
        changes['added_classes'] = list(new_classes - old_classes)
        changes['removed_classes'] = list(old_classes - new_classes)
        
        return changes


class DocGenerator:
    """文档生成器"""
    
    TEMPLATES = {
        'function': """### {name}

**功能描述**: {description}

**参数**:
{params}

**返回值**: {returns}

**示例**:
```python
{example}
```
""",
        'class': """## {name}

**类描述**: {description}

**属性**:
{attributes}

**方法**:
{methods}
""",
        'module': """# {name}

**模块描述**: {description}

**导出内容**:
{exports}

---

{content}
"""
    }
    
    def __init__(self):
        self.templates = self.TEMPLATES
    
    def generate_function_doc(self, func_name: str, analysis: Dict) -> str:
        """生成函数文档"""
        return self.templates['function'].format(
            name=func_name,
            description=f"{func_name} 函数",
            params="- 待补充",
            returns="待补充",
            example=f"{func_name}()"
        )
    
    def generate_class_doc(self, class_name: str, analysis: Dict) -> str:
        """生成类文档"""
        methods = '\n'.join([f"- `{m}()`" for m in analysis.get('functions', [])[:5]])
        return self.templates['class'].format(
            name=class_name,
            description=f"{class_name} 类",
            attributes="- 待补充",
            methods=methods or "- 待补充"
        )
    
    def generate_update_suggestions(self, changes: List[CodeChange], 
                                   analyses: Dict[str, Dict]) -> List[DocSection]:
        """生成文档更新建议"""
        suggestions = []
        
        for change in changes:
            if change.change_type == 'added':
                analysis = analyses.get(change.file_path, {})
                
                # 为新函数生成文档建议
                for func in analysis.get('functions', []):
                    content = self.generate_function_doc(func, analysis)
                    suggestions.append(DocSection(
                        title=f"新增函数: {func}",
                        content=content,
                        level=3,
                        source_file=change.file_path,
                        last_updated=datetime.now().isoformat()
                    ))
                
                # 为新类生成文档建议
                for cls in analysis.get('classes', []):
                    content = self.generate_class_doc(cls, analysis)
                    suggestions.append(DocSection(
                        title=f"新增类: {cls}",
                        content=content,
                        level=2,
                        source_file=change.file_path,
                        last_updated=datetime.now().isoformat()
                    ))
            
            elif change.change_type == 'modified':
                suggestions.append(DocSection(
                    title=f"更新: {Path(change.file_path).name}",
                    content=f"文件 `{change.file_path}` 已修改，建议检查相关文档是否需要更新。",
                    level=2,
                    source_file=change.file_path,
                    last_updated=datetime.now().isoformat()
                ))
        
        return suggestions


class DocSyncEngine:
    """文档同步引擎"""
    
    def __init__(self, config: Optional[SyncConfig] = None):
        self.config = config or self._default_config()
        self.git_detector = GitChangeDetector()
        self.ast_analyzer = ASTAnalyzer()
        self.doc_generator = DocGenerator()
        self.sync_history: List[Dict] = []
    
    def _default_config(self) -> SyncConfig:
        """默认配置"""
        return SyncConfig(
            source_dirs=['src', 'lib', 'app'],
            doc_dirs=['docs', 'README.md'],
            ignore_patterns=['*.pyc', '*.min.js', 'node_modules/*', '.git/*'],
            watch_extensions=['.py', '.js', '.ts', '.java', '.go', '.rs'],
            sync_targets=['local'],
            auto_sync=False
        )
    
    def load_config(self, config_path: str) -> bool:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.config = SyncConfig(**data)
            return True
        except Exception as e:
            print(f"[错误] 加载配置失败: {e}")
            return False
    
    def save_config(self, config_path: str) -> bool:
        """保存配置文件"""
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config.to_dict(), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[错误] 保存配置失败: {e}")
            return False
    
    def should_ignore(self, file_path: str) -> bool:
        """检查文件是否应该被忽略"""
        for pattern in self.config.ignore_patterns:
            if fnmatch.fnmatch(file_path, pattern):
                return True
        return False
    
    def scan_changes(self, since_ref: str = "HEAD~1") -> Dict[str, Any]:
        """扫描代码变更"""
        if not self.git_detector.is_git_repo():
            return {'error': '当前目录不是Git仓库'}
        
        # 获取变更文件
        changes = self.git_detector.get_changed_files(since_ref)
        
        # 过滤需要处理的文件
        filtered_changes = []
        for change in changes:
            if self.should_ignore(change.file_path):
                continue
            
            ext = Path(change.file_path).suffix
            if ext in self.config.watch_extensions:
                filtered_changes.append(change)
        
        # 分析变更文件
        analyses = {}
        for change in filtered_changes:
            if change.change_type != 'deleted':
                full_path = self.git_detector.repo_path / change.file_path
                if full_path.exists():
                    analyses[change.file_path] = self.ast_analyzer.analyze_file(str(full_path))
        
        # 生成文档更新建议
        suggestions = self.doc_generator.generate_update_suggestions(
            filtered_changes, analyses
        )
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'total_changes': len(changes),
            'filtered_changes': len(filtered_changes),
            'changes': [c.to_dict() for c in filtered_changes],
            'analyses': analyses,
            'suggestions': [s.to_dict() for s in suggestions]
        }
        
        self.sync_history.append(result)
        return result
    
    def generate_report(self, output_path: Optional[str] = None) -> str:
        """生成同步报告"""
        if not self.sync_history:
            return "暂无同步记录"
        
        latest = self.sync_history[-1]
        
        report_lines = [
            "# DocSyncForge 同步报告",
            "",
            f"**生成时间**: {latest['timestamp']}",
            f"**总变更数**: {latest['total_changes']}",
            f"**需处理变更**: {latest['filtered_changes']}",
            "",
            "## 变更文件列表",
            ""
        ]
        
        for change in latest['changes']:
            icon = {'added': '➕', 'modified': '✏️', 'deleted': '🗑️'}.get(
                change['change_type'], '📝'
            )
            report_lines.append(f"- {icon} `{change['file_path']}` ({change['change_type']})")
        
        report_lines.extend([
            "",
            "## 文档更新建议",
            ""
        ])
        
        for suggestion in latest['suggestions']:
            report_lines.append(f"### {suggestion['title']}")
            report_lines.append(f"**来源文件**: `{suggestion['source_file']}`")
            report_lines.append("")
            report_lines.append(suggestion['content'])
            report_lines.append("")
        
        report = '\n'.join(report_lines)
        
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"[成功] 报告已保存至: {output_path}")
            except Exception as e:
                print(f"[错误] 保存报告失败: {e}")
        
        return report


# =============================================================================
# CLI 界面
# =============================================================================

def create_banner() -> str:
    """创建ASCII艺术横幅"""
    return """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   📚 DocSyncForge - 智能文档同步引擎                         ║
║   Lightweight Intelligent Documentation Sync Engine          ║
║                                                              ║
║   自动检测代码变更 → 智能生成文档 → 多平台同步               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """


def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(
        description='DocSyncForge - 智能文档同步引擎',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s scan                    # 扫描最近的代码变更
  %(prog)s scan --since HEAD~5     # 扫描最近5次提交的变更
  %(prog)s report                  # 生成同步报告
  %(prog)s init                    # 初始化配置文件
  %(prog)s watch                   # 监听文件变更（开发模式）
        """
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version=f'DocSyncForge v{__version__}'
    )
    
    parser.add_argument(
        '--config', '-c',
        default='.docsyncforge.json',
        help='配置文件路径 (默认: .docsyncforge.json)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # scan 命令
    scan_parser = subparsers.add_parser('scan', help='扫描代码变更')
    scan_parser.add_argument(
        '--since', '-s',
        default='HEAD~1',
        help='从哪个Git引用开始扫描 (默认: HEAD~1)'
    )
    scan_parser.add_argument(
        '--output', '-o',
        help='输出JSON文件路径'
    )
    
    # report 命令
    report_parser = subparsers.add_parser('report', help='生成同步报告')
    report_parser.add_argument(
        '--output', '-o',
        default='docsync-report.md',
        help='报告输出路径 (默认: docsync-report.md)'
    )
    
    # init 命令
    init_parser = subparsers.add_parser('init', help='初始化配置文件')
    init_parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='强制覆盖已存在的配置文件'
    )
    
    # analyze 命令
    analyze_parser = subparsers.add_parser('analyze', help='分析代码文件')
    analyze_parser.add_argument(
        'file',
        help='要分析的代码文件路径'
    )
    
    # status 命令
    status_parser = subparsers.add_parser('status', help='查看同步状态')
    
    args = parser.parse_args()
    
    # 打印横幅
    if args.command:
        print(create_banner())
    
    # 初始化引擎
    engine = DocSyncEngine()
    
    # 加载配置（如果存在）
    config_path = Path(args.config)
    if config_path.exists():
        engine.load_config(str(config_path))
    
    # 执行命令
    if args.command == 'scan':
        print(f"[扫描] 正在扫描代码变更 (since: {args.since})...")
        result = engine.scan_changes(args.since)
        
        if 'error' in result:
            print(f"[错误] {result['error']}")
            sys.exit(1)
        
        print(f"[完成] 发现 {result['total_changes']} 个变更")
        print(f"       其中 {result['filtered_changes']} 个需要处理")
        
        if result['suggestions']:
            print(f"\n[建议] 生成 {len(result['suggestions'])} 条文档更新建议:")
            for suggestion in result['suggestions']:
                print(f"  • {suggestion['title']}")
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n[保存] 结果已保存至: {args.output}")
    
    elif args.command == 'report':
        print("[生成] 正在生成同步报告...")
        report = engine.generate_report(args.output)
        
        if not engine.sync_history:
            print("[提示] 暂无同步记录，请先运行 'scan' 命令")
        else:
            print(f"\n{report}")
    
    elif args.command == 'init':
        if config_path.exists() and not args.force:
            print(f"[提示] 配置文件已存在: {config_path}")
            print("      使用 --force 覆盖")
            sys.exit(0)
        
        engine.save_config(str(config_path))
        print(f"[成功] 配置文件已创建: {config_path}")
        print("\n您可以编辑此文件来自定义同步规则:")
        print("  - source_dirs: 源代码目录")
        print("  - doc_dirs: 文档目录")
        print("  - ignore_patterns: 忽略模式")
        print("  - watch_extensions: 监听的文件扩展名")
    
    elif args.command == 'analyze':
        print(f"[分析] 正在分析文件: {args.file}")
        
        if not Path(args.file).exists():
            print(f"[错误] 文件不存在: {args.file}")
            sys.exit(1)
        
        analysis = engine.ast_analyzer.analyze_file(args.file)
        
        if not analysis:
            print("[提示] 不支持的文件类型")
            sys.exit(0)
        
        print(f"\n语言: {analysis.get('language', 'unknown')}")
        print(f"总行数: {analysis.get('total_lines', 0)}")
        
        if analysis.get('functions'):
            print(f"\n函数 ({len(analysis['functions'])}):")
            for func in analysis['functions'][:10]:
                print(f"  • {func}")
        
        if analysis.get('classes'):
            print(f"\n类 ({len(analysis['classes'])}):")
            for cls in analysis['classes']:
                print(f"  • {cls}")
        
        if analysis.get('docstrings'):
            print(f"\n文档字符串 ({len(analysis['docstrings'])}):")
            for doc in analysis['docstrings'][:3]:
                preview = doc[:100].replace('\n', ' ')
                print(f"  • {preview}...")
    
    elif args.command == 'status':
        print("[状态] DocSyncForge 状态信息")
        print(f"\n版本: {__version__}")
        print(f"配置文件: {config_path} ({'存在' if config_path.exists() else '不存在'})")
        print(f"Git仓库: {'是' if engine.git_detector.is_git_repo() else '否'}")
        print(f"同步历史: {len(engine.sync_history)} 条记录")
        
        if engine.sync_history:
            latest = engine.sync_history[-1]
            print(f"最后同步: {latest['timestamp']}")
    
    else:
        parser.print_help()
        print(create_banner())


if __name__ == '__main__':
    main()
