# import os
# import difflib
# import google.generativeai as genai
# from src.prompts import Prompts

# MODEL_NAME = "gemini-1.5-pro"


# class reviewLLM:
#     def __init__(self):
#         # Configuring the Google API key
#         genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#         self.model = genai.GenerativeModel(MODEL_NAME)
#         self.prompts = Prompts()  # Initialize Prompts class to get the prompt templates

#     def ask_gemini(self, added_code_lines):
#         # Adjust the prompt format to handle added_code_lines correctly
#         prompt = f"Please review the following code changes:\n{added_code_lines}\nExplain the changes in detail."
#         response = self.model.generate_content(prompt)

#         # Print the response structure to debug
#         print(response)

#         # Assuming 'response' has a 'text' attribute or method to get the content
#         try:
#             return response.text  # Or another correct way to access the content
#         except AttributeError:
#             return "No explanation received from Gemini."

#     def get_added_lines(self, old_lines, new_lines):
#         diff = difflib.unified_diff(old_lines, new_lines, lineterm='')
#         added = [line[1:] for line in diff if line.startswith('+') and not line.startswith('+++')]
#         return added

#     def get_removed_lines(self, old_lines, new_lines):
#         diff = difflib.unified_diff(old_lines, new_lines, lineterm='')
#         removed = [line[1:] for line in diff if line.startswith('-') and not line.startswith('---')]
#         return removed

#     def get_updated_lines(self, old_lines, new_lines):
#         added_lines = self.get_added_lines(old_lines, new_lines)
#         removed_lines = self.get_removed_lines(old_lines, new_lines)
#         return {"added": added_lines, "removed": removed_lines}

#     def calculate_diff_percentage(self, old_lines, new_lines):
#         sm = difflib.SequenceMatcher(None, ''.join(old_lines), ''.join(new_lines))
#         diff_ratio = 1 - sm.ratio()  # Calculating difference as 1 - similarity ratio
#         return round(diff_ratio * 100, 2)

#     def compare_files(self, file1, file2):
#         old_lines = self.read_file(file1)
#         new_lines = self.read_file(file2)
#         added = self.get_added_lines(old_lines, new_lines)
#         removed = self.get_removed_lines(old_lines, new_lines)
#         updated = self.get_updated_lines(old_lines, new_lines)
#         diff_percentage = self.calculate_diff_percentage(old_lines, new_lines)
#         return added, removed, updated, old_lines, new_lines, diff_percentage

#     def read_file(self, filepath):
#         with open(filepath, 'r', encoding='utf-8') as file:
#             return file.readlines()

#     def generate_report(self, folder1, folder2):
#         """Generates a short comparison report with added/removed modules and explanations."""
#         with open('comparison_report.txt', 'w', encoding='utf-8') as report:
#             report.write("=== FOLDER COMPARISON REPORT ===\n\n")

#             files_in_folder1 = {f for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f))}
#             files_in_folder2 = {f for f in os.listdir(folder2) if os.path.isfile(os.path.join(folder2, f))}

#             matching_files = files_in_folder1.intersection(files_in_folder2)

#             total_diff_percentage = 0
#             file_count = 0

#             for file_name in matching_files:
#                 file1 = os.path.join(folder1, file_name)
#                 file2 = os.path.join(folder2, file_name)

#                 added, removed, updated, old_lines, new_lines, diff_percentage = self.compare_files(file1, file2)

#                 # Report for each file
#                 report.write(f"--- Comparing File: {file_name} ---\n")
#                 report.write(f"Difference Percentage: {diff_percentage}%\n")
#                 if added or removed:
#                     report.write(f"Changes Detected: {' '.join(added[:3] + removed[:3])}\n")  # Show a snippet
#                 else:
#                     report.write("No significant changes detected.\n")

#                 # AI explanation for added lines
#                 if added:
#                     explanation = self.ask_gemini('\n'.join(added[:3]))  # Only send a snippet of added lines
#                     report.write(f"\nAI Explanation of Changes:\n{explanation}\n")
#                 report.write("=" * 50 + "\n")

#                 total_diff_percentage += diff_percentage
#                 file_count += 1

#             # Calculate overall percentage
#             overall_diff_percentage = total_diff_percentage / file_count if file_count > 0 else 0
#             report.write("\n=== FOLDER COMPARISON SUMMARY ===\n")
#             report.write(f"Overall Difference Percentage: {overall_diff_percentage}%\n")
#             report.write("=" * 50 + "\n")

#         print("\n✅ Report generated: 'comparison_report.txt'.")


# def main():
#     print("=== Folder Comparison Script ===\n")
#     folder1 = r"C:\workitem\AITHON\Medical project\code reviewer\src_old"
#     folder2 = r"C:\workitem\AITHON\Medical project\code reviewer\src"
#     review = reviewLLM()
#     review.generate_report(folder1, folder2)


# if __name__ == "__main__":
#     main()



import os
import difflib
import google.generativeai as genai
from src.prompts import Prompts

