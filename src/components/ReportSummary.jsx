import { useReports } from '../components/ReportsContext';

export default function ReportSummary() {
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
          {activeFile.content.includes('>>> PRIORITY FIX ORDER <<<') ? 
            <pre className="whitespace-pre-wrap">{
              activeFile.content.split('>>> PRIORITY FIX ORDER <<<')[1]
              .split('================================================================================')[0]
              .trim()
            }</pre> : 
            <p>No priority fix order specified</p>
          }
        </div>
      </div>
    );
  } else if (activeFile.type === 'comparison') {
    const report = parseComparisonReport(activeFile.content);
    
    return (
      <div className="p-6">
        <h2 className="text-xl font-bold mb-4">Comparison Summary</h2>
        <div className="bg-gray-100 p-4 rounded-lg mb-6 whitespace-pre-wrap">
          {report.summary}
        </div>
        
        <div className="grid grid-cols-2 gap-6">
          <div className="border rounded-lg overflow-hidden">
            <div className="bg-green-100 p-3 border-b">
              <h3 className="font-bold text-green-700">Added Files ({report.addedFiles.count})</h3>
            </div>
            <div className="p-4">
              {report.addedFiles.files.length > 0 ? (
                <ul className="list-disc pl-5">
                  {report.addedFiles.files.map((file, idx) => (
                    <li key={idx} className="font-mono">{file}</li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500">No files added</p>
              )}
            </div>
          </div>
          
          <div className="border rounded-lg overflow-hidden">
            <div className="bg-red-100 p-3 border-b">
              <h3 className="font-bold text-red-700">Removed Files ({report.removedFiles.count})</h3>
            </div>
            <div className="p-4">
              {report.removedFiles.files.length > 0 ? (
                <ul className="list-disc pl-5">
                  {report.removedFiles.files.map((file, idx) => (
                    <li key={idx} className="font-mono">{file}</li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500">No files removed</p>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }
}