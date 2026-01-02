'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Settings, Shield, Cpu, Bell, Database, Globe, Zap, Moon } from 'lucide-react'
import { cn } from '@/lib/utils'

export function CoreSystems() {
  const [notifications, setNotifications] = useState(true)
  const [encryption, setEncryption] = useState(true)
  const [sync, setSync] = useState(true)

  const settingsGroups = [
    {
      title: "Neural Interface",
      icon: Cpu,
      settings: [
        { id: 'notif', label: 'Neural Alerts', value: notifications, setter: setNotifications, icon: Bell, desc: 'Receive real-time pulses for objective deadlines' },
        { id: 'theme', label: 'Dark Matter Mode', value: true, disabled: true, icon: Moon, desc: 'Optimized visual spectral interface for long sessions' },
      ]
    },
    {
      title: "Security & Protocols",
      icon: Shield,
      settings: [
        { id: 'enc', label: 'Neural Encryption', value: encryption, setter: setEncryption, icon: Shield, desc: 'End-to-end multi-layer data synchronization' },
        { id: 'privacy', label: 'Ghost Mode', value: false, icon: Globe, desc: 'Mask neural presence from the public network' },
      ]
    },
    {
      title: "Data Core",
      icon: Database,
      settings: [
        { id: 'sync', label: 'Cloud Uplink', value: sync, setter: setSync, icon: Zap, desc: 'Automatically synchronize binary logs with Neon core' },
      ]
    }
  ]

  return (
    <div className="max-w-4xl space-y-12">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
        <div className="space-y-8">
          {settingsGroups.map((group, groupIdx) => (
            <section key={group.title} className="space-y-4">
              <div className="flex items-center gap-3 mb-2">
                <group.icon className="w-4 h-4 text-neonBlue" />
                <h3 className="text-white font-black uppercase tracking-[0.2em] text-xs pb-1 border-b border-slate-900 flex-1">{group.title}</h3>
              </div>
              <div className="space-y-2">
                {group.settings.map((setting) => (
                  <div
                    key={setting.id}
                    className="p-4 rounded-xl bg-slate-900/50 border border-slate-800 hover:border-slate-700 transition-all flex items-center justify-between group"
                  >
                    <div className="flex items-center gap-4">
                      <div className="p-2 rounded-lg bg-slate-800 text-slate-400 group-hover:text-neonBlue transition-colors">
                        <setting.icon className="w-4 h-4" />
                      </div>
                      <div>
                        <p className="text-sm font-bold text-white leading-none mb-1">{setting.label}</p>
                        <p className="text-[10px] text-slate-500">{setting.desc}</p>
                      </div>
                    </div>
                    {setting.setter ? (
                      <button
                        onClick={() => setting.setter(!setting.value)}
                        className={cn(
                          "w-12 h-6 rounded-full transition-all relative overflow-hidden",
                          setting.value ? "bg-neonBlue" : "bg-slate-800"
                        )}
                      >
                        <motion.div
                          animate={{ x: setting.value ? 24 : 4 }}
                          className="absolute top-1 w-4 h-4 bg-white rounded-full shadow-lg"
                        />
                      </button>
                    ) : (
                      <div className="px-2 py-1 rounded bg-slate-800 text-[8px] font-black text-slate-500 uppercase">System Lock</div>
                    )}
                  </div>
                ))}
              </div>
            </section>
          ))}
        </div>

        <div className="space-y-8">
          <div className="p-8 rounded-3xl bg-slate-900 border border-slate-800 relative overflow-hidden group">
             <div className="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity rotate-12">
                <Cpu className="w-32 h-32 text-neonBlue" />
             </div>
             <h3 className="text-white font-black uppercase tracking-widest text-sm mb-6 flex items-center gap-3">
                <Settings className="w-4 h-4 text-neonBlue" />
                System Maintenance
             </h3>
             <div className="space-y-6">
                <div className="space-y-2">
                   <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Database Optimization</p>
                   <button className="w-full py-3 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold transition-all border border-slate-700 text-left flex justify-between items-center group">
                      Run Neural Cleanup
                      <Zap className="w-3 h-3 text-neonBlue opacity-0 group-hover:opacity-100 transition-opacity" />
                   </button>
                </div>
                <div className="space-y-2">
                   <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Network Status</p>
                   <div className="p-4 rounded-xl bg-slate-950 border border-slate-900">
                      <div className="flex items-center justify-between mb-4">
                         <span className="text-xs text-slate-500">Signal Strength</span>
                         <div className="flex gap-0.5 items-end h-3">
                            <div className="w-1 h-1 bg-neonBlue" />
                            <div className="w-1 h-1.5 bg-neonBlue" />
                            <div className="w-1 h-2 bg-neonBlue" />
                            <div className="w-1 h-3 bg-neonBlue shadow-neon-blue" />
                         </div>
                      </div>
                      <div className="flex items-center justify-between">
                         <span className="text-xs text-slate-500">Protocol</span>
                         <span className="text-[10px] font-black text-neonBlue uppercase tabular-nums">IPv4 / Secure</span>
                      </div>
                   </div>
                </div>
             </div>

             <div className="mt-8 pt-8 border-t border-slate-800">
                <button className="w-full py-4 text-red-400 hover:bg-red-400/5 rounded-xl border border-red-400/20 text-xs font-black uppercase tracking-widest transition-all">
                   Flush All Neural Logs
                </button>
                <p className="text-[9px] text-slate-600 mt-4 text-center">Caution: This action will permanently erase all local logs and system configurations.</p>
             </div>
          </div>
        </div>
      </div>
    </div>
  )
}
