import React, { useState, useEffect } from 'react'
import {
  FileText, Download, BarChart2, ShieldAlert,
  CheckCircle, Activity, Sparkles, TrendingDown,
  Layers, Clock, AlertTriangle, ArrowUpRight
} from 'lucide-react'
import api from '../api/client'

export default function Reports() {
  const [activeTab, setActiveTab] = useState<'hypothesis' | 'ml' | 'survival' | 'methodology'>('hypothesis')
  const [data, setData] = useState<{
    hypothesis_tests: any[]
    ml_evaluations: any[]
    cox_hazard_ratios: any[]
    descriptive_statistics: any[]
    logistic_regression: any[]
    methodology_markdown: string
  } | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchReports() {
      setLoading(true)
      try {
        const res = await api.get('/api/v1/reports/data')
        setData(res.data)
      } catch (err: any) {
        setError(err.message || 'Failed to load research reports data')
      } finally {
        setLoading(false)
      }
    }
    fetchReports()
  }, [])

  const downloadFile = (filename: string) => {
    window.open(`http://localhost:8000/api/v1/reports/download/${filename}`, '_blank')
  }

  const formatFactorName = (name: string) => {
    return name
      .replace(/_/g, ' ')
      .replace(/\b\w/g, (c) => c.toUpperCase())
  }

  return (
    <div className="p-8 flex flex-col gap-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <FileText className="text-blue-600" /> Research & Statistical Intelligence
          </h1>
          <p className="text-sm text-slate-500 dark:text-gray-400 mt-1">
            Empirical hypothesis validation, longitudinal ML benchmarks, Cox survival models, and exportable research data.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => downloadFile('statistical_analysis_report.md')}
            className="flex items-center gap-1.5 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-xs transition-colors cursor-pointer"
          >
            <Download size={14} /> Export Executive Summary (.md)
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-200 dark:border-gray-800 gap-6">
        <button
          onClick={() => setActiveTab('hypothesis')}
          className={`pb-3 text-sm font-semibold flex items-center gap-2 cursor-pointer transition-colors border-b-2 -mb-px ${
            activeTab === 'hypothesis'
              ? 'border-blue-600 text-blue-600 dark:text-blue-400'
              : 'border-transparent text-slate-500 hover:text-slate-800 dark:text-gray-400'
          }`}
        >
          <BarChart2 size={16} /> Empirical Hypothesis Tests
        </button>

        <button
          onClick={() => setActiveTab('ml')}
          className={`pb-3 text-sm font-semibold flex items-center gap-2 cursor-pointer transition-colors border-b-2 -mb-px ${
            activeTab === 'ml'
              ? 'border-blue-600 text-blue-600 dark:text-blue-400'
              : 'border-transparent text-slate-500 hover:text-slate-800 dark:text-gray-400'
          }`}
        >
          <Layers size={16} /> ML Benchmarking (Static vs Temporal)
        </button>

        <button
          onClick={() => setActiveTab('survival')}
          className={`pb-3 text-sm font-semibold flex items-center gap-2 cursor-pointer transition-colors border-b-2 -mb-px ${
            activeTab === 'survival'
              ? 'border-blue-600 text-blue-600 dark:text-blue-400'
              : 'border-transparent text-slate-500 hover:text-slate-800 dark:text-gray-400'
          }`}
        >
          <Clock size={16} /> Cox Hazard Ratios & Survival
        </button>

        <button
          onClick={() => setActiveTab('methodology')}
          className={`pb-3 text-sm font-semibold flex items-center gap-2 cursor-pointer transition-colors border-b-2 -mb-px ${
            activeTab === 'methodology'
              ? 'border-blue-600 text-blue-600 dark:text-blue-400'
              : 'border-transparent text-slate-500 hover:text-slate-800 dark:text-gray-400'
          }`}
        >
          <Sparkles size={16} /> Methodology Narrative
        </button>
      </div>

      {loading && (
        <div className="p-12 text-center text-slate-500 dark:text-gray-400 flex flex-col items-center gap-3">
          <Activity className="animate-spin text-blue-600" size={28} />
          <p className="text-sm">Loading statistical research reports...</p>
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-800/60 rounded-xl text-red-700 dark:text-red-300 text-sm">
          Failed to load research data: {error}
        </div>
      )}

      {!loading && data && (
        <div className="flex flex-col gap-6">
          {/* TAB 1: HYPOTHESIS TESTS */}
          {activeTab === 'hypothesis' && (
            <div className="flex flex-col gap-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-base font-bold text-slate-800 dark:text-white">
                    Factor Divergence: Departing vs Retained Cohorts
                  </h2>
                  <p className="text-xs text-slate-500 dark:text-gray-400 mt-0.5">
                    Evaluated with Mann-Whitney U test, Welch's t-test, Cohen's d effect sizes, and Benjamini-Hochberg FDR adjustments (α = 0.05).
                  </p>
                </div>
                <button
                  onClick={() => downloadFile('hypothesis_tests.csv')}
                  className="flex items-center gap-1.5 px-3 py-1.5 border border-slate-200 dark:border-gray-700 hover:bg-slate-50 dark:hover:bg-gray-800 rounded-lg text-xs font-semibold text-slate-700 dark:text-gray-200 transition-colors cursor-pointer"
                >
                  <Download size={13} /> Export CSV
                </button>
              </div>

              <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl overflow-x-auto shadow-xs">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 dark:bg-gray-800/60 text-slate-600 dark:text-gray-300 border-b border-slate-200 dark:border-gray-800 font-semibold">
                    <tr>
                      <th className="p-3">Factor Name</th>
                      <th className="p-3 text-right">Departing Mean</th>
                      <th className="p-3 text-right">Retained Mean</th>
                      <th className="p-3 text-right">t-Statistic</th>
                      <th className="p-3 text-right">Cohen's d</th>
                      <th className="p-3 text-right">FDR Adjusted p-Value</th>
                      <th className="p-3 text-center">Significance (p &lt; 0.05)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 dark:divide-gray-800 text-slate-700 dark:text-gray-200 font-mono">
                    {data.hypothesis_tests.map((row, idx) => (
                      <tr key={idx} className="hover:bg-slate-50/60 dark:hover:bg-gray-800/40">
                        <td className="p-3 font-sans font-medium text-slate-900 dark:text-white">
                          {formatFactorName(row.factor)}
                        </td>
                        <td className="p-3 text-right">{Number(row.attrited_mean).toFixed(2)}</td>
                        <td className="p-3 text-right">{Number(row.retained_mean).toFixed(2)}</td>
                        <td className="p-3 text-right font-medium">{Number(row.t_statistic).toFixed(2)}</td>
                        <td className="p-3 text-right">
                          <span
                            className={
                              Math.abs(row.cohens_d) >= 0.8
                                ? 'text-purple-600 dark:text-purple-400 font-bold'
                                : Math.abs(row.cohens_d) >= 0.5
                                ? 'text-blue-600 dark:text-blue-400 font-medium'
                                : 'text-slate-500'
                            }
                          >
                            {Number(row.cohens_d).toFixed(2)}
                          </span>
                        </td>
                        <td className="p-3 text-right">
                          {Number(row.p_value_fdr_adjusted) < 0.0001
                            ? '< 0.0001'
                            : Number(row.p_value_fdr_adjusted).toFixed(4)}
                        </td>
                        <td className="p-3 text-center">
                          {row.significant_at_05 ? (
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-sans font-semibold bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
                              <CheckCircle size={10} /> Significant
                            </span>
                          ) : (
                            <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-sans font-medium bg-slate-100 dark:bg-gray-800 text-slate-500 dark:text-gray-400">
                              Not Significant
                            </span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB 2: ML BENCHMARKS */}
          {activeTab === 'ml' && (
            <div className="flex flex-col gap-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-base font-bold text-slate-800 dark:text-white">
                    Predictive Performance: Model A (Static) vs Model B (Temporal Longitudinal)
                  </h2>
                  <p className="text-xs text-slate-500 dark:text-gray-400 mt-0.5">
                    Evaluated on holdout cross-validation testing Brier calibration and Discrimination (ROC-AUC).
                  </p>
                </div>
                <button
                  onClick={() => downloadFile('ml_model_evaluation.csv')}
                  className="flex items-center gap-1.5 px-3 py-1.5 border border-slate-200 dark:border-gray-700 hover:bg-slate-50 dark:hover:bg-gray-800 rounded-lg text-xs font-semibold text-slate-700 dark:text-gray-200 transition-colors cursor-pointer"
                >
                  <Download size={13} /> Export CSV
                </button>
              </div>

              {/* Callout box */}
              <div className="p-4 bg-blue-50/80 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-900/60 rounded-xl flex items-start gap-3">
                <Sparkles size={18} className="text-blue-600 dark:text-blue-400 shrink-0 mt-0.5" />
                <div className="text-xs text-blue-900 dark:text-blue-200">
                  <p className="font-semibold">Key Empirical Finding:</p>
                  <p className="mt-0.5">
                    Temporal feature engineering (3-month slope, FDI, rolling standard deviation) improves <strong>PR-AUC from 0.450 → 0.680 (+51%)</strong> and reduces the Brier error score from 0.296 → 0.224, proving that longitudinal telemetry is significantly more predictive than static single-month snapshots.
                  </p>
                </div>
              </div>

              <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl overflow-x-auto shadow-xs">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 dark:bg-gray-800/60 text-slate-600 dark:text-gray-300 border-b border-slate-200 dark:border-gray-800 font-semibold">
                    <tr>
                      <th className="p-3">Feature Set</th>
                      <th className="p-3">Algorithm</th>
                      <th className="p-3 text-right">ROC-AUC</th>
                      <th className="p-3 text-right">PR-AUC</th>
                      <th className="p-3 text-right">Precision</th>
                      <th className="p-3 text-right">Recall</th>
                      <th className="p-3 text-right">F1 Score</th>
                      <th className="p-3 text-right">Brier Score (Lower is Better)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 dark:divide-gray-800 text-slate-700 dark:text-gray-200 font-mono">
                    {data.ml_evaluations.map((row, idx) => {
                      const isTemporal = row.feature_set.includes('Temporal')
                      return (
                        <tr
                          key={idx}
                          className={
                            isTemporal
                              ? 'bg-blue-50/20 dark:bg-blue-950/10 hover:bg-blue-50/40 dark:hover:bg-blue-950/20'
                              : 'hover:bg-slate-50/60 dark:hover:bg-gray-800/40'
                          }
                        >
                          <td className="p-3 font-sans font-medium">
                            <span
                              className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                                isTemporal
                                  ? 'bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-300'
                                  : 'bg-slate-100 dark:bg-gray-800 text-slate-600 dark:text-gray-400'
                              }`}
                            >
                              {row.feature_set.replace(/_/g, ' ')}
                            </span>
                          </td>
                          <td className="p-3 font-sans font-semibold text-slate-900 dark:text-white">
                            {formatFactorName(row.algorithm)}
                          </td>
                          <td className="p-3 text-right font-bold text-slate-900 dark:text-white">
                            {Number(row.roc_auc).toFixed(4)}
                          </td>
                          <td className="p-3 text-right text-blue-600 dark:text-blue-400 font-bold">
                            {Number(row.pr_auc).toFixed(4)}
                          </td>
                          <td className="p-3 text-right">{Number(row.precision).toFixed(4)}</td>
                          <td className="p-3 text-right">{Number(row.recall).toFixed(4)}</td>
                          <td className="p-3 text-right">{Number(row.f1_score).toFixed(4)}</td>
                          <td className="p-3 text-right font-semibold">
                            {Number(row.brier_score).toFixed(4)}
                          </td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB 3: SURVIVAL & COX HAZARD RATIOS */}
          {activeTab === 'survival' && (
            <div className="flex flex-col gap-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-base font-bold text-slate-800 dark:text-white">
                    Cox Proportional Hazards: Hazard Ratios & Risk Factors
                  </h2>
                  <p className="text-xs text-slate-500 dark:text-gray-400 mt-0.5">
                    Regularized Cox PH regression (Penalizer = 0.1). Harrell's Concordance Index: 0.6253.
                  </p>
                </div>
                <button
                  onClick={() => downloadFile('cox_hazard_ratios.csv')}
                  className="flex items-center gap-1.5 px-3 py-1.5 border border-slate-200 dark:border-gray-700 hover:bg-slate-50 dark:hover:bg-gray-800 rounded-lg text-xs font-semibold text-slate-700 dark:text-gray-200 transition-colors cursor-pointer"
                >
                  <Download size={13} /> Export CSV
                </button>
              </div>

              <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl overflow-x-auto shadow-xs">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 dark:bg-gray-800/60 text-slate-600 dark:text-gray-300 border-b border-slate-200 dark:border-gray-800 font-semibold">
                    <tr>
                      <th className="p-3">Risk Factor</th>
                      <th className="p-3 text-right">Hazard Ratio (HR)</th>
                      <th className="p-3 text-right">95% Confidence Interval</th>
                      <th className="p-3 text-right">z-Score</th>
                      <th className="p-3 text-right">p-Value</th>
                      <th className="p-3 text-center">Clinical Effect</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 dark:divide-gray-800 text-slate-700 dark:text-gray-200 font-mono">
                    {data.cox_hazard_ratios.map((row, idx) => {
                      const hr = Number(row.hazard_ratio)
                      const isProtective = hr < 0.95
                      const isRisk = hr > 1.01
                      return (
                        <tr key={idx} className="hover:bg-slate-50/60 dark:hover:bg-gray-800/40">
                          <td className="p-3 font-sans font-medium text-slate-900 dark:text-white">
                            {formatFactorName(row.factor)}
                          </td>
                          <td className="p-3 text-right font-bold text-slate-900 dark:text-white">
                            {hr.toFixed(3)}
                          </td>
                          <td className="p-3 text-right text-slate-500">
                            [{Number(row.hr_ci_lower_95).toFixed(2)}, {Number(row.hr_ci_upper_95).toFixed(2)}]
                          </td>
                          <td className="p-3 text-right">{Number(row.z_score).toFixed(2)}</td>
                          <td className="p-3 text-right">
                            {Number(row.p_value) < 0.01 ? (
                              <span className="font-bold text-emerald-600 dark:text-emerald-400">
                                {Number(row.p_value).toFixed(4)}
                              </span>
                            ) : (
                              Number(row.p_value).toFixed(4)
                            )}
                          </td>
                          <td className="p-3 text-center">
                            {isProtective ? (
                              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-sans font-semibold bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
                                <TrendingDown size={11} /> Protective Factor (Reduces Attrition)
                              </span>
                            ) : isRisk ? (
                              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-sans font-semibold bg-amber-50 dark:bg-amber-950/60 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
                                <AlertTriangle size={11} /> Escalates Risk
                              </span>
                            ) : (
                              <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-sans text-slate-500 bg-slate-100 dark:bg-gray-800">
                                Neutral Baseline
                              </span>
                            )}
                          </td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB 4: METHODOLOGY NARRATIVE */}
          {activeTab === 'methodology' && (
            <div className="flex flex-col gap-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-base font-bold text-slate-800 dark:text-white">
                    Executive Statistical Report & Research Methodology
                  </h2>
                  <p className="text-xs text-slate-500 dark:text-gray-400 mt-0.5">
                    Original experimental paper and empirical research documentation.
                  </p>
                </div>
                <button
                  onClick={() => downloadFile('statistical_analysis_report.md')}
                  className="flex items-center gap-1.5 px-3 py-1.5 border border-slate-200 dark:border-gray-700 hover:bg-slate-50 dark:hover:bg-gray-800 rounded-lg text-xs font-semibold text-slate-700 dark:text-gray-200 transition-colors cursor-pointer"
                >
                  <Download size={13} /> Download .md
                </button>
              </div>

              <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-6 font-mono text-xs text-slate-700 dark:text-gray-300 whitespace-pre-wrap leading-relaxed shadow-xs max-h-[600px] overflow-y-auto">
                {data.methodology_markdown || 'No methodology documentation found.'}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
