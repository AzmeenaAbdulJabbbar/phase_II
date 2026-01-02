'use client'

import { useState } from 'react'
import { CheckCircle2, Circle, Trash2, Edit3, Clock, AlertCircle } from 'lucide-react'
import { api, Task } from '@/lib/api'
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

interface TaskCardProps {
  task: Task
  onUpdate: () => void
}

export function TaskCard({ task, onUpdate }: TaskCardProps) {
  const [loading, setLoading] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [editTitle, setEditTitle] = useState(task.title)

  const handleToggle = async () => {
    try {
      setLoading(true)
      await api.toggleTask(task.id, !task.completed)
      onUpdate()
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) return
    try {
      setLoading(true)
      await api.deleteTask(task.id)
      onUpdate()
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleEdit = async () => {
    if (!editTitle.trim() || editTitle === task.title) {
      setIsEditing(false)
      return
    }
    try {
      setLoading(true)
      await api.patch(`/tasks/${task.id}`, { title: editTitle })
      setIsEditing(false)
      onUpdate()
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      whileHover={{ y: -2 }}
      className={cn(
        "group relative p-4 rounded-2xl transition-all duration-300",
        "bg-slate-900/40 backdrop-blur-md border",
        task.completed
          ? "border-slate-800 opacity-60"
          : "border-slate-800 hover:border-neonBlue/50 shadow-lg hover:shadow-neon-blue/5"
      )}
    >
      <div className="flex items-start gap-4">
        <button
          onClick={handleToggle}
          disabled={loading}
          className={cn(
            "mt-1 p-1 rounded-full transition-all duration-300",
            task.completed ? "text-neonBlue" : "text-slate-600 hover:text-neonBlue"
          )}
        >
          {task.completed ? (
            <CheckCircle2 className="w-6 h-6" />
          ) : (
            <Circle className="w-6 h-6" />
          )}
        </button>

        <div className="flex-1 min-w-0">
          {isEditing ? (
            <input
              autoFocus
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              onBlur={handleEdit}
              onKeyDown={(e) => e.key === 'Enter' && handleEdit()}
              className="w-full bg-slate-950 border border-neonBlue/50 rounded-lg px-2 py-1 text-white outline-none"
            />
          ) : (
            <h3 className={cn(
              "text-lg font-medium transition-all duration-300 truncate",
              task.completed ? "text-slate-500 line-through" : "text-white"
            )}>
              {task.title}
            </h3>
          )}

          {task.description && !isEditing && (
            <p className="text-slate-400 text-sm mt-1 line-clamp-2">
              {task.description}
            </p>
          )}

          <div className="flex items-center gap-4 mt-3 text-[10px] uppercase tracking-wider font-bold">
            <span className={cn(
              "flex items-center gap-1",
              task.completed ? "text-neonBlue" : "text-slate-500"
            )}>
              <Clock className="w-3 h-3" />
              {new Date(task.created_at).toLocaleDateString()}
            </span>
          </div>
        </div>

        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            onClick={() => setIsEditing(true)}
            className="p-2 text-slate-500 hover:text-white hover:bg-slate-800 rounded-lg transition-all"
          >
            <Edit3 className="w-4 h-4" />
          </button>
          <button
            onClick={handleDelete}
            className="p-2 text-slate-500 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-all"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </motion.div>
  )
}
