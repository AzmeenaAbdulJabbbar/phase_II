// Auth Client Contract: Phase II Frontend UI Core
// This file defines the TypeScript interface contract for Better Auth integration
// Purpose: Authentication state management and JWT token handling

import type { User, Session, AuthState, SignInCredentials, SignUpData } from '../../../types/auth'

/**
 * Better Auth configuration options.
 */
export interface AuthClientConfig {
  /**
   * Base URL for the auth endpoints.
   * Typically the backend API URL.
   */
  baseURL: string

  /**
   * Storage type for tokens.
   * 'cookie' (httpOnly) is recommended for production.
   */
  storage?: 'cookie' | 'localStorage' | 'sessionStorage'

  /**
   * Automatic token refresh.
   * Refreshes token before expiration.
   */
  autoRefresh?: boolean

  /**
   * Time in seconds before expiration to trigger refresh.
   * Default: 60 seconds.
   */
  refreshBuffer?: number
}

/**
 * Auth client interface for Better Auth integration.
 * This contract ensures consistent authentication patterns.
 */
export interface IAuthClient {
  /**
   * Sign in with email and password.
   * Returns user and session on success.
   * Throws error on invalid credentials.
   */
  signIn(credentials: SignInCredentials): Promise<{ user: User; session: Session }>

  /**
   * Sign up a new user with email and password.
   * Returns user and session on success.
   * Throws error if email already exists or validation fails.
   */
  signUp(data: SignUpData): Promise<{ user: User; session: Session }>

  /**
   * Sign out the current user.
   * Clears session and redirects to sign-in page.
   */
  signOut(): Promise<void>

  /**
   * Get the current session.
   * Returns null if not authenticated or token expired.
   */
  getSession(): Promise<Session | null>

  /**
   * Get the current user.
   * Returns null if not authenticated.
   */
  getUser(): Promise<User | null>

  /**
   * Check if user is authenticated.
   * Convenience method that checks session validity.
   */
  isAuthenticated(): Promise<boolean>

  /**
   * Manually refresh the access token.
   * Normally handled automatically if autoRefresh is enabled.
   */
  refreshToken(): Promise<void>

  /**
   * Subscribe to auth state changes.
   * Useful for updating UI when session changes.
   */
  onAuthStateChange(callback: (state: AuthState) => void): () => void
}

/**
 * React hooks for auth state management.
 * These are provided by Better Auth React integration.
 */
export interface IAuthHooks {
  /**
   * React hook to get current session.
   * Returns { data: Session | null, isLoading: boolean, error: Error | null }
   */
  useSession(): {
    data: Session | null
    isLoading: boolean
    error: Error | null
  }

  /**
   * React hook to get current user.
   * Returns { data: User | null, isLoading: boolean, error: Error | null }
   */
  useUser(): {
    data: User | null
    isLoading: boolean
    error: Error | null
  }

  /**
   * React hook for auth actions.
   * Returns { signIn, signUp, signOut } functions with loading states.
   */
  useAuth(): {
    signIn: (credentials: SignInCredentials) => Promise<void>
    signUp: (data: SignUpData) => Promise<void>
    signOut: () => Promise<void>
    isLoading: boolean
    error: Error | null
  }
}

/**
 * Error class for authentication errors.
 */
export class AuthError extends Error {
  constructor(
    public code: string,
    message: string,
    public details?: Record<string, unknown>
  ) {
    super(message)
    this.name = 'AuthError'
  }

  /**
   * Check if error is due to invalid credentials.
   */
  isInvalidCredentials(): boolean {
    return this.code === 'INVALID_CREDENTIALS'
  }

  /**
   * Check if error is due to email already existing.
   */
  isEmailExists(): boolean {
    return this.code === 'EMAIL_EXISTS'
  }

  /**
   * Check if error is due to weak password.
   */
  isWeakPassword(): boolean {
    return this.code === 'WEAK_PASSWORD'
  }

  /**
   * Check if error is due to token expiration.
   */
  isTokenExpired(): boolean {
    return this.code === 'TOKEN_EXPIRED'
  }
}

/**
 * Middleware function type for protecting routes.
 * Used in Next.js middleware.ts.
 */
export type AuthMiddleware = (
  request: Request,
  options?: {
    redirectTo?: string
    publicRoutes?: string[]
  }
) => Promise<Response | null>

/**
 * Usage Example:
 *
 * ```typescript
 * // Implementation in lib/auth.ts
 * import { createAuthClient } from "better-auth/react"
 * import { jwtPlugin } from "better-auth/plugins"
 * import type { IAuthClient } from './contracts/auth-client'
 *
 * // Create Better Auth client
 * export const authClient = createAuthClient({
 *   baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
 *   plugins: [
 *     jwtPlugin({
 *       storage: "cookie",
 *       autoRefresh: true,
 *       refreshBuffer: 60,
 *     }),
 *   ],
 * }) as IAuthClient
 *
 * // Export convenience functions
 * export const { signIn, signUp, signOut, useSession, useUser } = authClient
 *
 * // Usage in components:
 * function LoginPage() {
 *   const { signIn, isLoading, error } = useAuth()
 *
 *   async function handleSubmit(e: FormEvent) {
 *     e.preventDefault()
 *     const formData = new FormData(e.target as HTMLFormElement)
 *     await signIn({
 *       email: formData.get('email') as string,
 *       password: formData.get('password') as string,
 *     })
 *   }
 *
 *   return <form onSubmit={handleSubmit}>...</form>
 * }
 *
 * // Usage in middleware.ts for route protection:
 * import { NextResponse } from 'next/server'
 * import type { NextRequest } from 'next/server'
 * import { authClient } from './lib/auth'
 *
 * export async function middleware(request: NextRequest) {
 *   const session = await authClient.getSession()
 *
 *   // Redirect to signin if not authenticated
 *   if (!session && !request.nextUrl.pathname.startsWith('/signin')) {
 *     return NextResponse.redirect(new URL('/signin', request.url))
 *   }
 *
 *   // Redirect to dashboard if authenticated and on auth pages
 *   if (session && request.nextUrl.pathname.startsWith('/signin')) {
 *     return NextResponse.redirect(new URL('/dashboard', request.url))
 *   }
 *
 *   return NextResponse.next()
 * }
 *
 * export const config = {
 *   matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
 * }
 * ```
 */
