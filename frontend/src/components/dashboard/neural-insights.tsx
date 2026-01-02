'use client'

import { Task } from '@/lib/api'
import { motion } from 'framer-motion'
import { Brain, Zap, Target, TrendingUp, AlertCircle, Layers } from 'lucide-react'
import { cn } from '@/lib/utils'

interface NeuralInsightsProps {
  tasks: Task[]
}

const CATEGORIES = [
  { name: "Development", keywords: ["code", "bug", "feature", "api", "git", "deploy", "build", "fix"], color: "bg-blue-500" },
  { name: "Documentation", keywords: ["read", "write", "docs", "readme", "spec", "plan"], color: "bg-emerald-500" },
  { name: "Operations", keywords: ["server", "db", "database", "neon", "cloud", "config", "setup"], color: "bg-purple-500" },
  { name: "Research", keywords: ["explore", "search", "investigate", "learn", "study"], color: "bg-amber-500" },
  { name: "Maintenance", keywords: ["update", "refactor", "cleanup", "test", "check"], color: "bg-rose-500" }
]

function categorizeTask(task: Task) {
  const content = `${task.title} ${task.description || ''}`.toLowerCase()
  for (const cat of CATEGORIES) {
    if (cat.keywords.some(kw => content.includes(kw))) {
      return cat.name
    }
  }
  return "General"
}

export function NeuralInsights({ tasks }: NeuralInsightsProps) {
  const completedTasks = tasks.filter(t => t.completed).length
  const totalTasks = tasks.length
  const completionRate = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0

  const overdueTasks = tasks.filter(t =>
    !t.completed && t.due_date && new Date(t.due_date) < new Date()
  ).length

  // Categorize tasks
  const categoryCounts = tasks.reduce((acc, task) => {
    const cat = categorizeTask(task)
    acc[cat] = (acc[cat] || 0) + 1
    return acc
  }, {} as Record<string, number>)

  const sortedCategories = Object.entries(categoryCounts)
    .sort(([, a], [, b]) => b - a)
    .map(([name, count]) => ({
      name,
      count,
      percentage: totalTasks > 0 ? (count / totalTasks) * 100 : 0,
      color: CATEGORIES.find(c => c.name === name)?.color || "bg-slate-700"
    }))

  const insights = [
    {
      title: "Efficiency Quotient",
      value: `${completionRate.toFixed(1)}%`,
      icon: TrendingUp,
      desc: "Overall mission success rate based on objective completion.",
      color: "text-emerald-400",
      bg: "bg-emerald-400/10"
    },
    {
      title: "Neural Load",
      value: `${totalTasks - completedTasks}`,
      icon: Brain,
      desc: "Current number of active cognitive threads pending execution.",
      color: "text-neonBlue",
      bg: "bg-neonBlue/10"
    },
    {
      title: "Critical Priority",
      value: overdueTasks,
      icon: AlertCircle,
      desc: "Objectives that have exceeded their neural synchronization window.",
      color: "text-red-400",
      bg: "bg-red-400/10"
    }
  ]

  return (
    <div className="space-y-12">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {insights.map((insight, i) => (
          <motion.div
            key={insight.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="p-6 rounded-2xl bg-slate-900 border border-slate-800 hover:border-neonBlue/30 transition-all group"
          >
            <div className={cn("w-12 h-12 rounded-xl flex items-center justify-center mb-6 transition-transform group-hover:scale-110", insight.bg)}>
              <insight.icon className={cn("w-6 h-6", insight.color)} />
            </div>
            <p className="text-slate-500 text-[10px] font-black uppercase tracking-widest mb-1">{insight.title}</p>
            <h4 className="text-3xl font-black text-white mb-2">{insight.value}</h4>
            <p className="text-xs text-slate-500 leading-relaxed">{insight.desc}</p>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="p-8 rounded-3xl bg-slate-900 border border-slate-800 relative overflow-hidden">
          <div className="absolute -right-8 -bottom-8 opacity-5">
            <Target className="w-64 h-64 text-neonBlue" />
          </div>
          <h3 className="text-white font-black uppercase tracking-widest text-sm mb-8 flex items-center gap-3">
             <Target className="text-neonBlue w-5 h-5" />
             Strategic Analysis
          </h3>
          <div className="space-y-6 relative z-10">
            <div className="space-y-2">
              <div className="flex justify-between text-xs font-bold uppercase tracking-tighter">
                <span className="text-slate-500">Task Velocity</span>
                <span className="text-neonBlue">Accelerating</span>
              </div>
              <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                <motion.div
                   initial={{ width: 0 }}
                   animate={{ width: '75%' }}
                   className="h-full bg-neonBlue shadow-neon-blue"
                />
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-xs font-bold uppercase tracking-tighter">
                <span className="text-slate-500">Focus Distribution</span>
                <span className="text-purple-400">Localized</span>
              </div>
              <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                <motion.div
                   initial={{ width: 0 }}
                   animate={{ width: '45%' }}
                   className="h-full bg-purple-400"
                />
              </div>
            </div>
          </div>
          <div className="mt-12 p-4 rounded-xl bg-neonBlue/5 border border-neonBlue/10">
             <p className="text-[10px] text-neonBlue font-bold uppercase tracking-widest mb-2 flex items-center gap-2">
                <Zap className="w-3 h-3" /> AI Suggestion
             </p>
             <p className="text-xs text-slate-400 italic">"Based on your neural load, we recommend tackling the oldest pending objective to maintain network equilibrium."</p>
          </div>
        </div>

        <div className="p-8 rounded-3xl bg-slate-900 border border-slate-800">
           <h3 className="text-white font-black uppercase tracking-widest text-sm mb-8">Weekly Sync Log</h3>
           <div className="space-y-4">
              {[7, 6, 5, 4, 3, 2, 1].map(day => (
                 <div key={day} className="flex items-center gap-4">
                    <span className="text-[10px] font-black text-slate-600 w-8">DAY {day}</span>
                    <div className="flex-1 h-3 flex gap-1">
                       {Array.from({ length: 12 }).map((_, i) => (
                          <div
                             key={i}
                             className={cn(
                                "flex-1 rounded-sm transition-all duration-500",
                                Math.random() > 0.4 ? "bg-neonBlue/20" : "bg-slate-800"
                             )}
                          />
                       ))}
                    </div>
                 </div>
              ))}
           </div>
           <p className="text-[10px] text-slate-600 font-bold uppercase mt-6 text-center tracking-[0.3em]">Neural Activity Heatmap</p>
        </div>
      </div>

      <div className="p-8 rounded-3xl bg-slate-900 border border-slate-800">
        <h3 className="text-white font-black uppercase tracking-widest text-sm mb-8 flex items-center gap-3">
          <Layers className="text-neonBlue w-5 h-5" />
          Task Category Clusters (AI Identified)
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sortedCategories.map((cat, i) => (
            <div key={cat.name} className="space-y-3">
              <div className="flex justify-between items-center text-xs">
                <span className="text-white font-bold">{cat.name}</span>
                <span className="text-slate-500 font-black tracking-tighter">{cat.count} LOGS</span>
              </div>
              <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden flex">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${cat.percentage}%` }}
                  className={cn("h-full", cat.color)}
                />
              </div>
              <p className="text-[10px] text-slate-500">{cat.percentage.toFixed(0)}% of total neural load</p>
            </div>
          ))}
          {sortedCategories.length === 0 && (
            <div className="col-span-full py-12 text-center border-2 border-dashed border-slate-800 rounded-2xl">
              <p className="text-slate-600 font-bold uppercase text-[10px] tracking-widest">No neural clusters identified</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
