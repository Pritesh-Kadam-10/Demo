import { useState, useEffect } from 'react';

export default function CodeReviewReportUI() {
  const [files, setFiles] = useState([]);
  const [activeFile, setActiveFile] = useState(null);
  const [activeFileName, setActiveFileName] = useState(null);
  const [activeTab, setActiveTab] = useState('summary');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastPollTime, setLastPollTime] = useState(null);

  const API_ENDPOINT = 'http://172.25.10.159:9000/getPath';
  const POLL_INTERVAL = 900000; 

  const handleSetActiveFile = (file) => {
    setActiveFile(file);
    setActiveFileName(file.name);
  };

  const fetchReports = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(API_ENDPOINT);

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();

      processApiResponse(data);
      setLastPollTime(new Date());

    } catch (err) {
      console.error('Error fetching reports:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

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

      if (activeFileName) {
        const currentFile = processedFiles.find(file => file.name === activeFileName);
        if (currentFile) {
          if (!activeFile || activeFile.content !== currentFile.content) {
            setActiveFile(currentFile);
          }
        }
        // Don't reset to first file if not found!
      } else if (!activeFile) {
        setActiveFile(processedFiles[0]);
        setActiveFileName(processedFiles[0].name);
      }
    }
  };

  useEffect(() => {
    fetchReports(); // Only fetch once when component mounts
  }, []);
  

  const parseReviewReport = (content) => {
    const summaryMatch = content.match(/Total Critical Issues\s*:\s*(\d+)\nTotal Warnings\s*:\s*(\d+)\nTotal Style Issues\s*:\s*(\d+)/);
    const summary = summaryMatch ? {
      critical: parseInt(summaryMatch[1]),
      warnings: parseInt(summaryMatch[2]),
      style: parseInt(summaryMatch[3])
    } : { critical: 0, warnings: 0, style: 0 };

    const fileRegex = /========== File: ([^\s]+) \(([^)]+)\) ==========/g;
    const files = [];
    let match;

    while ((match = fileRegex.exec(content)) !== null) {
      const fileName = match[1];
      const fileType = match[2];
      const startIndex = match.index + match[0].length;
      const nextFileIndex = content.indexOf('==========', startIndex);
      const endIndex = nextFileIndex !== -1 ? nextFileIndex : content.length;
      const fileContent = content.substring(startIndex, endIndex).trim();

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
    const summaryIndex = sections.findIndex(s => s.includes('=== FOLDER COMPARISON SUMMARY ==='));
    const summary = summaryIndex !== -1 ? sections[summaryIndex] : '';

    const fileComparisons = [];

    sections.forEach(section => {
      const fileMatch = section.match(/--- Comparing File: ([^\s]+) ---\nDifference Percentage: ([^\s]+)%/);
      if (fileMatch) {
        const fileName = fileMatch[1];
        const diffPercentage = parseFloat(fileMatch[2]);
        const changesMatch = section.match(/Changes Detected: ([\s\S]+?)(?=\n\nAI Explanation|$)/);
        const changes = changesMatch ? changesMatch[1].trim() : '';
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

    return { summary, fileComparisons, addedFiles, removedFiles };
  };

  const renderFileContent = () => {
    if (!activeFile) {
      if (loading) return <div className="p-6 text-center text-gray-500">Loading reports...</div>;
      if (error) return <div className="p-6 text-center text-red-500">Error: {error}</div>;
      return <div className="p-6 text-center text-gray-500">No files available</div>;
    }

    if (activeFile.type === 'review') {
      const report = parseReviewReport(activeFile.content);

      if (activeTab === 'summary') {
        return (
          <div className="p-6">
            <h2 className="text-xl font-bold mb-4">Code Review Summary</h2>
            <div className="grid grid-cols-3 gap-4 mb-6">
              <div className="bg-red-100 p-4 rounded-lg">
                <h3 className="font-bold text-red-700">Critical Issues</h3>
                <p className="text-2xl font-bold text-red-700">{report.summary.critical}</p>
              </div>
              <div className="bg-yellow-100 p-4 rounded-lg">
                <h3 className="font-bold text-yellow-700">Warnings</h3>
                <p className="text-2xl font-bold text-yellow-700">{report.summary.warnings}</p>
              </div>
              <div className="bg-blue-100 p-4 rounded-lg">
                <h3 className="font-bold text-blue-700">Style Issues</h3>
                <p className="text-2xl font-bold text-blue-700">{report.summary.style}</p>
              </div>
            </div>

            <h3 className="text-lg font-bold mb-2">Priority Fix Order</h3>
            <div className="bg-gray-100 p-4 rounded-lg mb-6">
              {activeFile.content.includes('>>> PRIORITY FIX ORDER <<<') ? (
                <pre className="whitespace-pre-wrap">{
                  activeFile.content.split('>>> PRIORITY FIX ORDER <<<')[1]
                  .split('================================================================================')[0]
                  .trim()
                }</pre>
              ) : (
                <p>No priority fix order specified</p>
              )}
            </div>
          </div>
        );
      } else if (activeTab === 'files') {
        return (
          <div className="p-6">
            <h2 className="text-xl font-bold mb-4">File Analysis</h2>
            {report.files.map((file, index) => (
              <div key={index} className="mb-6 border rounded-lg overflow-hidden">
                <div className="bg-gray-100 p-3 border-b font-mono">{file.name} <span className="text-gray-500">({file.type})</span></div>
                <div className="p-4">
                  {file.issues.length > 0 ? (
                    <ul className="space-y-2">
                      {file.issues.map((issue, idx) => (
                        <li key={idx} className={`p-2 rounded ${
                          issue.type.includes('CRITICAL') ? 'bg-red-50' :
                          issue.type.includes('WARNING') ? 'bg-yellow-50' :
                          'bg-blue-50'
                        }`}>
                          <span className={`font-bold ${
                            issue.type.includes('CRITICAL') ? 'text-red-700' :
                            issue.type.includes('WARNING') ? 'text-yellow-700' :
                            'text-blue-700'
                          }`}>[{issue.type}]</span> {issue.description}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-gray-500">No issues found</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        );
      } else {
        return (
          <div className="p-6">
            <h2 className="text-xl font-bold mb-4">Raw Report</h2>
            <pre className="whitespace-pre-wrap bg-gray-100 p-4 rounded-lg text-sm font-mono overflow-auto max-h-screen">{activeFile.content}</pre>
          </div>
        );
      }
    } else if (activeFile.type === 'comparison') {
      const report = parseComparisonReport(activeFile.content);

      if (activeTab === 'summary') {
        return (
          <div className="p-6">
            <h2 className="text-xl font-bold mb-4">Comparison Summary</h2>
            <div className="bg-gray-100 p-4 rounded-lg mb-6 whitespace-pre-wrap">{report.summary}</div>
          </div>
        );
      } else if (activeTab === 'files') {
        return (
          <div className="p-6">
            <h2 className="text-xl font-bold mb-4">File Comparisons</h2>
            {report.fileComparisons.map((file, index) => (
              <div key={index} className="mb-6 border rounded-lg overflow-hidden">
                <div className="bg-gray-100 p-3 border-b">
                  <div className="flex justify-between items-center">
                    <span className="font-mono">{file.fileName}</span>
                    <span className={`px-2 py-1 rounded text-sm ${
                      file.diffPercentage > 50 ? 'bg-red-100 text-red-700' :
                      file.diffPercentage > 20 ? 'bg-yellow-100 text-yellow-700' :
                      'bg-green-100 text-green-700'
                    }`}>
                      Difference: {file.diffPercentage}%
                    </span>
                  </div>
                </div>
                <div className="p-4">
                  <h3 className="font-bold mb-2">Changes</h3>
                  <pre className="whitespace-pre-wrap bg-gray-50 p-3 rounded-lg mb-4 text-sm font-mono overflow-auto">{file.changes}</pre>

                  <h3 className="font-bold mb-2">AI Explanation</h3>
                  <div className="bg-blue-50 p-3 rounded-lg whitespace-pre-wrap">{file.explanation}</div>
                </div>
              </div>
            ))}
          </div>
        );
      } else {
        return (
          <div className="p-6">
            <h2 className="text-xl font-bold mb-4">Raw Report</h2>
            <pre className="whitespace-pre-wrap bg-gray-100 p-4 rounded-lg text-sm font-mono overflow-auto max-h-screen">{activeFile.content}</pre>
          </div>
        );
      }
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <header className="bg-gray-800 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Code Review Reports</h1>
          <div className="flex items-center">
            {lastPollTime && (
              <div className="mr-4 text-sm text-gray-300">
                Last updated: {lastPollTime.toLocaleTimeString()}
              </div>
            )}
            <button 
              onClick={fetchReports}
              disabled={loading}
              className={`bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded cursor-pointer ${loading ? 'opacity-50' : ''}`}
            >
              {loading ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        <div className="w-64 bg-gray-100 border-r overflow-y-auto">
          <div className="p-4">
            <h2 className="text-lg font-bold mb-2">Files</h2>
            {files.length === 0 ? (
              loading ? (
                <p className="text-gray-500 text-sm">Loading reports...</p>
              ) : (
                <p className="text-gray-500 text-sm">No reports available</p>
              )
            ) : (
              <ul className="space-y-1">
                {files.map((file, index) => (
                  <li key={index}>
                    <button
                      className={`w-full text-left p-2 rounded text-sm ${
                        activeFile && activeFile.name === file.name ? 'bg-blue-100 text-blue-700' : 'hover:bg-gray-200'
                      }`}
                      onClick={() => {
                        handleSetActiveFile(file);
                        if (file.type !== activeFile?.type) {
                          setActiveTab('summary');
                        }
                      }}
                    >
                      <div className="font-medium truncate">{file.name}</div>
                      <div className="text-xs text-gray-500">
                        {file.type === 'review' ? 'Code Review Report' : 'Comparison Report'}
                      </div>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        <div className="flex-1 flex flex-col overflow-hidden">
          {activeFile && (
            <div className="bg-white border-b">
              <div className="flex">
                <button
                  className={`px-4 py-3 text-sm font-medium ${
                    activeTab === 'summary' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
                  }`}
                  onClick={() => setActiveTab('summary')}
                >
                  Summary
                </button>
                <button
                  className={`px-4 py-3 text-sm font-medium ${
                    activeTab === 'files' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
                  }`}
                  onClick={() => setActiveTab('files')}
                >
                  File Analysis
                </button>
                <button
                  className={`px-4 py-3 text-sm font-medium ${
                    activeTab === 'raw' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
                  }`}
                  onClick={() => setActiveTab('raw')}
                >
                  Raw Report
                </button>
              </div>
            </div>
          )}

          <div className="flex-1 overflow-y-auto">
            {renderFileContent()}
          </div>
        </div>
      </div>

      {loading && (
        <div className="fixed bottom-4 right-4 bg-blue-600 text-white px-3 py-2 rounded-full shadow-lg">
          <div className="flex items-center">
            <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Fetching reports...
          </div>
        </div>
      )}
    </div>
  );
}
