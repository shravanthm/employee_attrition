export interface Employee {
  id: number
  employee_code: string
  department: string
  job_role: string
  business_unit?: string
  location?: string
  hire_date: string
  employment_status: string
}

export interface MonthlySnapshot {
  id: number
  employee_id: number
  snapshot_month: string
  overtime_hours: number
  job_satisfaction_score?: number
  work_life_balance_score?: number
  manager_support_score?: number
  engagement_score?: number
  stress_score?: number
  absence_rate: number
  factor_deterioration_index?: number
}

export interface ExplanationItem {
  feature: string
  shap_value: number
  impact: string
}

export interface PredictionResult {
  employee_id: number
  risk_probability: number
  risk_category: 'Low' | 'Moderate' | 'High' | 'Critical'
  prediction_horizon_days: number
  top_explanations: ExplanationItem[]
}

export interface SurvivalPoint {
  horizon_days: number
  survival_probability: number
  cumulative_attrition_risk: number
}

export interface SurvivalResult {
  employee_id: number
  median_survival_days?: number
  survival_timeline: SurvivalPoint[]
}

export interface DashboardMetrics {
  total_employees: number
  active_employees: number
  high_risk_count: number
  moderate_risk_count: number
  low_risk_count: number
  average_fdi: number
  department_distribution: Record<string, number>
}

export interface Intervention {
  id: number
  employee_id: number
  intervention_type: string
  assigned_reviewer: string
  created_date: string
  planned_date?: string
  status: 'PLANNED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED'
  notes?: string
}
