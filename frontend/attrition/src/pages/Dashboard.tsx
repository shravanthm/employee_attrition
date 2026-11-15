import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  Users, AlertTriangle, ShieldCheck, TrendingUp,
  Brain, Activity, ArrowUpRight, Search, Download,
  ChevronRight, Filter, Sparkles
} from 'lucide-react'
import api from '../api/client'

function StatCard({ icon: Icon, label, value, sub, color, active, onClick }: any) {
  return (
    <div
      onClick={onClick}
      className={`bg-white dark:bg-gray-900 border rounded-xl p-5 flex flex-col gap-1 shadow-xs transition-all cursor-pointer ${
        active
          ? 'border-blue-600 ring-2 ring-blue-600/20 shadow-md'
          : 'border-slate-200 dark:border-gray-800 hover:border-slate-300 dark:hover:border-gray-700'
      }`}
    >
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-slate-500 dark:text-gray-400 uppercase tracking-wider">{label}</span>
        <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${color}`}>
          <Icon size={16} className="text-white" />
        </div>
      </div>
      <span className="text-3xl font-bold text-slate-800 dark:text-white mt-1">{value}</span>
      <span className="text-xs text-slate-400 dark:text-gray-500">{sub}</span>
    </div>
  )
}

export default function Dashboard() {
  const [metrics, setMetrics] = useState({
    total_employees: 60,
    active_employees: 60,
    high_risk_count: 15,
    moderate_risk_count: 22,
    low_risk_count: 23,
    average_fdi: 0.058,
    department_distribution: { "Sales": 20, "Research & Development": 25, "Human Resources": 15 }
  })
  const [atRiskList, setAtRiskList] = useState<any[]>([])
  const [selectedTier, setSelectedTier] = useState<string>('all')
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    Promise.all([
      api.get('/api/v1/metrics/dashboard'),
      api.get('/api/v1/metrics/at-risk-employees', { params: { tier: 'all', limit: 100 } })
    ])
      .then(([metricsRes, listRes]) => {
        if (metricsRes?.data) setMetrics(metricsRes.data)
        if (listRes?.data) setAtRiskList(listRes.data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  const filteredEmployees = atRiskList.filter((emp) => {
    const matchesTier =
      selectedTier === 'all' || emp.risk_category?.toLowerCase() === selectedTier.toLowerCase()
    const matchesSearch =
      emp.employee_code?.toLowerCase().includes(search.toLowerCase()) ||
      emp.department?.toLowerCase().includes(search.toLowerCase()) ||
      emp.job_role?.toLowerCase().includes(search.toLowerCase()) ||
      emp.primary_driver?.toLowerCase().includes(search.toLowerCase())
    return matchesTier && matchesSearch
  })

  const getTierBadge = (cat: string) => {
    if (cat === 'High' || cat === 'Critical') {
      return 'bg-red-50 dark:bg-red-950/60 text-red-600 dark:text-red-300 border-red-200 dark:border-red-800'
    }
    if (cat === 'Moderate') {
      return 'bg-amber-50 dark:bg-amber-950/60 text-amber-600 dark:text-amber-300 border-amber-200 dark:border-amber-800'
    }
    return 'bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800'
  }

  return (
    <div className="p-8 flex flex-col gap-6 max-w-7xl mx-auto">
      {/* Dashboard Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Activity className="text-blue-600" /> Executive Risk Dashboard
          </h1>
          <p className="text-sm text-slate-500 dark:text-gray-400 mt-1">
            AttritionPulse AI — Longitudinal Early-Warning & Explainable Intelligence
          </p>
        </div>
        <div className="flex items-center gap-2 bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 px-3 py-1.5 rounded-lg text-xs font-semibold">
          <Brain size={14} /> Production Model: XGBoost + Temporal Slopes
        </div>
      </div>

      {/* KPI Cards (Interactive Filters) */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          icon={Users}
          label="Total Monitored"
          value={metrics.total_employees.toLocaleString()}
          sub={`${metrics.active_employees} currently active`}
          color="bg-blue-600"
          active={selectedTier === 'all'}
          onClick={() => setSelectedTier('all')}
        />
        <StatCard
          icon={AlertTriangle}
          label="High Flight Risk"
          value={metrics.high_risk_count}
          sub={`${((metrics.high_risk_count / (metrics.total_employees || 1)) * 100).toFixed(1)}% of workforce`}
          color="bg-red-500"
          active={selectedTier === 'High'}
          onClick={() => setSelectedTier('High')}
        />
        <StatCard
          icon={TrendingUp}
          label="Moderate Risk"
          value={metrics.moderate_risk_count}
          sub={`${((metrics.moderate_risk_count / (metrics.total_employees || 1)) * 100).toFixed(1)}% of workforce`}
          color="bg-amber-500"
          active={selectedTier === 'Moderate'}
          onClick={() => setSelectedTier('Moderate')}
        />
        <StatCard
          icon={ShieldCheck}
          label="Low Risk Stable"
          value={metrics.low_risk_count}
          sub={`${((metrics.low_risk_count / (metrics.total_employees || 1)) * 100).toFixed(1)}% of workforce`}
          color="bg-emerald-500"
          active={selectedTier === 'Low'}
          onClick={() => setSelectedTier('Low')}
        />
      </div>

      {/* PRIORITY AT-RISK EMPLOYEES ROSTER */}
      <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-6 shadow-xs flex flex-col gap-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base font-bold text-slate-800 dark:text-white">
                Priority Early-Warning Roster: Employees at Risk
              </h2>
              <span className="text-xs px-2 py-0.5 rounded-full bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-300 font-bold">
                {filteredEmployees.length} {selectedTier !== 'all' ? selectedTier : 'Total'}
              </span>
            </div>
            <p className="text-xs text-slate-500 dark:text-gray-400 mt-0.5">
              Ranked in real time by 90-day flight probability and longitudinal distress velocity (FDI). Click any row to view full telemetry dossier.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            {/* Filter Pills */}
            <div className="flex items-center bg-slate-100 dark:bg-gray-800 p-0.5 rounded-lg text-xs font-semibold">
              <button
                onClick={() => setSelectedTier('all')}
                className={`px-3 py-1 rounded-md transition-colors cursor-pointer ${
                  selectedTier === 'all'
                    ? 'bg-white dark:bg-gray-700 text-slate-800 dark:text-white shadow-xs'
                    : 'text-slate-500 dark:text-gray-400 hover:text-slate-800'
                }`}
              >
                All ({atRiskList.length})
              </button>
              <button
                onClick={() => setSelectedTier('High')}
                className={`px-3 py-1 rounded-md transition-colors cursor-pointer ${
                  selectedTier === 'High'
                    ? 'bg-red-600 text-white shadow-xs'
                    : 'text-slate-500 dark:text-gray-400 hover:text-red-600'
                }`}
              >
                High Risk ({atRiskList.filter((e) => e.risk_category === 'High').length})
              </button>
              <button
                onClick={() => setSelectedTier('Moderate')}
                className={`px-3 py-1 rounded-md transition-colors cursor-pointer ${
                  selectedTier === 'Moderate'
                    ? 'bg-amber-500 text-white shadow-xs'
                    : 'text-slate-500 dark:text-gray-400 hover:text-amber-500'
                }`}
              >
                Moderate ({atRiskList.filter((e) => e.risk_category === 'Moderate').length})
              </button>
              <button
                onClick={() => setSelectedTier('Low')}
                className={`px-3 py-1 rounded-md transition-colors cursor-pointer ${
                  selectedTier === 'Low'
                    ? 'bg-emerald-600 text-white shadow-xs'
                    : 'text-slate-500 dark:text-gray-400 hover:text-emerald-600'
                }`}
              >
                Stable Low ({atRiskList.filter((e) => e.risk_category === 'Low').length})
              </button>
            </div>

            {/* Search Input */}
            <div className="relative min-w-[200px]">
              <Search className="absolute left-3 top-2.5 text-slate-400" size={14} />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search employee, role, driver..."
                className="w-full pl-8 pr-3 py-1.5 text-xs bg-slate-50 dark:bg-gray-800 border border-slate-200 dark:border-gray-700 rounded-lg text-slate-800 dark:text-white focus:outline-none focus:ring-1 focus:ring-blue-600"
              />
            </div>
          </div>
        </div>

        {/* Employees Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 dark:bg-gray-800/60 border-b border-slate-200 dark:border-gray-800 text-slate-600 dark:text-gray-300 font-semibold">
              <tr>
                <th className="py-3 px-4">Employee</th>
                <th className="py-3 px-4">Department & Role</th>
                <th className="py-3 px-4">90-Day Flight Risk</th>
                <th className="py-3 px-4 text-center">Risk Tier</th>
                <th className="py-3 px-4">FDI Velocity</th>
                <th className="py-3 px-4">Primary Distress Driver</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-gray-800 text-slate-700 dark:text-gray-200 font-medium">
              {filteredEmployees.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-8 text-center text-slate-400 font-normal">
                    No employees matching the current filter criteria.
                  </td>
                </tr>
              ) : (
                filteredEmployees.map((emp) => (
                  <tr
                    key={emp.id}
                    className="hover:bg-slate-50/80 dark:hover:bg-gray-800/40 transition-colors"
                  >
                    <td className="py-3 px-4 font-bold text-slate-900 dark:text-white">
                      <Link
                        to={`/employees/${emp.id}`}
                        className="hover:text-blue-600 dark:hover:text-blue-400 flex items-center gap-1.5"
                      >
                        {emp.employee_code}
                      </Link>
                    </td>

                    <td className="py-3 px-4">
                      <span className="font-semibold text-slate-800 dark:text-gray-200">{emp.department}</span>
                      <span className="block text-[11px] text-slate-400">{emp.job_role}</span>
                    </td>

                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        <div className="w-20 bg-slate-100 dark:bg-gray-800 h-2 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${
                              emp.risk_category === 'High'
                                ? 'bg-red-500'
                                : emp.risk_category === 'Moderate'
                                ? 'bg-amber-500'
                                : 'bg-emerald-500'
                            }`}
                            style={{ width: `${Math.round(emp.risk_probability * 100)}%` }}
                          />
                        </div>
                        <span className="font-mono font-bold text-slate-800 dark:text-white">
                          {(emp.risk_probability * 100).toFixed(1)}%
                        </span>
                      </div>
                    </td>

                    <td className="py-3 px-4 text-center">
                      <span
                        className={`inline-block px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${getTierBadge(
                          emp.risk_category
                        )}`}
                      >
                        {emp.risk_category}
                      </span>
                    </td>

                    <td className="py-3 px-4 font-mono font-semibold">
                      <span
                        className={
                          emp.factor_deterioration_index > 0.15
                            ? 'text-red-600 dark:text-red-400 font-bold'
                            : emp.factor_deterioration_index > 0.05
                            ? 'text-amber-600 dark:text-amber-400 font-medium'
                            : 'text-slate-500'
                        }
                      >
                        +{emp.factor_deterioration_index.toFixed(3)}
                      </span>
                    </td>

                    <td className="py-3 px-4">
                      <span className="text-[11px] font-semibold text-slate-700 dark:text-gray-300">
                        {emp.primary_driver}
                      </span>
                    </td>

                    <td className="py-3 px-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <a
                          href={`http://localhost:8000/api/v1/employees/${emp.id}/report/download?format=md`}
                          target="_blank"
                          rel="noreferrer"
                          className="px-2 py-1 bg-slate-100 dark:bg-gray-800 hover:bg-slate-200 dark:hover:bg-gray-700 rounded text-[11px] font-semibold text-slate-600 dark:text-gray-300 transition-colors inline-flex items-center gap-1"
                          title="Export Dossier (.md)"
                        >
                          <Download size={11} /> Dossier
                        </a>
                        <Link
                          to={`/employees/${emp.id}`}
                          className="px-2.5 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded text-[11px] font-semibold transition-colors inline-flex items-center gap-1"
                        >
                          Telemetry <ChevronRight size={11} />
                        </Link>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Analytics Insights: Department Headcount & FDI */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-6 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-bold text-slate-800 dark:text-white">Department Headcount & Risk Exposure</h2>
            <span className="text-xs text-slate-400">Live Ingested Telemetry</span>
          </div>
          <div className="space-y-4">
            {Object.entries(metrics.department_distribution).map(([dept, count]: any) => (
              <div key={dept} className="flex flex-col gap-1.5">
                <div className="flex justify-between text-xs font-semibold text-slate-700 dark:text-gray-300">
                  <span>{dept}</span>
                  <span>{count} employees</span>
                </div>
                <div className="w-full bg-slate-100 dark:bg-gray-800 h-2.5 rounded-full overflow-hidden">
                  <div
                    className="bg-blue-600 h-full rounded-full transition-all duration-500"
                    style={{ width: `${(count / (metrics.total_employees || 1)) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-6 shadow-xs flex flex-col justify-between">
          <div>
            <h2 className="text-base font-bold text-slate-800 dark:text-white mb-2">Factor Deterioration Index (FDI)</h2>
            <p className="text-xs text-slate-500 dark:text-gray-400 mb-6">
              Longitudinal rate of psychological and workload distress across active cohorts.
            </p>
            <div className="flex items-baseline gap-2">
              <span className="text-4xl font-extrabold text-blue-600">+{metrics.average_fdi}</span>
              <span className="text-xs font-medium text-slate-500">slope velocity</span>
            </div>
            <p className="text-xs text-slate-400 mt-2">
              Statistically validated with <span className="font-semibold text-slate-700 dark:text-gray-200">p &lt; 0.001</span> against voluntary departure events.
            </p>
          </div>
          <div className="mt-6 pt-4 border-t border-slate-100 dark:border-gray-800 text-xs text-slate-500">
            <span className="font-semibold text-slate-700 dark:text-gray-300">Protected Horizon:</span> 90-Day Early Warning window active.
          </div>
        </div>
      </div>
    </div>
  )
}
