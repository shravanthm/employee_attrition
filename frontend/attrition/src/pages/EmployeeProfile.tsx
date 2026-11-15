import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import {
  User, ArrowLeft, Brain, TrendingDown, Clock,
  Calendar, Briefcase, MapPin, Activity, Download,
  Printer, FileText, FileSpreadsheet
} from 'lucide-react'
import api from '../api/client'
import { Employee, MonthlySnapshot, PredictionResult, SurvivalResult } from '../types'

export default function EmployeeProfile() {
  const { id } = useParams<{ id: string }>()
  const empId = id || '1'

  const [employee, setEmployee] = useState<Employee | null>(null)
  const [snapshots, setSnapshots] = useState<MonthlySnapshot[]>([])
  const [prediction, setPrediction] = useState<PredictionResult | null>(null)
  const [survival, setSurvival] = useState<SurvivalResult | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    Promise.all([
      api.get(`/api/v1/employees/${empId}`).catch(() => null),
      api.get(`/api/v1/employees/${empId}/snapshots`).catch(() => null),
      api.post(`/api/v1/predictions/${empId}`).catch(() => null),
      api.get(`/api/v1/survival/${empId}`).catch(() => null)
    ]).then(([eRes, sRes, pRes, survRes]) => {
      if (eRes?.data) setEmployee(eRes.data)
      if (sRes?.data) setSnapshots(sRes.data)
      if (pRes?.data) setPrediction(pRes.data)
      if (survRes?.data) setSurvival(survRes.data)
      setLoading(false)
    })
  }, [empId])

  const downloadReport = (format: 'md' | 'json' | 'csv') => {
    window.open(`http://localhost:8000/api/v1/employees/${empId}/report/download?format=${format}`, '_blank')
  }

  const printDossier = () => {
    window.print()
  }

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh] text-sm text-slate-500">
        Loading comprehensive employee telemetry...
      </div>
    )
  }

  const getTierColor = (cat?: string) => {
    if (cat === 'Critical' || cat === 'High') return 'text-red-600 bg-red-50 border-red-200'
    if (cat === 'Moderate') return 'text-amber-600 bg-amber-50 border-amber-200'
    return 'text-emerald-600 bg-emerald-50 border-emerald-200'
  }

  return (
    <div className="p-8 flex flex-col gap-6 max-w-6xl mx-auto print:p-0 print:max-w-full">
      {/* Top Navigation & Action Buttons */}
      <div className="flex items-center justify-between print:hidden">
        <Link to="/employees" className="flex items-center gap-1.5 text-xs font-semibold text-blue-600 hover:underline">
          <ArrowLeft size={14} /> Back to Employee Directory
        </Link>

        {/* Export & Download Controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => downloadReport('md')}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-xs transition-colors cursor-pointer"
            title="Download full executive report as Markdown"
          >
            <Download size={13} /> Download Dossier (.md)
          </button>

          <button
            onClick={() => downloadReport('csv')}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-white dark:bg-gray-800 border border-slate-200 dark:border-gray-700 hover:bg-slate-50 dark:hover:bg-gray-700 text-slate-700 dark:text-gray-200 text-xs font-semibold rounded-lg shadow-xs transition-colors cursor-pointer"
            title="Download monthly telemetry history as CSV"
          >
            <FileSpreadsheet size={13} className="text-emerald-600 dark:text-emerald-400" /> Export CSV
          </button>

          <button
            onClick={printDossier}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-white dark:bg-gray-800 border border-slate-200 dark:border-gray-700 hover:bg-slate-50 dark:hover:bg-gray-700 text-slate-700 dark:text-gray-200 text-xs font-semibold rounded-lg shadow-xs transition-colors cursor-pointer"
            title="Print or Save as PDF"
          >
            <Printer size={13} /> Print / Save PDF
          </button>
        </div>
      </div>

      {/* Header Profile Bar */}
      <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-full bg-blue-100 dark:bg-blue-950 flex items-center justify-center text-blue-600 font-bold text-lg">
            <User size={24} />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-slate-900 dark:text-white">
                {employee?.employee_code || `EMP-${empId.padStart(4, '0')}`}
              </h1>
              <span className={`text-xs font-semibold px-2.5 py-0.5 rounded-full border ${getTierColor(prediction?.risk_category)}`}>
                {prediction?.risk_category || 'Low'} Risk
              </span>
            </div>
            <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500 mt-1">
              <span className="flex items-center gap-1"><Briefcase size={12} /> {employee?.department || 'R&D'} — {employee?.job_role || 'Scientist'}</span>
              <span className="flex items-center gap-1"><MapPin size={12} /> {employee?.location || 'HQ Office'}</span>
              <span className="flex items-center gap-1"><Calendar size={12} /> Hired: {employee?.hire_date || '2023-01-15'}</span>
            </div>
          </div>
        </div>

        {/* 90-Day Probability */}
        <div className="flex items-center gap-6 bg-slate-50 dark:bg-gray-800/50 px-5 py-3 rounded-xl">
          <div>
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">90-Day Flight Risk</span>
            <span className="text-2xl font-extrabold text-slate-800 dark:text-white">
              {prediction ? `${(prediction.risk_probability * 100).toFixed(1)}%` : '—'}
            </span>
          </div>
          {survival?.median_survival_days && (
            <div className="border-l border-slate-200 dark:border-gray-700 pl-4">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">Median Survival</span>
              <span className="text-sm font-bold text-slate-700 dark:text-gray-300">
                {survival.median_survival_days} Days
              </span>
            </div>
          )}
        </div>
      </div>

      {/* SHAP & Flight Risk Attribution */}
      {prediction?.top_explanations && (
        <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-6 shadow-sm">
          <h2 className="text-sm font-bold text-slate-900 dark:text-white mb-1 flex items-center gap-1.5">
            <Brain size={16} className="text-blue-600" /> Explainable Risk Drivers (SHAP Attribution)
          </h2>
          <p className="text-xs text-slate-500 mb-4">Features pushing risk probability up (+) or down (-).</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {prediction.top_explanations.map((exp, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 rounded-lg bg-slate-50 dark:bg-gray-800/60 text-xs">
                <span className="font-semibold text-slate-700 dark:text-gray-300 capitalize">
                  {exp.feature.replace(/_/g, ' ')}
                </span>
                <div className="flex items-center gap-2">
                  <span className="font-mono font-bold text-slate-600 dark:text-gray-400">
                    {exp.shap_value > 0 ? `+${exp.shap_value.toFixed(3)}` : exp.shap_value.toFixed(3)}
                  </span>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                    exp.impact === 'Increases Risk' ? 'bg-red-100 text-red-700 dark:bg-red-950/60 dark:text-red-300' : 'bg-emerald-100 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300'
                  }`}>
                    {exp.impact}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 12-Factor Monthly Snapshots Telemetry Table */}
      <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-6 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-1.5">
              <Activity size={16} className="text-blue-600" /> Longitudinal Factor Observations
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Monthly telemetry across key organizational satisfaction, workload, and wellbeing factors.
            </p>
          </div>
          <button
            onClick={() => downloadReport('csv')}
            className="flex items-center gap-1 px-2.5 py-1 text-[11px] font-medium border border-slate-200 dark:border-gray-700 hover:bg-slate-50 dark:hover:bg-gray-800 rounded text-slate-600 dark:text-gray-300 transition-colors cursor-pointer print:hidden"
          >
            <Download size={11} /> Download Table (.csv)
          </button>
        </div>

        {snapshots.length === 0 ? (
          <p className="text-xs text-slate-400">No monthly telemetry records currently populated for this employee.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-100 dark:border-gray-800 text-slate-400 font-semibold">
                  <th className="pb-3">Month</th>
                  <th className="pb-3">Job Sat (1-5)</th>
                  <th className="pb-3">Work-Life (1-5)</th>
                  <th className="pb-3">Overtime (Hrs)</th>
                  <th className="pb-3">Manager Support</th>
                  <th className="pb-3">Stress (1-5)</th>
                  <th className="pb-3">Absence Rate</th>
                  <th className="pb-3">FDI</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-gray-800 font-medium font-mono text-slate-700 dark:text-gray-300">
                {snapshots.map((s) => (
                  <tr key={s.id} className="hover:bg-slate-50/50 dark:hover:bg-gray-800/40">
                    <td className="py-2.5 font-bold font-sans text-slate-800 dark:text-white">{s.snapshot_month}</td>
                    <td className="py-2.5">{s.job_satisfaction_score ?? '—'}</td>
                    <td className="py-2.5">{s.work_life_balance_score ?? '—'}</td>
                    <td className="py-2.5">{s.overtime_hours} hrs</td>
                    <td className="py-2.5">{s.manager_support_score ?? '—'}</td>
                    <td className="py-2.5">{s.stress_score ?? '—'}</td>
                    <td className="py-2.5">{s.absence_rate}%</td>
                    <td className="py-2.5">
                      <span className={`text-xs ${Number(s.factor_deterioration_index) > 0 ? 'text-red-500 font-bold' : 'text-slate-500'}`}>
                        {s.factor_deterioration_index != null ? s.factor_deterioration_index.toFixed(3) : '0.000'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
