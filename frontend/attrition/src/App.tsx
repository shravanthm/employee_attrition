import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Employees from './pages/Employees'
import EmployeeProfile from './pages/EmployeeProfile'
import Predictions from './pages/Predictions'
import Interventions from './pages/Interventions'
import Reports from './pages/Reports'
import Chat from './pages/Chat'
import Upload from './pages/Upload'
import Layout from './components/Layout'

export default function App() {
  const [darkMode, setDarkMode] = useState(false)

  return (
    <div className={darkMode ? 'dark' : ''}>
      <div className="min-h-screen bg-slate-50 dark:bg-gray-950 transition-colors duration-200">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Layout darkMode={darkMode} setDarkMode={setDarkMode} />}>
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="employees" element={<Employees />} />
              <Route path="employees/:id" element={<EmployeeProfile />} />
              <Route path="predictions" element={<Predictions />} />
              <Route path="interventions" element={<Interventions />} />
              <Route path="reports" element={<Reports />} />
              <Route path="chat" element={<Chat />} />
              <Route path="upload" element={<Upload />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </div>
    </div>
  )
}
