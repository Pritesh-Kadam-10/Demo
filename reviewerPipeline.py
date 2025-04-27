import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from src.codeAnalyzer import AnalysisPipeline

load_dotenv()

def reviewMain(folder_path):
    try:
        pipeline = AnalysisPipeline()
        # folder_path = input("Enter code folder path: ").strip()

        if not os.path.isdir(folder_path):
            raise ValueError("Invalid folder path")

        report = pipeline.generate_report(folder_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"code_review_report_{timestamp}.txt"
        report_path = Path.cwd() / report_filename

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n✅ Report saved automatically at: {report_path}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    reviewMain()
