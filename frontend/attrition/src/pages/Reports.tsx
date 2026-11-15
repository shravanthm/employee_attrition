import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import {
  FileText, Download, BarChart2, ShieldAlert,
  Calendar, CheckCircle, ExternalLink
} from 'lucide-react'

export default function Reports() {
  const [downloading, setDownloading] = useState(false)

  return (
    <div className="p-8 flex flex-col gap-6 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <FileText className="text-blue-600" /> Research & Analytics Reports
        </h1>
        <p className="text-sm text-slate-500 dark:text-gray-400 mt-1">
          Exportable research summaries, empirical hypothesis findings, and longitudinal risk audit logs.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Report 1 */}
        <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="w-10 h-10 rounded-lg bg-blue-50 dark:bg-blue-950 flex items-center justify-center text-blue-600 mb-4">
              <BarChart2 size={20} />
            </div>
            <h2 className="text-base font-bold text-slate-900 dark:text-white mb-1">
              Statistical Methodology & Hypothesis Report
            </h2>
            <p className="text-xs text-slate-500 mb-4">
              Comprehensive report detailing Mann-Whitney U test statistics, Welch's t-test, Cohen's d effect sizes, and Benjamini-Hochberg FDR adjustments across all 12 factors.
            </p>
            <div className="flex items-center gap-2 text-[11px] text-slate-400">
              <Calendar size={12} /> Generated: 2026-11-15
            </div>
          </div>
          <a
            href="/reports/statistical_analysis_report.md"
            target="_blank"
            className="mt-6 flex items-center justify-center gap-1.5 px-4 py-2 border border-slate-200 dark:border-gray-700 hover:bg-slate-50 dark:hover:bg-gray-800 text-xs font-semibold rounded-lg text-slate-700 dark:text-gray-200 transition-colors"
          >
            <ExternalLink size={14} /> View Methodology Report
          </a>
        </div>

        {/* Report 2 */}
        <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="w-10 h-10 rounded-lg bg-emerald-50 dark:bg-emerald-950 flex items-center justify-center text-emerald-600 mb-4">
              <ShieldAlert size={20} />
            </div>
            <h2 className="text-base font-bold text-slate-900 dark:text-white mb-1">
              ML Model Benchmark & SHAP Evaluation
            </h2>
            <p className="text-xs text-slate-500 mb-4">
              Cross-model comparison across Model A (static baseline) and Model B (temporal features) testing Logistic Regression, Random Forest, and XGBoost with Brier score calibration.
            </p>
            <div className="flex items-center gap-2 text-[11px] text-slate-400">
              <Calendar size={12} /> Evaluation ROC-AUC: 0.6198
            </div>
          </div>
          <a
            href="/docs/MODEL_EVALUATION.md"
            target="_blank"
            className="mt-6 flex items-center justify-center gap-1.5 px-4 py-2 border border-slate-200 dark:border-gray-700 hover:bg-slate-50 dark:hover:bg-gray-800 text-xs font-semibold rounded-lg text-slate-700 dark:text-gray-200 transition-colors"
          >
            <ExternalLink size={14} /> View Benchmark Report
          </a>
        </div>

        {/* Report 3 */}
        <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="w-10 h-10 rounded-lg bg-purple-50 dark:bg-purple-950 flex items-center justify-center text-purple-600 mb-4">
              <FileText size={20} />
            </div>
            <h2 className="text-base font-bold text-slate-900 dark:text-white mb-1">
              Survival Analysis & Hazard Ratios
            </h2>
            <p className="text-xs text-slate-500 mb-4">
              Cox Proportional Hazards regression hazard ratios (95% CI) and Kaplan-Meier workforce tenure projection milestones. Harrell's C-Index: 0.6253.
            </p>
            <div className="flex items-center gap-2 text-[11px] text-slate-400">
              <Calendar size={12} /> Penalizer: 0.1 Regularized
            </div>
          </div>
          <a
            href="/docs/SURVIVAL_ANALYSIS.md"
            target="_blank"
            className="mt-6 flex items-center justify-center gap-1.5 px-4 py-2 border border-slate-200 dark:border-gray-700 hover:bg-slate-50 dark:hover:bg-gray-800 text-xs font-semibold rounded-lg text-slate-700 dark:text-gray-200 transition-colors"
          >
            <ExternalLink size={14} /> View Survival Analysis
          </a>
        </div>
      </div>
    </div>
  )
}
