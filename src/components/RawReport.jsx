import { useReports } from '../components/ReportsContext';

export default function RawReport() {
  const { activeFile, loading, error } = useReports();

  if (!activeFile) {
    if (loading) {
      return <div className="p-6 text-center text-gray-500">Loading reports...</div>;
    }
    if (error) {
      return <div className="p-6 text-center text-red-500">Error: {error}</div>;
    }
    return <div className="p-6 text-center text-gray-500">No files available</div>;
  }

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Raw Report</h2>
      <pre className="whitespace-pre-wrap bg-gray-100 p-4 rounded-lg text-sm font-mono overflow-auto max-h-screen">
        {activeFile.content}
      </pre>
    </div>
  );
}