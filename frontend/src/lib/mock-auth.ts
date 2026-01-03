// Mock authentication implementation

interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
}

interface Session {
  user: User;
  token: string;
  expires_at: string;
}

class MockAuth {
  private session: Session | null = null;

  constructor() {
    // Check if there's a session in localStorage
    if (typeof window !== 'undefined') {
      const storedSession = localStorage.getItem('mock-session');
      if (storedSession) {
        try {
          this.session = JSON.parse(storedSession);
        } catch (e) {
          console.error('Failed to parse stored session:', e);
        }
      }
    }
  }

  private saveSession() {
    if (typeof window !== 'undefined' && this.session) {
      localStorage.setItem('mock-session', JSON.stringify(this.session));
    }
  }

  private clearSession() {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('mock-session');
    }
    this.session = null;
  }

  isAuthenticated(): boolean {
    if (!this.session) return false;
    
    // Check if session is expired
    const now = new Date();
    const expiresAt = new Date(this.session.expires_at);
    return now < expiresAt;
  }

  getSession(): Session | null {
    if (this.isAuthenticated()) {
      return this.session;
    }
    this.clearSession();
    return null;
  }

  async signIn(email: string, password: string): Promise<{ error?: string; user?: User }> {
    // Mock validation
    if (!email || !password) {
      return { error: 'Email and password are required' };
    }

    // Mock user data
    const user: User = {
      id: 'user_' + Date.now(),
      name: email.split('@')[0],
      email,
      created_at: new Date().toISOString(),
    };

    // Create a mock session (valid for 24 hours)
    const expiresAt = new Date();
    expiresAt.setHours(expiresAt.getHours() + 24);

    this.session = {
      user,
      token: 'mock_token_' + Date.now(),
      expires_at: expiresAt.toISOString(),
    };

    this.saveSession();

    return { user };
  }

  async signUp(email: string, password: string, name: string): Promise<{ error?: string; user?: User }> {
    // Mock validation
    if (!email || !password || !name) {
      return { error: 'Email, password, and name are required' };
    }

    if (password.length < 8) {
      return { error: 'Password must be at least 8 characters' };
    }

    // Mock user data
    const user: User = {
      id: 'user_' + Date.now(),
      name,
      email,
      created_at: new Date().toISOString(),
    };

    // Create a mock session (valid for 24 hours)
    const expiresAt = new Date();
    expiresAt.setHours(expiresAt.getHours() + 24);

    this.session = {
      user,
      token: 'mock_token_' + Date.now(),
      expires_at: expiresAt.toISOString(),
    };

    this.saveSession();

    return { user };
  }

  async signOut(): Promise<void> {
    this.clearSession();
  }

  async changePassword(oldPassword: string, newPassword: string): Promise<{ error?: string }> {
    if (!this.session) {
      return { error: 'Not authenticated' };
    }

    if (newPassword.length < 8) {
      return { error: 'New password must be at least 8 characters' };
    }

    // In a real app, you would validate the old password here
    // For mock, we just update the session

    return {};
  }
}

export const mockAuth = new MockAuth();