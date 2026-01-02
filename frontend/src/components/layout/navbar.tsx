'use client'

import { mockAuth } from '@/lib/mock-auth'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'

export function Navbar() {
  const router = useRouter()
  const session = mockAuth.getSession()
  const user = session?.user

  // Logout handler
  const handleLogout = async () => {
    await mockAuth.signOut()
    router.push('/signin')
  }

  return (
    <nav className="bg-slate-900 border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo/Title */}
          <div className="flex-shrink-0">
            <h1 className="text-xl font-bold text-white">Todo App</h1>
          </div>

          {/* User info and logout */}
          <div className="flex items-center space-x-4">
            {/* T006: User email display from JWT token (T008: responsive - hide on mobile) */}
            {user?.email && (
              <span className="hidden md:block text-sm font-medium text-white">
                {user.email}
              </span>
            )}

            {/* T007: Logout button with Better Auth signOut */}
            <Button
              variant="ghost"
              size="sm"
              onClick={handleLogout}
              aria-label="Logout"
              className="text-white hover:bg-slate-800"
            >
              Logout
            </Button>
          </div>
        </div>
      </div>
    </nav>
  )
}
