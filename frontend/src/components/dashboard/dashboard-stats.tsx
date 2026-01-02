'use client'

import { PieChart, Pie, Cell, ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts'
import { Task } from '@/lib/api'
import { motion } from 'framer-motion'
import { Activity, CheckCircle, Target, TrendingUp, Inbox } from 'lucide-react'

interface DashboardStatsProps {
  tasks: Task[]
}

export function DashboardStats({ tasks }: DashboardStatsProps) {
  const completed = tasks.filter(t => t.completed).length
  const pending = tasks.length - completed
  const ratio = tasks.length ? Math.round((completed / tasks.length) * 100) : 0

  const pieData = [
    { name: 'Completed', value: completed, color: '#10b981' }, // Green-500
    { name: 'Incomplete', value: pending, color: '#ef4444' }    // Red-500
  ]

  // Mock trend data for flow visualization
  const trendData = [
    { name: '00:00', completed: 0, pending: 0 },
    { name: '04:00', completed: Math.round(completed * 0.2), pending: Math.round(pending * 0.3) },
    { name: '08:00', completed: Math.round(completed * 0.5), pending: Math.round(pending * 0.6) },
    { name: '12:00', completed: completed, pending: pending },
    { name: '16:00', completed: completed, pending: pending },
  ]

  return (
    <div className="space-y-8 mb-12">
      {/* Glassmorphism Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: 'System Efficiency', value: `${ratio}%`, icon: Target, color: 'text-neonBlue' },
          { label: 'Active Process', value: tasks.length, icon: Activity, color: 'text-white' },
          { label: 'Completed', value: completed, icon: CheckCircle, color: 'text-emerald-400' },
          { label: 'Incomplete', value: pending, icon: Inbox, color: 'text-red-400' },
        ].map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="group relative p-6 rounded-[2rem] bg-slate-900/40 backdrop-blur-xl border border-slate-800/50 hover:border-neonBlue/40 transition-all duration-500 flex flex-col justify-between h-40 shadow-2xl overflow-hidden"
          >
            <div className={`absolute -right-4 -top-4 w-24 h-24 blur-3xl opacity-10 group-hover:opacity-20 transition-opacity rounded-full bg-current ${stat.color}`} />

            <div className="flex justify-between items-start">
              <div className="p-3 rounded-2xl bg-slate-950/50 border border-slate-800 group-hover:border-neonBlue/30 transition-colors">
                <stat.icon className={`w-5 h-5 ${stat.color}`} />
              </div>
              <div className="text-right">
                 <span className="text-[9px] font-black uppercase tracking-[0.2em] text-slate-600 block mb-1">Status</span>
                 <div className={`w-2 h-2 rounded-full ml-auto animate-pulse bg-current ${stat.color}`} />
              </div>
            </div>

            <div>
              <p className={`text-4xl font-black ${stat.color} tracking-tighter mb-1`}>{stat.value}</p>
              <p className="text-[10px] font-bold uppercase tracking-widest text-slate-500">{stat.label}</p>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Main Analytics Flow */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 rounded-[2rem] bg-slate-900/40 backdrop-blur-xl border border-slate-800/50 p-8 shadow-2xl relative overflow-hidden">
           <div className="absolute inset-0 opacity-[0.03] pointer-events-none bg-[radial-gradient(#00f2ff_1px,transparent_1px)] [background-size:16px_16px]" />

           <div className="flex justify-between items-center mb-10 relative">
            <div>
              <h3 className="text-white font-black uppercase tracking-[0.3em] text-xs">Neural Data Flow</h3>
              <p className="text-slate-500 text-[10px] uppercase font-bold mt-1">Status over synchronization cycle</p>
            </div>
            <div className="flex gap-4">
               <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-emerald-500" />
                <span className="text-[9px] text-slate-400 font-bold uppercase tracking-widest">Complete</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-red-500" />
                <span className="text-[9px] text-slate-400 font-bold uppercase tracking-widest">Incomplete</span>
              </div>
            </div>
          </div>

          <div className="w-full h-72 relative">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trendData}>
                <defs>
                  <linearGradient id="colorComplete" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.2}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorPending" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.2}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} opacity={0.2} />
                <XAxis dataKey="name" stroke="#64748b" fontSize={10} axisLine={false} tickLine={false} dy={10} />
                <YAxis hide />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '16px' }}
                  itemStyle={{ fontSize: '10px', fontWeight: 'bold', textTransform: 'uppercase' }}
                />
                <Area
                  type="monotone"
                  dataKey="completed"
                  stroke="#10b981"
                  strokeWidth={3}
                  fillOpacity={1}
                  fill="url(#colorComplete)"
                  animationDuration={2000}
                />
                <Area
                  type="monotone"
                  dataKey="pending"
                  stroke="#ef4444"
                  strokeWidth={3}
                  fillOpacity={1}
                  fill="url(#colorPending)"
                  animationDuration={2000}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-[2rem] bg-slate-900/40 backdrop-blur-xl border border-slate-800/50 p-8 shadow-2xl relative flex flex-col items-center">
          <h3 className="text-white font-black uppercase tracking-[0.3em] text-xs mb-8">Completion Matrix</h3>

          <div className="w-full h-56 relative">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  innerRadius={75}
                  outerRadius={95}
                  paddingAngle={10}
                  dataKey="value"
                  stroke="none"
                  animationDuration={1500}
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
              <span className="text-3xl font-black text-white leading-none">{ratio}%</span>
              <span className="text-[9px] text-slate-500 font-bold uppercase tracking-widest mt-1">Uptime</span>
            </div>
          </div>

          <div className="w-full mt-10 space-y-3">
             {pieData.map(d => (
               <div key={d.name} className="flex items-center justify-between p-4 rounded-2xl bg-slate-950/40 border border-slate-800 group hover:border-slate-700 transition-colors">
                  <div className="flex items-center gap-3">
                     <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: d.color, boxShadow: `0 0 10px ${d.color}40` }} />
                     <span className="font-bold text-slate-400 text-xs tracking-wider uppercase">{d.name}</span>
                  </div>
                  <span className="font-black text-white text-sm">{d.value}</span>
               </div>
             ))}
          </div>
        </div>
      </div>
    </div>
  )
}
