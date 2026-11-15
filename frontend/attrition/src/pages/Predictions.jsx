import { useState } from 'react'
import { TrendingUp, AlertTriangle, ShieldCheck, Clock, Brain, Search } from 'lucide-react'
import api from '../api/client'

export default function Predictions() {
  const [empId, setEmpId] = useState('1')
  const [predResult, setPredResult] = useState(null)
  const [survivalResult, setSurvivalResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const runPrediction = async () => {
    if (!empId) return
    setLoading(true)
    setError(null)
    try {
      const [pRes, sRes] = await Promise.all([
        api.post(`/api/v1/predictions/${empId}`),
        api.get(`/api/v1/survival/${empId}`)
      ])
      setPredResult(pRes.data)
      setSurvivalResult(sRes.data)
    } catch (err) {
      setError(`Employee #${empId} not found or prediction computation failed.`)
    }
    setLoading(false)
  }

  const getTierBadge = (cat) => {
    if (cat === 'Critical' || cat === 'High') return 'bg-red-50 text-red-600 border-red-200'
    if (cat === 'Moderate') return 'bg-amber-50 text-amber-600 border-amber-200'
    return 'bg-emerald-50 text-emerald-600 border-emerald-200'
  }

  return (
    <div className="p-8 flex flex-col gap-6 max-w-5xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <Brain className="text-blue-600" /> Longitudinal Flight Risk Intelligence
        </h1>
        <p className="text-sm text-slate-500 dark:text-gray-400 mt-1">
          Simultaneously evaluates calibrated 90-day classification risk, SHAP drivers, and Cox PH time-to-event curves.
        </p>
      </div>

      {/* Query Bar */}
      <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-5 shadow-sm">
        <label className="text-xs font-semibold text-slate-600 dark:text-gray-300 uppercase tracking-wider block mb-2">
          Target Employee Identifier
        </label>
        <div className="flex gap-3">
          <div className="relative flex-1">
            <input
              type="number"
              value={empId}
              onChange={(e) => setEmpId(e.target.value)}
              placeholder="e.g. 1"
              className="w-full px-4 py-2.5 text-sm bg-slate-50 dark:bg-gray-800 border border-slate-200 dark:border-gray-700 rounded-lg text-slate-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>
          <button
            onClick={runPrediction}
            disabled={loading}
            className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold rounded-lg transition-colors flex items-center gap-2 disabled:opacity-50 cursor-pointer"
          >
            <Search size={16} /> {loading ? 'Analyzing...' : 'Generate Prediction'}
          </button>
        </div>
        {error && <p className="text-xs text-red-500 mt-2 font-medium">{error}</p>}
      </div>

      {predResult && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Card 1: 90-Day Probability */}
          <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-6 shadow-sm flex flex-col justify-between">
            <div>
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">90-Day Departure Risk</span>
              <div className="text-4xl font-extrabold text-slate-900 dark:text-white mt-3">
                {(predResult.risk_probability * 100).toFixed(1)}%
              </div>
              <div className="mt-3">
                <span className={`text-xs font-bold px-3 py-1 rounded-full border ${getTierBadge(predResult.risk_category)}`}>
                  {predResult.risk_category} Risk Tier
                </span>
              </div>
            </div>
            <p className="text-xs text-slate-500 dark:text-gray-400 mt-6 pt-4 border-t border-slate-100 dark:border-gray-800">
              Evaluated with calibrated XGBoost + 12-factor temporal slope telemetry.
            </p>
          </div>

          {/* Card 2: SHAP Explanations */}
          <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-6 shadow-sm md:col-span-2">
            <h2 className="text-sm font-bold text-slate-900 dark:text-white mb-1">Key SHAP Attribution Drivers</h2>
            <p className="text-xs text-slate-500 mb-4">Top contributing factors pushing flight risk up or down.</p>
            <div className="space-y-3">
              {predResult.top_explanations.map((exp, idx) => (
                <div key={idx} className="flex items-center justify-between text-xs p-2.5 rounded-lg bg-slate-50 dark:bg-gray-800/60">
                  <span className="font-semibold text-slate-800 dark:text-gray-200 capitalize">
                    {exp.feature.replace(/_/g, ' ')}
                  </span>
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-medium text-slate-500">
                      {exp.shap_value > 0 ? `+${exp.shap_value.toFixed(3)}` : exp.shap_value.toFixed(3)}
                    </span>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      exp.impact === 'Increases Risk' ? 'bg-red-100 text-red-700' : 'bg-emerald-100 text-emerald-700'
                    }`}>
                      {exp.impact}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Card 3: Multi-Horizon Survival Timeline */}
          {survivalResult && (
            <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-6 shadow-sm md:col-span-3">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-sm font-bold text-slate-900 dark:text-white">Cox Proportional Hazards Timeline Projection</h2>
                  <p className="text-xs text-slate-500">Cumulative attrition risk over extended time horizons.</p>
                </div>
                <div className="flex items-center gap-1.5 text-xs text-blue-600 bg-blue-50 px-2.5 py-1 rounded">
                  <Clock size={14} /> Median Survival: {survivalResult.median_survival_days} days
                </div>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                {survivalResult.survival_timeline.map((point) => (
                  <div key={point.horizon_days} className="p-3 bg-slate-50 dark:bg-gray-800/60 rounded-xl text-center">
                    <span className="text-xs font-semibold text-slate-400 block mb-1">{point.horizon_days} Days</span>
                    <span className="text-lg font-bold text-slate-800 dark:text-white">
                      {(point.cumulative_attrition_risk * 100).toFixed(1)}%
                    </span>
                    <span className="text-[10px] text-slate-500 block mt-0.5">
                      Retention: {(point.survival_probability * 100).toFixed(0)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
