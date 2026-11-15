import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Search, ChevronRight, User, Download } from 'lucide-react'
import api, { API_BASE_URL } from '../api/client'

export default function Employees() {
  const [employees, setEmployees] = useState([])
  const [search, setSearch] = useState('')
  const [department, setDepartment] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.get('/api/v1/employees', {
      params: { limit: 100, department: department || undefined }
    })
      .then((res) => {
        setEmployees(res.data)
        setLoading(false)
      })
      .catch(() => {
        // Fallback demo data if backend connection pending
        setEmployees([
          { id: 1, employee_code: 'EMP-0001', department: 'Sales', job_role: 'Sales Executive', employment_status: 'Active', hire_date: '2022-04-12' },
          { id: 2, employee_code: 'EMP-0002', department: 'Research & Development', job_role: 'Research Scientist', employment_status: 'Active', hire_date: '2021-08-01' },
          { id: 3, employee_code: 'EMP-0003', department: 'Human Resources', job_role: 'Manager', employment_status: 'Active', hire_date: '2020-02-15' },
          { id: 4, employee_code: 'EMP-0004', department: 'Research & Development', job_role: 'Laboratory Technician', employment_status: 'Terminated', hire_date: '2023-01-10' },
        ])
        setLoading(false)
      })
  }, [department])

  const filtered = employees.filter((e) =>
    e.employee_code?.toLowerCase().includes(search.toLowerCase()) ||
    e.job_role?.toLowerCase().includes(search.toLowerCase()) ||
    e.department?.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="p-8 flex flex-col gap-6 max-w-6xl mx-auto">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Employee Directory</h1>
          <p className="text-sm text-slate-500 dark:text-gray-400 mt-1">
            Access master profiles, longitudinal factor observations, and historical predictions.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
            className="text-xs p-2.5 rounded-lg border border-slate-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-slate-700 dark:text-gray-200"
          >
            <option value="">All Departments</option>
            <option value="Sales">Sales</option>
            <option value="Research & Development">Research & Development</option>
            <option value="Human Resources">Human Resources</option>
          </select>
          <div className="relative">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search code or role..."
              className="pl-8 pr-4 py-2 text-xs bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-700 rounded-lg text-slate-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl overflow-hidden shadow-sm">
        {loading ? (
          <div className="p-12 text-center text-xs text-slate-400">Loading directory...</div>
        ) : (
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="bg-slate-50 dark:bg-gray-800/60 border-b border-slate-100 dark:border-gray-800 text-slate-500 font-semibold">
                <th className="py-3 px-4">Code</th>
                <th className="py-3 px-4">Department</th>
                <th className="py-3 px-4">Job Role</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Hire Date</th>
                <th className="py-3 px-4 text-right">Telemetry Profile</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-gray-800 font-medium">
              {filtered.map((emp) => (
                <tr key={emp.id} className="hover:bg-slate-50/50 dark:hover:bg-gray-800/40">
                  <td className="py-3 px-4 font-bold text-slate-900 dark:text-white">{emp.employee_code}</td>
                  <td className="py-3 px-4 text-slate-700 dark:text-gray-300">{emp.department}</td>
                  <td className="py-3 px-4 text-slate-600 dark:text-gray-400">{emp.job_role}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                      emp.employment_status === 'Active' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600'
                    }`}>
                      {emp.employment_status}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-slate-500">{emp.hire_date}</td>
                  <td className="py-3 px-4 text-right">
                    <div className="flex items-center justify-end gap-3">
                      <a
                        href={`${API_BASE_URL}/api/v1/employees/${emp.id}/report/download?format=md`}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1 text-[11px] font-semibold text-slate-500 hover:text-blue-600 dark:hover:text-blue-400"
                        title="Download Dossier (.md)"
                      >
                        <Download size={12} /> Dossier
                      </a>
                      <Link
                        to={`/employees/${emp.id}`}
                        className="inline-flex items-center gap-1 text-xs font-bold text-blue-600 hover:text-blue-700"
                      >
                        View Profile <ChevronRight size={13} />
                      </Link>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
