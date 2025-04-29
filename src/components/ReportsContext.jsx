import { createContext, useState, useEffect, useContext } from 'react';

const ReportsContext = createContext();

export function ReportsProvider({ children }) {
  const [files, setFiles] = useState([]);
  const [activeFile, setActiveFile] = useState(null);
  const [activeFileName, setActiveFileName] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastPollTime, setLastPollTime] = useState(null);

  // API endpoint - replace with your actual endpoint
  const API_ENDPOINT = 'http://172.25.10.159:9000/getPath';
  const POLL_INTERVAL = 10000; // Poll every 10 seconds

  // Function to handle setting active file
  const handleSetActiveFile = (file) => {
    setActiveFile(file);
    setActiveFileName(file.name);
  };

  // Function to fetch reports from API
  const fetchReports = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(API_ENDPOINT);
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Process the received JSON data
      processApiResponse(data);
      setLastPollTime(new Date());
      
    } catch (err) {
      console.error('Error fetching reports:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Process the API response into the format expected by the UI
  const processApiResponse = (data) => {
    if (!data || !data.files) return;
    
    const processedFiles = Object.entries(data.files).map(([filename, content]) => {
      return {
        name: filename,
        content: content,
        type: filename.includes('comparison') ? 'comparison' : 'review'
      };
    });
    
    if (processedFiles.length > 0) {
      setFiles(processedFiles);
      
      // If we have an activeFileName, try to preserve it
      if (activeFileName) {
        const currentFile = processedFiles.find(file => file.name === activeFileName);
        if (currentFile) {
          setActiveFile(currentFile);
        } else if (!activeFile) {
          // If we can't find the file or no file is active, default to first
          setActiveFile(processedFiles[0]);
          setActiveFileName(processedFiles[0].name);
        }
      } else if (!activeFile) {
        // Initial setup, no file is active yet
        setActiveFile(processedFiles[0]);
        setActiveFileName(processedFiles[0].name);
      }
    }
  };

  // Set up polling
  useEffect(() => {
    fetchReports(); // Only fetch once when component mounts
  }, []);
    
//     // Set up polling interval
//     const intervalId = setInterval(fetchReports, POLL_INTERVAL);
    
//     // Clean up interval on component unmount
//     return () => clearInterval(intervalId);
//   }, []);

  // Helper functions for parsing reports
  const parseReviewReport = (content) => {
    const lines = content.split('\n');
    
    // Extract summary data
    const summaryMatch = content.match(/Total Critical Issues\s*:\s*(\d+)\nTotal Warnings\s*:\s*(\d+)\nTotal Style Issues\s*:\s*(\d+)/);
    const summary = summaryMatch ? {
      critical: parseInt(summaryMatch[1]),
      warnings: parseInt(summaryMatch[2]),
      style: parseInt(summaryMatch[3])
    } : { critical: 0, warnings: 0, style: 0 };
    
    // Extract files
    const fileRegex = /========== File: ([^\s]+) \(([^)]+)\) ==========/g;
    const files = [];
    let match;
    
    while ((match = fileRegex.exec(content)) !== null) {
      const fileName = match[1];
      const fileType = match[2];
      const startIndex = match.index + match[0].length;
      
      // Find the end of this file section
      const nextFileIndex = content.indexOf('==========', startIndex);
      const endIndex = nextFileIndex !== -1 ? nextFileIndex : content.length;
      
      const fileContent = content.substring(startIndex, endIndex).trim();
      
      // Parse issues
      const issues = [];
      const issueRegex = /\[([^\]]+)\]\s*(.*)/g;
      let issueMatch;
      
      while ((issueMatch = issueRegex.exec(fileContent)) !== null) {
        issues.push({
          type: issueMatch[1],
          description: issueMatch[2]
        });
      }
      
      files.push({
        name: fileName,
        type: fileType,
        issues
      });
    }
    
    return { summary, files };
  };

  const parseComparisonReport = (content) => {
    const sections = content.split('==================================================');
    
    // Extract the general summary
    const summaryIndex = sections.findIndex(s => s.includes('=== FOLDER COMPARISON SUMMARY ==='));
    const summary = summaryIndex !== -1 ? sections[summaryIndex] : '';
    
    // Extract file comparisons
    const fileComparisons = [];
    
    sections.forEach(section => {
      const fileMatch = section.match(/--- Comparing File: ([^\s]+) ---\nDifference Percentage: ([^\s]+)%/);
      if (fileMatch) {
        const fileName = fileMatch[1];
        const diffPercentage = parseFloat(fileMatch[2]);
        
        // Find the changes part
        const changesMatch = section.match(/Changes Detected: ([\s\S]+?)(?=\n\nAI Explanation|$)/);
        const changes = changesMatch ? changesMatch[1].trim() : '';
        
        // Find the AI explanation
        const explanationMatch = section.match(/AI Explanation of Changes:([\s\S]+?)(?=\n====================|$)/);
        const explanation = explanationMatch ? explanationMatch[1].trim() : '';
        
        fileComparisons.push({
          fileName,
          diffPercentage,
          changes,
          explanation
        });
      }
    });
    
    // Extract added and removed files
    const addedFilesMatch = content.match(/=== ADDED PY FILES ===[\s\S]+?Total added files: (\d+)([\s\S]+?)(?===|$)/);
    const removedFilesMatch = content.match(/=== REMOVED PY FILES ===[\s\S]+?Total removed files: (\d+)([\s\S]+?)(?===|$)/);
    
    const addedFiles = addedFilesMatch ? {
      count: parseInt(addedFilesMatch[1]),
      files: addedFilesMatch[2].split('\n').filter(line => line.startsWith('- ')).map(line => line.substring(2))
    } : { count: 0, files: [] };
    
    const removedFiles = removedFilesMatch ? {
      count: parseInt(removedFilesMatch[1]),
      files: removedFilesMatch[2].split('\n').filter(line => line.startsWith('- ')).map(line => line.substring(2))
    } : { count: 0, files: [] };
    
    return { 
      summary, 
      fileComparisons,
      addedFiles,
      removedFiles
    };
  };

  const value = {
    files,
    activeFile,
    setActiveFile: handleSetActiveFile,
    loading,
    error,
    lastPollTime,
    fetchReports,
    parseReviewReport,
    parseComparisonReport
  };

  return (
    <ReportsContext.Provider value={value}>
      {children}
    </ReportsContext.Provider>
  );
}

export const useReports = () => useContext(ReportsContext);