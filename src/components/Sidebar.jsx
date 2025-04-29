import { useReports } from '../components/ReportsContext';
import { useNavigate } from 'react-router-dom';

export default function Sidebar() {
  const { files, activeFile, setActiveFile, loading } = useReports();
  const navigate = useNavigate();

  const handleFileSelect = (file) => {
    setActiveFile(file);
    navigate('/reports/summary');
  };

  return (
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
                  onClick={() => handleFileSelect(file)}
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
  );
}
