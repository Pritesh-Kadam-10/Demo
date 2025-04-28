import google.generativeai as genai
from src.prompta2 import Prompts
import os

# class LLM:
#     def __init__(self):
#         genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#         self.model = genai.GenerativeModel('gemini-1.5-pro')
#         self.prompts = Prompts()

#     def analyze_files(self, files):
#         file_analysis = []
#         for file in files:
#             file_analysis.append(
#                 f"FILE: {file['path']}\n"
#                 f"LANGUAGE: {file['language']}\n"
#                 f"CONTENT:\n{file['content'][:2000]}\n"
#             )
        
#         prompt = self.prompts.analysis_prompt().format(
#             files_analysis='\n'.join(file_analysis)
#         )
        
#         try:
#             response = self.model.generate_content(prompt)
#             return self._parse_response(response.text)
#         except Exception as e:
#             return {"error": str(e)}

#     '''def _parse_response(self, text):
#         parsed = {
#             'critical': [],
#             'warnings': [],
#             'style': [],
#             'priority': []
#         }
        
#         current_file = None
#         current_category = None
        
#         for line in text.split('\n'):
#             line = line.strip()
            
#             if line.startswith('File:'):
#                 current_file = line.split('File:')[1].split('Language:')[0].strip()
            
#             elif line.startswith('[Critical]:'):
#                 current_category = 'critical'
            
#             elif line.startswith('[Warning]:'):
#                 current_category = 'warning'
            
#             elif line.startswith('[Style]:'):
#                 current_category = 'style'
            
#             elif line.startswith('-') and current_file and current_category:
#                 issue = {
#                     'file': current_file,
#                     'description': line[1:].strip(),
#                     'category': current_category
#                 }
#                 parsed[current_category].append(issue)
            
#             elif line.startswith('PRIORITY FIX ORDER:'):
#                 current_category = 'priority'
            
#             elif line.startswith('1.') and current_category == 'priority':
#                 parsed['priority'] = []
#                 for fix in line.split('\n'):
#                     if fix.strip():
#                         parsed['priority'].append(fix.strip())
        
#         return parsed'''

# def _parse_response(self, text):
#     parsed = {
#         'critical': [],
#         'warning': [],  # <<< changed
#         'style': [],
#         'priority': []
#     }
    
#     current_file = None
#     current_category = None
    
#     for line in text.split('\n'):
#         line = line.strip()
        
#         if line.startswith('File:'):
#             current_file = line.split('File:')[1].split('Language:')[0].strip()
        
#         elif line.startswith('[Critical]:'):
#             current_category = 'critical'
        
#         elif line.startswith('[Warning]:'):
#             current_category = 'warning'
        
#         elif line.startswith('[Style]:'):
#             current_category = 'style'
        
#         elif line.startswith('-') and current_file and current_category:
#             issue = {
#                 'file': current_file,
#                 'description': line[1:].strip(),
#                 'category': current_category
#             }
#             parsed[current_category].append(issue)
        
#         elif line.startswith('PRIORITY FIX ORDER:'):
#             current_category = 'priority'
        
#         elif line.startswith('1.') and current_category == 'priority':
#             parsed['priority'] = []
#             for fix in line.split('\n'):
#                 if fix.strip():
#                     parsed['priority'].append(fix.strip())
    
#     return parsed



class LLM:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.prompts = Prompts()

    def analyze_files(self, files):
        file_analysis = []
        for file in files:
            file_analysis.append(
                f"FILE: {file['path']}\n"
                f"LANGUAGE: {file['language']}\n"
                f"CONTENT:\n{file['content'][:2000]}\n"
            )
        
        prompt = self.prompts.analysis_prompt().format(
            files_analysis='\n'.join(file_analysis)
        )
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text)  # calling correctly
        except Exception as e:
            return {"error": str(e)}

    def _parse_response(self, text):  # <<< NOTICE: now properly inside the class!
        parsed = {
            'critical': [],
            'warning': [],  # <<< typo fix (was "warnings" elsewhere)
            'style': [],
            'priority': []
        }
        
        current_file = None
        current_category = None
        
        for line in text.split('\n'):
            line = line.strip()
            
            if line.startswith('File:'):
                current_file = line.split('File:')[1].split('Language:')[0].strip()
            
            elif line.startswith('[Critical]:'):
                current_category = 'critical'
            
            elif line.startswith('[Warning]:'):
                current_category = 'warning'
            
            elif line.startswith('[Style]:'):
                current_category = 'style'
            
            elif line.startswith('-') and current_file and current_category:
                issue = {
                    'file': current_file,
                    'description': line[1:].strip(),
                    'category': current_category
                }
                parsed[current_category].append(issue)
            
            elif line.startswith('PRIORITY FIX ORDER:'):
                current_category = 'priority'
            
            elif line.startswith('1.') and current_category == 'priority':
                parsed['priority'] = []
                for fix in line.split('\n'):
                    if fix.strip():
                        parsed['priority'].append(fix.strip())
        
        return parsed
