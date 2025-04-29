import { useReports } from '../components/ReportsContext';

export default function FileAnalysis() {
  const { activeFile, loading, error, parseReviewReport, parseComparisonReport } = useReports();

  if (!activeFile) {
    if (loading) {
      return <div className="p-6 text-center text-gray-500">Loading reports...</div>;
    }
    if (error) {
      return <div className="p-6 text-center text-red-500">Error: {error}</div>;
    }
    return <div className="p-6 text-center text-gray-500">No files available</div>;
  }

  if (activeFile.type === 'review') {
    const report = parseReviewReport(activeFile.content);
    
    return (
      <div className="p-6">
        <h2 className="text-xl font-bold mb-4">File Analysis</h2>
        {report.files.map((file, index) => (
          <div key={index} className="mb-6 border rounded-lg overflow-hidden">
            <div className="bg-gray-100 p-3 border-b font-mono">
              {file.name} <span className="text-gray-500">({file.type})</span>
            </div>
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
  } else if (activeFile.type === 'comparison') {
    const report = parseComparisonReport(activeFile.content);
    
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
  }
}