import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

/**
 * Next.js Middleware for Protected Routes
 *
 * This middleware runs before requests are completed and checks authentication status.
 * It protects dashboard routes and redirects unauthenticated users to signin.
 */
export function middleware(request: NextRequest) {
  // Note: With client-side mock auth (localStorage), we can't check auth state in middleware
  // Auth protection is handled by client-side auth guards in the protected layout
  // This middleware is kept for future server-side auth implementation
  return NextResponse.next()
}

// Configure which routes to run middleware on
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public files (images, etc.)
     */
    '/((?!api|_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
