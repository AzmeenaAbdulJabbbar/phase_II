'use client'

import { useEffect, useState } from 'react'
import { api, Task } from '@/lib/api'
import { TaskList } from '@/components/dashboard/task-list'
import { TaskForm } from '@/components/dashboard/task-form'
import { DashboardStats } from '@/components/dashboard/dashboard-stats'
import { Sidebar } from '@/components/dashboard/sidebar'
import { NeuralInsights } from '@/components/dashboard/neural-insights'
import { CoreSystems } from '@/components/dashboard/core-systems'
import { motion, AnimatePresence } from 'framer-motion'
import { RefreshCw, Bell, Search, Zap, CheckSquare } from 'lucide-react'
import { cn } from '@/lib/utils'

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('dashboard')

  const loadTasks = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await api.listTasks()
      setTasks(data || [])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadTasks()
  }, [])

  return (
    <div className="flex bg-slate-950 min-h-screen">
      {/* Structural Sidebar */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main View Area */}
      <main className="flex-1 ml-64 p-8 lg:p-12 overflow-y-auto">
        <header className="flex justify-between items-center mb-12">
          <div>
            <h2 className="text-slate-500 text-[10px] font-black uppercase tracking-[0.3em] mb-1">
              Neural Interface / {activeTab}
            </h2>
            <div className="flex items-center gap-3">
               <h1 className="text-3xl font-black text-white capitalize">{activeTab}</h1>
               <div className="px-2 py-0.5 rounded-md bg-neonBlue/10 border border-neonBlue/20 text-[10px] text-neonBlue font-black uppercase tracking-tighter">Live</div>
            </div>
          </div>

          <div className="flex items-center gap-6">
            <div className="hidden md:flex items-center bg-slate-900 border border-slate-800 rounded-xl px-4 py-2 w-64 group focus-within:border-neonBlue transition-all">
               <Search className="w-4 h-4 text-slate-500 group-focus-within:text-neonBlue" />
               <input type="text" placeholder="CMD + K to search..." className="bg-transparent border-none outline-none text-xs text-white ml-3 w-full" />
            </div>
            <button className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white transition-all relative">
               <Bell className="w-5 h-5" />
               <span className="absolute top-2.5 right-2.5 w-2 h-2 bg-neonBlue rounded-full shadow-neon-blue border-2 border-slate-900" />
            </button>
            <button
               onClick={loadTasks}
               disabled={loading}
               className="flex items-center gap-2 bg-white text-slate-950 px-5 py-2.5 rounded-xl font-bold text-sm hover:bg-neonBlue transition-all"
            >
               <RefreshCw className={cn("w-4 h-4", loading && "animate-spin")} />
               Sync
            </button>
          </div>
        </header>

        <AnimatePresence mode="wait">
          {activeTab === 'dashboard' && (
            <motion.div
              key="dashboard"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-12"
            >
              <section>
                <DashboardStats tasks={tasks} />
              </section>

              <section className="grid grid-cols-1 lg:grid-cols-3 gap-12">
                 <div className="lg:col-span-2 space-y-8">
                    <div className="flex items-center justify-between">
                       <h3 className="text-white font-black uppercase tracking-widest text-sm flex items-center gap-3">
                          <CheckSquare className="text-neonBlue w-5 h-5" />
                          Priority Sync (Recent)
                       </h3>
                       <button
                          onClick={() => setActiveTab('tasks')}
                          className="text-xs font-bold text-neonBlue hover:underline"
                       >
                          View All Systems
                       </button>
                    </div>
                    <TaskList tasks={tasks.slice(0, 4)} onUpdate={loadTasks} />
                 </div>

                 <div className="space-y-8">
                    <div className="p-8 rounded-3xl bg-slate-900 border border-slate-800 relative overflow-hidden group">
                       <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                          <Zap className="w-20 h-20" />
                       </div>
                       <h3 className="text-white font-black uppercase tracking-widest text-sm mb-4">Core System Status</h3>
                       <div className="space-y-4">
                          <div className="flex justify-between items-center text-xs">
                             <span className="text-slate-500 font-bold uppercase">Neural Link</span>
                             <span className="text-neonBlue font-bold">STABLE</span>
                          </div>
                          <div className="w-full h-1 bg-slate-800 rounded-full overflow-hidden">
                             <div className="w-full h-full bg-neonBlue shadow-neon-blue animate-pulse" />
                          </div>
                          <div className="flex justify-between items-center text-xs">
                             <span className="text-slate-500 font-bold uppercase">Database Sync</span>
                             <span className="text-emerald-400 font-bold">100% SUCCESS</span>
                          </div>
                       </div>
                    </div>

                    <div className="p-8 rounded-3xl bg-gradient-to-br from-neonBlue/10 to-transparent border border-neonBlue/20">
                       <h4 className="text-white font-bold text-lg mb-2">Nexus Pro Agent</h4>
                       <p className="text-slate-400 text-xs mb-6">Upgrade to unlock predictive task scheduling and advanced neural analytics.</p>
                       <button className="w-full py-4 bg-neonBlue text-slate-950 font-black rounded-xl text-xs uppercase tracking-widest shadow-neon-blue hover:scale-105 transition-all">
                          Initialize Upgrade
                       </button>
                    </div>
                 </div>
              </section>
            </motion.div>
          )}

          {activeTab === 'tasks' && (
            <motion.div
              key="tasks"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="max-w-4xl mx-auto space-y-12"
            >
               <section>
                  <div className="flex items-center justify-between mb-8">
                     <div>
                        <h3 className="text-white font-black uppercase tracking-widest text-lg">Task Command Center</h3>
                        <p className="text-slate-500 text-xs mt-1">Manage, modify, and synchronize your daily objectives.</p>
                     </div>
                  </div>
                  <TaskForm onTaskCreated={loadTasks} />
               </section>

               <section className="space-y-6">
                  <div className="flex items-center justify-between border-b border-slate-900 pb-4">
                     <h3 className="text-white font-black uppercase tracking-widest text-sm">Synchronized Objectives</h3>
                     <span className="bg-slate-900 text-slate-500 px-3 py-1 rounded-lg text-[10px] font-black border border-slate-800">
                        {tasks.length} LOGS FOUND
                     </span>
                  </div>
                  <TaskList tasks={tasks} onUpdate={loadTasks} />
               </section>
            </motion.div>
          )}

          {activeTab === 'analytics' && (
            <motion.div
              key="analytics"
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.98 }}
            >
              <NeuralInsights tasks={tasks} />
            </motion.div>
          )}

          {activeTab === 'settings' && (
            <motion.div
              key="settings"
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.98 }}
            >
              <CoreSystems />
            </motion.div>
          )}

          {activeTab !== 'dashboard' && activeTab !== 'tasks' && activeTab !== 'analytics' && activeTab !== 'settings' && (
             <motion.div
               key="placeholder"
               initial={{ opacity: 0 }}
               animate={{ opacity: 1 }}
               className="h-96 flex flex-col items-center justify-center text-center p-12 bg-slate-900/40 rounded-3xl border border-slate-800"
             >
                <div className="w-16 h-16 bg-slate-800 rounded-full mb-6 animate-pulse" />
                <h2 className="text-2xl font-bold text-white mb-2">Interface Locked</h2>
                <p className="text-slate-500 max-w-xs capitalize">{activeTab} module is currently being calibrated in the neural network.</p>
             </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  )
}
