import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import ReportSummary from './components/ReportSummary';
import FileAnalysis from './components/FileAnalysis';
import RawReport from './components/RawReport';
import { ReportsProvider } from './components/ReportsContext';

export default function App() {
  return (
    <ReportsProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Navigate to="/reports" replace />} />
          <Route path="/reports" element={<Layout />}>
            <Route index element={<Navigate to="summary" replace />} />
            <Route path="summary" element={<ReportSummary />} />
            <Route path="files" element={<FileAnalysis />} />
            <Route path="raw" element={<RawReport />} />
          </Route>
        </Routes>
      </Router>
    </ReportsProvider>
  );
}