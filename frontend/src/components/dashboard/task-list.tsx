'use client'

import { useState, useEffect } from 'react'
import { Task } from '@/lib/api'
import { TaskCard } from './task-card'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, Filter, LayoutGrid, List } from 'lucide-react'

interface TaskListProps {
  tasks: Task[]
  onUpdate: () => void
}

export function TaskList({ tasks, onUpdate }: TaskListProps) {
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all')
  const [search, setSearch] = useState('')

  const filteredTasks = tasks.filter(task => {
    const matchesFilter =
      filter === 'all' ? true :
      filter === 'completed' ? task.completed : !task.completed
    const matchesSearch = task.title.toLowerCase().includes(search.toLowerCase())
    return matchesFilter && matchesSearch
  })

  // Group tasks by completion status for a better visual hierarchy if needed
  // But for now let's keep it simple with filters

  if (tasks.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-slate-900/20 rounded-3xl border-2 border-dashed border-slate-800 p-20 text-center"
      >
        <div className="w-20 h-20 bg-slate-900/50 rounded-full flex items-center justify-center mx-auto mb-6 border border-slate-800">
           <LayoutGrid className="w-10 h-10 text-slate-700" />
        </div>
        <h3 className="text-2xl font-bold text-slate-400">System Clear</h3>
        <p className="text-slate-600 mt-2 max-w-xs mx-auto">No active tasks detected in the neural network. Initialize a new task to begin.</p>
      </motion.div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="flex flex-col md:flex-row gap-4 items-center justify-between pb-2">
        <div className="relative w-full md:w-96">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="Search tasks..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-slate-900/50 border border-slate-800 focus:border-neonBlue/50 rounded-xl pl-11 pr-4 py-2.5 text-sm text-white outline-none transition-all"
          />
        </div>

        <div className="flex bg-slate-900/50 p-1 rounded-xl border border-slate-800 w-full md:w-auto">
          {(['all', 'pending', 'completed'] as const).map((opt) => (
            <button
              key={opt}
              onClick={() => setFilter(opt)}
              className={`flex-1 md:flex-none px-6 py-1.5 rounded-lg text-xs font-bold uppercase tracking-wider transition-all ${
                filter === opt
                  ? 'bg-neonBlue text-slate-950 shadow-neon-blue/20 shadow-sm'
                  : 'text-slate-500 hover:text-white'
              }`}
            >
              {opt}
            </button>
          ))}
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <AnimatePresence mode="popLayout">
          {filteredTasks.map((task) => (
            <TaskCard key={task.id} task={task} onUpdate={onUpdate} />
          ))}
        </AnimatePresence>
      </div>

      {filteredTasks.length === 0 && (
         <div className="py-20 text-center text-slate-600 font-medium">
            No tasks match your current filters.
         </div>
      )}
    </div>
  )
}
