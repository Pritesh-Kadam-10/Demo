import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { useReports } from '../components/ReportsContext';
import Sidebar from './Sidebar';

export default function Layout() {
  const { activeFile, loading, lastPollTime, fetchReports } = useReports();
  const navigate = useNavigate();
  const location = useLocation();
  
  const getActiveTab = () => {
    const path = location.pathname;
    if (path.includes('/summary')) return 'summary';
    if (path.includes('/files')) return 'files';
    if (path.includes('/raw')) return 'raw';
    return 'summary';
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
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
      
      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <Sidebar />
        
        {/* Content */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Tabs */}
          {activeFile && (
            <div className="bg-white border-b">
              <div className="flex">
                <button
                  className={`px-4 py-3 text-sm font-medium ${
                    getActiveTab() === 'summary' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
                  }`}
                  onClick={() => navigate('/reports/summary')}
                >
                  Summary
                </button>
                <button
                  className={`px-4 py-3 text-sm font-medium ${
                    getActiveTab() === 'files' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
                  }`}
                  onClick={() => navigate('/reports/files')}
                >
                  File Analysis
                </button>
                <button
                  className={`px-4 py-3 text-sm font-medium ${
                    getActiveTab() === 'raw' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
                  }`}
                  onClick={() => navigate('/reports/raw')}
                >
                  Raw Report
                </button>
              </div>
            </div>
          )}
          
          {/* Content Area */}
          <div className="flex-1 overflow-y-auto">
            <Outlet />
          </div>
        </div>
      </div>
      
      {/* Status Indicator */}
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