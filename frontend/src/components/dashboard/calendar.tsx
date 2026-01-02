'use client'

import { useState, useEffect } from 'react'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { cn } from '@/lib/utils'
import { api, Task } from '@/lib/api'

export function Calendar() {
  const [currentDate, setCurrentDate] = useState(new Date())
  const [tasks, setTasks] = useState<Task[]>([])
  const today = new Date()

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const data = await api.listTasks()
        setTasks(data)
      } catch (err) {
        console.error('Failed to fetch tasks for calendar:', err)
      }
    }
    fetchTasks()
  }, [])

  const daysInMonth = (year: number, month: number) => new Date(year, month + 1, 0).getDate()
  const firstDayOfMonth = (year: number, month: number) => new Date(year, month, 1).getDay()

  const year = currentDate.getFullYear()
  const month = currentDate.getMonth()

  const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ]

  const daysArr = Array.from({ length: daysInMonth(year, month) }, (_, i) => i + 1)
  const blanks = Array.from({ length: firstDayOfMonth(year, month) }, (_, i) => i)

  const prevMonth = () => setCurrentDate(new Date(year, month - 1, 1))
  const nextMonth = () => setCurrentDate(new Date(year, month + 1, 1))

  return (
    <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-4 overflow-hidden">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-[10px] font-black text-neonBlue uppercase tracking-[0.2em]">
          {monthNames[month]} {year}
        </h3>
        <div className="flex gap-1">
          <button
            onClick={prevMonth}
            className="p-1 hover:bg-slate-800 rounded-md transition-colors text-slate-500 hover:text-white"
          >
            <ChevronLeft className="w-3 h-3" />
          </button>
          <button
            onClick={nextMonth}
            className="p-1 hover:bg-slate-800 rounded-md transition-colors text-slate-500 hover:text-white"
          >
            <ChevronRight className="w-3 h-3" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-7 gap-1 text-[10px]">
        {["S", "M", "T", "W", "T", "F", "S"].map((day, i) => (
          <div key={`header-${i}`} className="text-center font-bold text-slate-600 mb-1">{day}</div>
        ))}

        {blanks.map(i => (
          <div key={`blank-${i}`} className="text-center" />
        ))}

        {daysArr.map(day => {
          const isToday =
            day === today.getDate() &&
            month === today.getMonth() &&
            year === today.getFullYear()

          const hasTask = tasks.some(task => {
            if (!task.due_date) return false
            const dueDate = new Date(task.due_date)
            return (
              dueDate.getDate() === day &&
              dueDate.getMonth() === month &&
              dueDate.getFullYear() === year
            )
          })

          return (
            <div
              key={day}
              className={cn(
                "h-6 flex items-center justify-center rounded-md font-bold transition-all duration-300 relative",
                isToday
                  ? "bg-neonBlue text-slate-950 shadow-[0_0_10px_rgba(0,242,255,0.5)]"
                  : "text-slate-400 hover:bg-slate-800",
                hasTask && !isToday && "text-neonBlue border border-neonBlue/30"
              )}
            >
              {day}
              {hasTask && !isToday && (
                <div className="absolute -top-0.5 -right-0.5 w-1.5 h-1.5 bg-neonBlue rounded-full shadow-[0_0_5px_rgba(0,242,255,1)]" />
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