MODEL_NAME = "gemini-1.5-pro"


class compareLLM:
    def __init__(self):
        # Configuring the Google API key
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(MODEL_NAME)
        self.prompts = Prompts()  # Initialize Prompts class to get the prompt templates

    def ask_gemini(self, added_code_lines):
        # Adjust the prompt format to handle added_code_lines correctly
        prompt = f"Please review the following code changes:\n{added_code_lines}\nExplain the changes in detail."
        response = self.model.generate_content(prompt)

        # Print the response structure to debug
        print(response)

        # Assuming 'response' has a 'text' attribute or method to get the content
        try:
            return response.text  # Or another correct way to access the content
        except AttributeError:
            return "No explanation received from Gemini."

    def get_added_lines(self, old_lines, new_lines):
        diff = difflib.unified_diff(old_lines, new_lines, lineterm='')
        )]
        return added

    def get_removed_lines(self, old_lines, new_lines):
        diff = difflib.unified_diff(old_lines, new_lines, lineterm='')
        removed = [line[1:] for line in diff if line.startswith('-') and not line.startswith('---')]
        return removed

    def get_updated_lines(self, old_lines, new_lines):
        added_lines = self.get_added_lines(old_lines, new_lines)
        removed_lines = self.get_removed_lines(old_lines, new_lines)
        return {"added": added_lines, "removed": removed_lines}

    def calculate_diff_percentage(self, old_lines, new_lines):
        sm = difflib.SequenceMatcher(None, ''.join(old_lines), ''.join(new_lines))
        diff_ratio = 1 - sm.ratio()  # Calculating difference as 1 - similarity ratio
        return round(diff_ratio * 100, 2)

    def compare_files(self, file1, file2):
        old_lines = self.read_file(file1)
        new_lines = self.read_file(file2)
        added = self.get_added_lines(old_lines, new_lines)
        removed = self.get_removed_lines(old_lines, new_lines)
        updated = self.get_updated_lines(old_lines, new_lines)
        diff_percentage = self.calculate_diff_percentage(old_lines, new_lines)
        return added, removed, updated, old_lines, new_lines, diff_percentage

    def read_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.readlines()

    def generate_report(self, folder1, folder2):
        """Generates a short comparison report with added/removed modules and explanations."""
        with open('comparison_report.txt', 'w', encoding='utf-8') as report:
            report.write("=== FOLDER COMPARISON REPORT ===\n\n")

            files_in_folder1 = {f for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f))}
            files_in_folder2 = {f for f in os.listdir(folder2) if os.path.isfile(os.path.join(folder2, f))}

            matching_files = files_in_folder1.intersection(files_in_folder2)

            total_diff_percentage = 0
            file_count = 0

            added_files = {f for f in files_in_folder2 if f not in files_in_folder1 and f.endswith('.py')}
            removed_files = {f for f in files_in_folder1 if f not in files_in_folder2 and f.endswith('.py')}

            for file_name in matching_files:
                file1 = os.path.join(folder1, file_name)
                file2 = os.path.join(folder2, file_name)

                added, removed, updated, old_lines, new_lines, diff_percentage = self.compare_files(file1, file2)

                # Report for each file
                report.write(f"--- Comparing File: {file_name} ---\n")
                report.write(f"Difference Percentage: {diff_percentage}%\n")
                if added or removed:
                    report.write(f"Changes Detected: {' '.join(added[:3] + removed[:3])}\n")  # Show a snippet
                else:
                    report.write("No significant changes detected.\n")

                # AI explanation for added lines
                if added:
                    explanation = self.ask_gemini('\n'.join(added[:3]))  # Only send a snippet of added lines
                    report.write(f"\nAI Explanation of Changes:\n{explanation}\n")
                report.write("=" * 50 + "\n")

                total_diff_percentage += diff_percentage
                file_count += 1

            # Calculate overall percentage
            overall_diff_percentage = total_diff_percentage / file_count if file_count > 0 else 0
            report.write("\n=== FOLDER COMPARISON SUMMARY ===\n")
            report.write(f"Overall Difference Percentage: {overall_diff_percentage}%\n")

            # Report added and removed files/modules
            report.write("\n=== ADDED PY FILES ===\n")
            report.write(f"Total added files: {len(added_files)}\n")
            for file in added_files:
                report.write(f"- {file}\n")

            report.write("\n=== REMOVED PY FILES ===\n")
            report.write(f"Total removed files: {len(removed_files)}\n")
            for file in removed_files:
                report.write(f"- {file}\n")

            report.write("=" * 50 + "\n")

        print("\n✅ Report generated: 'comparison_report.txt'.")


def compareMain(folder1,folder2):
    print("=== Folder Comparison Script ===\n")
    # folder1 = r"C:\workitem\AITHON\Medical project\code reviewer\src_old"
    # folder2 = r"C:\workitem\AITHON\Medical project\code reviewer\src"
    compare = compareLLM()
    compare.generate_report(folder1, folder2)


if __name__ == "__main__":
    compareMain()
