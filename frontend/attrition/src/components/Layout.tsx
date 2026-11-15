import { Outlet, NavLink } from 'react-router-dom'
import {
  LayoutDashboard, Users, TrendingUp, MessageSquare,
  Upload, Moon, Sun, Brain, UserCheck, FileText
} from 'lucide-react'

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/employees', icon: Users, label: 'Employees' },
  { to: '/predictions', icon: TrendingUp, label: 'Risk Intelligence' },
  { to: '/interventions', icon: UserCheck, label: 'Interventions' },
  { to: '/reports', icon: FileText, label: 'Research Reports' },
  { to: '/chat', icon: MessageSquare, label: 'AI Assistant' },
  { to: '/upload', icon: Upload, label: 'Upload CSV' },
]

export default function Layout({ darkMode, setDarkMode }: { darkMode: boolean; setDarkMode: (v: boolean) => void }) {
  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <aside className="w-60 shrink-0 flex flex-col bg-white dark:bg-gray-900 border-r border-slate-200 dark:border-gray-800">
        {/* Logo */}
        <div className="flex items-center gap-2.5 px-6 py-5 border-b border-slate-200 dark:border-gray-800">
          <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center shadow-xs">
            <Brain size={18} className="text-white" />
          </div>
          <div>
            <span className="text-base font-bold text-slate-900 dark:text-white tracking-tight block">
              AttritionPulse
            </span>
            <span className="text-[10px] text-blue-600 font-semibold tracking-wider uppercase block">
              Intelligence v2.0
            </span>
          </div>
        </div>

        {/* Nav */}
        <nav className="flex-1 px-3 py-4 flex flex-col gap-1 overflow-y-auto">
          {navItems.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-xs font-semibold transition-all duration-150 ${
                  isActive
                    ? 'bg-blue-50 dark:bg-blue-950/70 text-blue-600 dark:text-blue-400 font-bold'
                    : 'text-slate-600 dark:text-gray-400 hover:bg-slate-50 dark:hover:bg-gray-800 hover:text-slate-900 dark:hover:text-gray-200'
                }`
              }
            >
              <Icon size={16} />
              {label}
            </NavLink>
          ))}
        </nav>

        {/* Dark mode toggle & Footer */}
        <div className="p-4 border-t border-slate-200 dark:border-gray-800">
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="w-full flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold text-slate-600 dark:text-gray-400 hover:bg-slate-100 dark:hover:bg-gray-800 transition-all cursor-pointer"
          >
            <span className="flex items-center gap-2">
              {darkMode ? <Sun size={15} className="text-amber-400" /> : <Moon size={15} />}
              {darkMode ? 'Light mode' : 'Dark mode'}
            </span>
          </button>
          <div className="mt-3 flex items-center gap-2.5 px-2">
            <div className="w-7 h-7 rounded-full bg-blue-600 flex items-center justify-center text-white text-[10px] font-bold">
              HR
            </div>
            <div>
              <p className="text-xs font-bold text-slate-800 dark:text-gray-200">HR Analytics Lead</p>
              <p className="text-[10px] text-slate-400 dark:text-gray-500">Enterprise Access</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto bg-slate-50 dark:bg-gray-950">
        <Outlet />
      </main>
    </div>
  )
}
