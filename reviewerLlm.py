import os
import google.generativeai as genai
from src.setting import MODEL_NAME
from dotenv import load_dotenv
from src.prompts import Prompts
from src import logging
from typing import Dict, Any
import json

load_dotenv()

class LLM:
    def __init__(self):
        self.API_KEY = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.API_KEY)
        self.model = genai.GenerativeModel(model_name=MODEL_NAME)
        self.prompts = Prompts()

    def _generate_response(self, prompt: str, config: Dict[str, Any] = None) -> str:
        """Internal method to handle API calls"""
        default_config = {
            'temperature': 0.2,
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 8192
        }
        merged_config = {**default_config, **(config or {})}
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(**merged_config)
            )
            return response.text
        except Exception as e:
            logging.error(f"Generation error: {str(e)}")
            raise

    def analyze_code_quality(self, code_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze code quality and standards compliance
        
        Args:
            code_data: Output from CodeAnalyzer
            
        Returns:
            Analysis report in dictionary format
        """
        prompt = self.prompts.code_quality_prompt().format(
            code_summary=json.dumps(code_data['metadata'], indent=2),
            code_samples=code_data['llm_input_sample']
        )
        
        response = self._generate_response(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {'report': response}

    def analyze_security(self, code_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform security audit of the code
        
        Args:
            code_data: Output from CodeAnalyzer
            
        Returns:
            Security audit report
        """
        prompt = self.prompts.security_audit_prompt().format(
            code_summary=json.dumps(code_data['metadata'], indent=2),
            code_samples=code_data['llm_input_sample']
        )
        
        response = self._generate_response(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {'report': response}

    def analyze_performance(self, code_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze code performance characteristics
        
        Args:
            code_data: Output from CodeAnalyzer
            
        Returns:
            Performance analysis report
        """
        prompt = self.prompts.performance_review_prompt().format(
            code_summary=json.dumps(code_data['metadata'], indent=2),
            code_samples=code_data['llm_input_sample']
        )
        
        response = self._generate_response(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {'report': response}
            
    def generate_file_by_file_report(self, code_data):
        file_analysis_sections = []
        
        for dir_entry in code_data['metadata']['file_tree']:
            if dir_entry['directory']:
                file_analysis_sections.append(f"\n### Directory: {dir_entry['directory']}/")
            
            for file_info in dir_entry['files']:
                try:
                    file_key = file_info.get('key')
                    if not file_key or file_key not in code_data['files']:
                        continue
                    
                    file_data = code_data['files'][file_key]
                    
                    # Ensure all required fields exist
                    rel_path = file_data.get('rel_path', 'Unknown path')
                    language = file_data.get('language', 'Unknown language')
                    content = file_data.get('content', '')
                    size = file_data.get('size_bytes', 0)
                    
                    file_analysis_sections.append(
                        f"\n#### File: {rel_path}\n"
                        f"**Language**: {language}\n"
                        f"**Size**: {size} bytes\n"
                        f"```{language.lower() if language != 'Unknown language' else 'text'}\n"
                        f"{content[:500]}\n...\n```\n"
                        "**Analysis**:\n"
                    )
                except Exception as e:
                    logging.error(f"Error processing file {file_info.get('name', 'unknown')}: {e}")
                    continue
        
        prompt = self.prompts.file_by_file_prompt().format(
            file_count=code_data['metadata']['total_files'],
            languages=", ".join(code_data['metadata']['file_types'].keys()),
            file_analysis="\n".join(file_analysis_sections)
        )
        
        response = self._generate_response(prompt)
        return {'report': response}
