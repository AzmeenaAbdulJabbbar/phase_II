'use client'

import {
  LayoutDashboard,
  CheckSquare,
  BarChart3,
  Settings,
  LogOut,
  Zap,
  User
} from 'lucide-react'
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'
import { mockAuth } from '@/lib/mock-auth'
import { Calendar } from './calendar'

interface SidebarProps {
  activeTab: string
  setActiveTab: (tab: string) => void
}

export function Sidebar({ activeTab, setActiveTab }: SidebarProps) {
  const menuItems = [
    { id: 'dashboard', label: 'NexusAI', icon: LayoutDashboard },
    { id: 'tasks', label: 'My Tasks', icon: CheckSquare },
    { id: 'analytics', label: 'Neural Insights', icon: BarChart3 },
    { id: 'settings', label: 'Core Systems', icon: Settings },
  ]

  const handleSignOut = async () => {
    await mockAuth.signOut()
    window.location.href = '/signin'
  }

  return (
    <div className="w-64 h-screen fixed left-0 top-0 bg-slate-950 border-r border-slate-900/50 flex flex-col z-50">
      <div className="p-8">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 bg-neonBlue rounded-xl flex items-center justify-center shadow-neon-blue">
            <Zap className="text-slate-950 w-6 h-6 fill-current" />
          </div>
          <h1 className="text-xl font-black text-white tracking-tighter">NEXUS<span className="text-neonBlue">.</span>AI</h1>
        </div>

        <nav className="space-y-2">
          {menuItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={cn(
                "w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold transition-all duration-300",
                activeTab === item.id
                  ? "bg-neonBlue/10 text-white border border-neonBlue/30 shadow-[0_0_15px_rgba(0,242,255,0.1)]"
                  : "text-slate-500 hover:text-white hover:bg-slate-900 border border-transparent"
              )}
            >
              <item.icon className={cn("w-5 h-5", activeTab === item.id ? "text-neonBlue" : "")} />
              {item.label}
            </button>
          ))}
        </nav>

        <div className="mt-8">
          <Calendar />
        </div>
      </div>

      <div className="mt-auto p-8 space-y-4">
        <div className="p-4 rounded-2xl bg-slate-900/50 border border-slate-800 flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center">
            <User className="text-slate-400 w-5 h-5" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-black text-white truncate uppercase tracking-widest">
              {mockAuth.getSession()?.user?.name || 'Operator'}
            </p>
            <p className="text-[10px] text-white truncate">
              {mockAuth.getSession()?.user?.email || 'v1.0.4 - Online'}
            </p>
          </div>
        </div>

        <button
          onClick={handleSignOut}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-slate-500 hover:text-red-400 hover:bg-red-400/5 transition-all"
        >
          <LogOut className="w-5 h-5" />
          Log Out
        </button>
      </div>
    </div>
  )
}
