'use client'

import { useEffect, useState } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { Navbar } from '@/components/layout/navbar'
import { mockAuth } from '@/lib/mock-auth'

export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const pathname = usePathname()
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null)

  useEffect(() => {
    // Check if user is authenticated (client-side only)
    const authenticated = mockAuth.isAuthenticated()
    setIsAuthenticated(authenticated)

    if (!authenticated) {
      // Redirect to signin with return URL
      router.push(`/signin?from=${encodeURIComponent(pathname)}`)
    }
  }, [router, pathname])

  // Show loading state during hydration
  if (isAuthenticated === null) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400">Loading...</div>
      </div>
    )
  }

  // Don't render protected content if not authenticated
  if (!isAuthenticated) {
    return null
  }

  return (
    <div className="min-h-screen bg-slate-950">
      <Navbar />
      {children}
    </div>
  )
}
