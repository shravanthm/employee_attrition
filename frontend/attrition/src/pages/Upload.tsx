import React, { useState, useRef } from 'react'
import { Upload as UploadIcon, FileText, CheckCircle, AlertCircle, Info } from 'lucide-react'
import api from '../api/client'

export default function Upload() {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [result, setResult] = useState<{ status: string; message: string; employees_count?: number; snapshots_count?: number } | null>(null)
  const [error, setError] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement | null>(null)

  const handleFile = (f: File) => {
    setFile(f)
    setResult(null)
    setError(null)
  }

  const upload = async () => {
    if (!file) return
    setUploading(true)
    setError(null)
    setResult(null)

    const form = new FormData()
    form.append('file', file)

    try {
      const res = await api.post('/employees/upload-csv', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setResult(res.data)
    } catch (err: any) {
      const detail = err.response?.data?.detail || err.message || 'Upload failed — please check that your CSV columns match the expected format.'
      setError(detail)
    } finally {
      setUploading(false)
    }
  }

  const longitudinalColumns = [
    'employee_code',
    'snapshot_month',
    'department',
    'job_role',
    'hire_date',
    'employment_status',
    'overtime_hours',
    'job_satisfaction_score',
    'work_life_balance_score',
    'manager_support_score',
    'engagement_score',
    'stress_score',
    'absence_rate'
  ]

  return (
    <div className="p-6 flex flex-col gap-5 max-w-3xl mx-auto">
      <div>
        <h1 className="text-[22px] font-semibold text-slate-800 dark:text-white">Upload Longitudinal Telemetry CSV</h1>
        <p className="text-[13px] text-slate-500 dark:text-gray-400 mt-1">
          Ingest monthly workforce observations for attrition risk intelligence and early-warning trend analytics.
        </p>
      </div>

      <div
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault()
          if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0])
          }
        }}
        className="border-2 border-dashed border-slate-200 dark:border-gray-700 rounded-xl p-10 flex flex-col items-center gap-3 cursor-pointer hover:border-blue-400 dark:hover:border-blue-600 hover:bg-blue-50/30 dark:hover:bg-blue-950/20 transition-all"
      >
        <div className="w-12 h-12 bg-blue-50 dark:bg-blue-950 rounded-xl flex items-center justify-center">
          <UploadIcon size={24} className="text-blue-600 dark:text-blue-400" />
        </div>
        <div className="text-center">
          <p className="text-[14px] font-medium text-slate-700 dark:text-gray-200">Drop your CSV here or click to browse</p>
          <p className="text-[12px] text-slate-400 dark:text-gray-500 mt-1">
            Supports multi-month longitudinal employee records (.csv format)
          </p>
        </div>
        <input
          ref={inputRef}
          type="file"
          accept=".csv"
          className="hidden"
          onChange={(e) => {
            if (e.target.files && e.target.files[0]) {
              handleFile(e.target.files[0])
            }
          }}
        />
      </div>

      {file && (
        <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-4 flex items-center justify-between gap-3 shadow-xs">
          <div className="flex items-center gap-3 min-w-0">
            <div className="w-10 h-10 bg-blue-50 dark:bg-blue-950 rounded-lg flex items-center justify-center shrink-0">
              <FileText size={18} className="text-blue-600 dark:text-blue-400" />
            </div>
            <div className="min-w-0">
              <p className="text-[13px] font-medium text-slate-700 dark:text-gray-200 truncate">{file.name}</p>
              <p className="text-[11px] text-slate-400 dark:text-gray-500">{(file.size / 1024).toFixed(1)} KB</p>
            </div>
          </div>

          <button
            onClick={upload}
            disabled={uploading}
            className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-[13px] font-medium rounded-lg transition-colors disabled:opacity-50 shrink-0 cursor-pointer"
          >
            {uploading ? 'Processing & Ingesting...' : 'Upload & Ingest'}
          </button>
        </div>
      )}

      {result && (
        <div className="p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/60 rounded-xl flex items-start gap-3">
          <CheckCircle size={18} className="text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
          <div>
            <p className="text-[13px] font-semibold text-emerald-800 dark:text-emerald-200">
              Ingestion Complete!
            </p>
            <p className="text-[12px] text-emerald-700 dark:text-emerald-300 mt-0.5">
              {result.message}
            </p>
            <div className="mt-2 flex gap-4 text-[12px] text-emerald-800 dark:text-emerald-300 font-medium">
              <span>Employees Ingested: <strong>{result.employees_count}</strong></span>
              <span>Snapshots Recorded: <strong>{result.snapshots_count}</strong></span>
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-800/60 rounded-xl flex items-start gap-3">
          <AlertCircle size={18} className="text-red-600 dark:text-red-400 shrink-0 mt-0.5" />
          <div>
            <p className="text-[13px] font-semibold text-red-800 dark:text-red-200">Ingestion Error</p>
            <p className="text-[12px] text-red-700 dark:text-red-300 mt-0.5">{error}</p>
          </div>
        </div>
      )}

      <div className="bg-slate-50 dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-4 flex flex-col gap-3">
        <div className="flex items-center gap-2">
          <Info size={15} className="text-blue-600 dark:text-blue-400" />
          <p className="text-[13px] font-medium text-slate-700 dark:text-gray-200">Supported Longitudinal Schema</p>
        </div>
        <p className="text-[12px] text-slate-500 dark:text-gray-400">
          The ingestion engine automatically links multi-month records by <code>employee_code</code>, handles empty survey ratings with temporal forward-fill, and computes the <strong>Factor Deterioration Index (FDI)</strong>.
        </p>
        <div className="flex flex-wrap gap-1.5 pt-1">
          {longitudinalColumns.map((col) => (
            <span
              key={col}
              className="text-[11px] font-mono px-2 py-0.5 bg-white dark:bg-gray-800 border border-slate-200 dark:border-gray-700 rounded text-slate-700 dark:text-gray-300"
            >
              {col}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}
