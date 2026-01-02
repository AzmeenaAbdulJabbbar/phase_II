// User entity from Better Auth
export interface User {
  id: string
  email: string
  name?: string
  createdAt: string
}

// Session entity from Better Auth
export interface Session {
  user: User
  accessToken: string
  refreshToken?: string
  expiresAt: string
}

// Auth state for components
export interface AuthState {
  user: User | null
  session: Session | null
  isLoading: boolean
  isAuthenticated: boolean
}

// Sign in credentials
export interface SignInCredentials {
  email: string
  password: string
}

// Sign up data
export interface SignUpData {
  email: string
  password: string
  name?: string
}
