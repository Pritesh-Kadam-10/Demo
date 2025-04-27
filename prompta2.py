class Prompts:
    @staticmethod
    def analysis_prompt():
        return """Analyze code files and categorize issues by severity. Follow this structure:

        Critical Issues (Must Fix Immediately):
        - Security vulnerabilities
        - Crash risks
        - Data corruption possibilities
        - Unhandled exceptions
        - Type system violations
        
        Warning Issues (Should Fix):
        - Syntax inconsistencies
        - Deprecated functions
        - Resource leaks
        - Magic numbers/strings
        
        Code Style Issues (Recommended Fix):
        - Naming convention violations
        - Formatting inconsistencies
        - Typos in code/comments
        - Redundant code

        Format response EXACTLY like this:

        File: [relative_path]
        Language: [language]
        [Critical]: 
        - [Issue description] (line X)
        [Warning]: 
        - [Issue description] (line Y)
        [Style]: 
        - [Issue description] (line Z)

        After all files:
        CRITICAL SUMMARY:
        - Total critical issues: [number]
        - Most dangerous: [description]
        
        PRIORITY FIX ORDER:
        1. [Critical issue file+line]
        2. [Next critical issue]
        
        FILES ANALYZED:
        {files_analysis}
        
        Use this severity scale:
        Critical: Will cause crashes/security holes/data loss
        Warning: May cause unexpected behavior
        Style: Non-dangerous quality issues"""