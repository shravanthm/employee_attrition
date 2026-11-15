import React, { useState } from 'react'
import { Plus, CheckCircle, Clock, UserCheck } from 'lucide-react'
import { Intervention } from '../types'

export default function Interventions() {
  const [interventions, setInterventions] = useState<Intervention[]>([
    {
      id: 1,
      employee_id: 1,
      intervention_type: 'Workload Rebalancing & Overtime Cap',
      assigned_reviewer: 'HR Business Partner',
      created_date: '2026-03-01',
      planned_date: '2026-03-15',
      status: 'IN_PROGRESS',
      notes: 'Employee flagged critical for compounding overtime and steep job satisfaction deterioration.'
    },
    {
      id: 2,
      employee_id: 42,
      intervention_type: 'Career Growth & Promotion Review',
      assigned_reviewer: 'Department Director',
      created_date: '2026-02-10',
      planned_date: '2026-02-28',
      status: 'COMPLETED',
      notes: 'Offered senior transition pathway and compensation adjustment. Retention verified.'
    },
    {
      id: 3,
      employee_id: 88,
      intervention_type: 'Manager 1:1 Cadence & Psychological Safety',
      assigned_reviewer: 'People Operations Lead',
      created_date: '2026-03-05',
      planned_date: '2026-03-20',
      status: 'PLANNED',
      notes: 'Recent leadership change led to feedback disruption.'
    }
  ])

  const [showModal, setShowModal] = useState(false)
  const [newType, setNewType] = useState('Workload Rebalancing & Overtime Cap')
  const [empId, setEmpId] = useState('15')
  const [reviewer, setReviewer] = useState('HR Specialist')
  const [notes, setNotes] = useState('')

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault()
    const item: Intervention = {
      id: interventions.length + 1,
      employee_id: Number(empId),
      intervention_type: newType,
      assigned_reviewer: reviewer,
      created_date: new Date().toISOString().split('T')[0],
      status: 'PLANNED',
      notes
    }
    setInterventions([item, ...interventions])
    setShowModal(false)
    setNotes('')
  }

  const getStatusBadge = (st: string) => {
    if (st === 'COMPLETED') return 'bg-emerald-50 text-emerald-700 border-emerald-200'
    if (st === 'IN_PROGRESS') return 'bg-blue-50 text-blue-700 border-blue-200'
    return 'bg-amber-50 text-amber-700 border-amber-200'
  }

  return (
    <div className="p-8 flex flex-col gap-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <UserCheck className="text-blue-600" /> Retention Interventions
          </h1>
          <p className="text-sm text-slate-500 dark:text-gray-400 mt-1">
            Track and verify proactive retention initiatives assigned to high flight-risk employees.
          </p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg flex items-center gap-1.5 transition-colors cursor-pointer"
        >
          <Plus size={16} /> New Retention Action
        </button>
      </div>

      <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-6 shadow-sm">
        <div className="space-y-4">
          {interventions.map((intv) => (
            <div key={intv.id} className="p-4 rounded-xl border border-slate-100 dark:border-gray-800 bg-slate-50/50 dark:bg-gray-800/40 flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-slate-900 dark:text-white text-sm">
                    Employee #{intv.employee_id}
                  </span>
                  <span className="text-xs text-slate-400">•</span>
                  <span className="text-xs font-semibold text-slate-700 dark:text-gray-300">
                    {intv.intervention_type}
                  </span>
                </div>
                <p className="text-xs text-slate-500 max-w-2xl">{intv.notes}</p>
                <div className="flex items-center gap-4 text-[11px] text-slate-400 pt-1">
                  <span>Assigned: <strong className="text-slate-600 dark:text-gray-300">{intv.assigned_reviewer}</strong></span>
                  <span>Logged: {intv.created_date}</span>
                </div>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <span className={`text-[11px] font-bold px-3 py-1 rounded-full border ${getStatusBadge(intv.status)}`}>
                  {intv.status.replace(/_/g, ' ')}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-xl p-6 max-w-md w-full shadow-xl">
            <h3 className="text-base font-bold text-slate-900 dark:text-white mb-4">Log Retention Action</h3>
            <form onSubmit={handleCreate} className="space-y-3">
              <div>
                <label className="text-xs font-semibold text-slate-600 dark:text-gray-300 block mb-1">Target Employee ID</label>
                <input
                  type="number"
                  value={empId}
                  onChange={(e) => setEmpId(e.target.value)}
                  className="w-full text-xs p-2.5 rounded-lg border border-slate-200 dark:border-gray-700 bg-slate-50 dark:bg-gray-800"
                  required
                />
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-600 dark:text-gray-300 block mb-1">Intervention Type</label>
                <select
                  value={newType}
                  onChange={(e) => setNewType(e.target.value)}
                  className="w-full text-xs p-2.5 rounded-lg border border-slate-200 dark:border-gray-700 bg-slate-50 dark:bg-gray-800"
                >
                  <option>Workload Rebalancing & Overtime Cap</option>
                  <option>Career Growth & Promotion Review</option>
                  <option>Manager 1:1 Cadence & Support</option>
                  <option>Compensation / Bonus Equity Adjustment</option>
                  <option>Flexible Schedule / Commute Relief</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-600 dark:text-gray-300 block mb-1">Assigned HR Reviewer</label>
                <input
                  type="text"
                  value={reviewer}
                  onChange={(e) => setReviewer(e.target.value)}
                  className="w-full text-xs p-2.5 rounded-lg border border-slate-200 dark:border-gray-700 bg-slate-50 dark:bg-gray-800"
                  required
                />
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-600 dark:text-gray-300 block mb-1">Reviewer Assessment & Action Plan</label>
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  className="w-full text-xs p-2.5 rounded-lg border border-slate-200 dark:border-gray-700 bg-slate-50 dark:bg-gray-800 h-20"
                  placeholder="Notes on agreement with employee..."
                />
              </div>
              <div className="flex justify-end gap-2 pt-3">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 text-xs font-semibold text-slate-500 hover:bg-slate-100 dark:hover:bg-gray-800 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-xs font-semibold bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Save Intervention
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
