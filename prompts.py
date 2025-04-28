class Prompts:
    @staticmethod
    def code_quality_prompt():
        return """
        You are a Senior Code Quality Analyst reviewing this codebase. Perform a thorough analysis focusing on:
        
        Codebase Metadata:
        {code_summary}
        
        Code Samples:
        {code_samples}
        
        Review Criteria:
        1. **Code Standards Compliance**
           - Language-specific style guidelines
           - Naming conventions
           - Consistent formatting
           - Proper file organization
        
        2. **Code Quality Metrics**
           - Cyclomatic complexity
           - Code duplication
           - Proper abstraction levels
           - Module cohesion
        
        3. **Best Practices**
           - Error handling
           - Resource management
           - Security practices
           - Documentation quality
        
        4. **Improvement Recommendations**
           - Specific refactoring suggestions
           - Code smells to address
           - Tools to adopt (linters, formatters)
        
        Output Format (Markdown):
        # Code Quality Report
        
        ## Standards Compliance (Rating: X/10)
        - [Language-specific findings]
        - [Naming convention issues]
        - [Formatting inconsistencies]
        
        ## Quality Metrics
        - [Complexity analysis]
        - [Duplication findings]
        
        ## Best Practices Assessment
        - [Error handling evaluation]
        - [Security practices]
        
        ## Actionable Recommendations
        - [High priority improvements]
        - [Medium priority improvements]
        """

    @staticmethod
    def security_audit_prompt():
        return """
        You are a Security Code Reviewer analyzing this codebase for vulnerabilities.
        
        Codebase Metadata:
        {code_summary}
        
        Code Samples:
        {code_samples}
        
        Focus Areas:
        1. **OWASP Top 10 Compliance**
        2. **Input Validation**
        3. **Authentication/Authorization**
        4. **Data Protection**
        5. **Error Handling**
        6. **Dependency Security**
        
        Report Format:
        # Security Audit Report
        
        ## Critical Vulnerabilities (Risk: High)
        - [Vulnerability 1]
          - Location: [file:line]
          - Description: 
          - Recommendation:
        
        ## Important Issues (Risk: Medium)
        - [Issue 1]
          - Location: [file:line]
          - Description:
          - Recommendation:
        
        ## Security Score: X/10
        [Overall assessment with justification]
        """

    @staticmethod
    def performance_review_prompt():
        return """
        You are a Performance Code Reviewer analyzing this codebase for efficiency.
        
        Codebase Info:
        {code_summary}
        
        Code Samples:
        {code_samples}
        
        Analysis Focus:
        1. **Algorithm Efficiency**
        2. **Memory Management**
        3. **I/O Operations**
        4. **Concurrency Patterns**
        5. **Database Interactions**
        
        Output Format:
        # Performance Review
        
        ## Critical Bottlenecks
        - [Issue 1 with location]
        - [Impact analysis]
        - [Suggested optimization]
        
        ## Optimization Opportunities
        - [Area 1]
        - [Area 2]
        
        ## Performance Score: X/10
        [Detailed justification]
        """
        

    @staticmethod
    def file_by_file_prompt():
        return """
        Analyze each file in sequence and provide detailed report following this structure:

        For each file:
        1. File path: {file_path}
        2. Language: {language}
        3. Code Structure Analysis
        4. Potential Issues
        5. Quality Assessment (1-10)
        6. Recommendations

        Output Format (Markdown):
        # File-by-File Analysis Report
        
        ## Codebase Overview
        - Total Files: {file_count}
        - Languages: {languages}
        
        ## Detailed Analysis
        {file_analysis}
        
        ## Summary
        - Overall Quality Score: X/10
        - Critical Issues Found: X
        - Key Recommendations
        """
