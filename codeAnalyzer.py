import re
from pathlib import Path
from dotenv import load_dotenv
from src.reviewerLlm import reviewLLM

load_dotenv()

class CodeAnalyzer:
    def __init__(self):
        self.supported_langs = {
            '.py': 'Python',
            '.java': 'Java',
            '.cpp': 'C++',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.go': 'Go'
        }

    def get_code_files(self, folder_path):
        files = []
        folder_path = Path(folder_path)

        for path in folder_path.rglob('*'):
            if path.is_file() and path.suffix.lower() in self.supported_langs:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    files.append({
                        'path': str(path.relative_to(folder_path)),
                        'language': self.supported_langs[path.suffix.lower()],
                        'content': content,
                        'camel_issues': self.check_camel_casing(content)
                    })
                except Exception as e:
                    print(f"⚠️ Error reading {path}: {e}")

        return files


    def check_camel_casing(self, content):
        snake_case = re.findall(r'\b[a-z]+_[a-z0-9_]+\b', content)
        return snake_case

class AnalysisPipeline:
    def __init__(self):
        self.analyzer = CodeAnalyzer()
        self.llm = reviewLLM()

    def generate_report(self, folder_path):
        files = self.analyzer.get_code_files(folder_path)
        if not files:
            raise ValueError("No code files found")
        
        report = self.llm.analyze_files(files)
        print("DEBUG: Report from LLM:", report)

        if 'warning' in report and 'warnings' not in report:
            report['warnings'] = report.pop('warning')

        return self._format_report(files, report)

    def _format_report(self, files, analysis):
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("                       CODE REVIEW REPORT")
        report_lines.append("=" * 80 + "\n")

        report_lines.append(f"Total Critical Issues  : {len(analysis['critical'])}")
        report_lines.append(f"Total Warnings         : {len(analysis['warnings'])}")
        report_lines.append(f"Total Style Issues     : {len(analysis['style'])}\n")

        if analysis['critical']:
            report_lines.append(">>> CRITICAL ISSUES <<<\n")
            for issue in analysis['critical']:
                report_lines.append(f"• File: {issue['file']}")
                report_lines.append(f"  >> {issue['description']}\n")

        if analysis.get('priority'):
            report_lines.append(">>> PRIORITY FIX ORDER <<<\n")
            for fix in analysis['priority']:
                report_lines.append(f"• {fix}")
            report_lines.append("")

        report_lines.append("=" * 80)
        report_lines.append("                       FILE-WISE ANALYSIS")
        report_lines.append("=" * 80 + "\n")

        for file in files:
            report_lines.append(f"\n========== File: {file['path']} ({file['language']}) ==========\n")

            file_issues = [
                i for i in analysis['critical'] +
                analysis['warnings'] +
                analysis['style']
                if i['file'] == file['path']
            ]

            if not file_issues:
                report_lines.append("✓ No issues found in this file.\n")
            else:
                for issue in file_issues:
                    report_lines.append(f"[{issue['category'].upper()}] {issue['description']} (line {issue.get('line', '?')})")

            if file['camel_issues']:
                report_lines.append("\n⚠ Potential Naming Issues Detected:")
                for name in file['camel_issues']:
                    report_lines.append(f"• {name}")

        report_lines.append("\n" + "=" * 80)
        report_lines.append("                       END OF REPORT")
        report_lines.append("=" * 80)

        return '\n'.join(report_lines)