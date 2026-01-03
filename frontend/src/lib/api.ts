// Mock API implementation for the todo app

export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  due_date?: string; // ISO string format
  priority?: 'low' | 'medium' | 'high';
  created_at: string; // ISO string format
  updated_at: string; // ISO string format
}

interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

class ApiClient {
  private baseUrl: string;
  private token: string | null;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001/api';
    this.token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
      ...(this.token && { 'Authorization': `Bearer ${this.token}` })
    };

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (!response.ok) {
        const errorData = await response.text();
        throw new Error(errorData || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('API request failed:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error occurred' 
      };
    }
  }

  async listTasks(): Promise<Task[]> {
    const result = await this.request<Task[]>('/tasks');
    if (result.success && result.data) {
      return result.data;
    }
    console.error('Failed to fetch tasks:', result.error);
    return [];
  }

  async getTask(id: string): Promise<Task | null> {
    const result = await this.request<Task>(`/tasks/${id}`);
    return result.success && result.data ? result.data : null;
  }

  async createTask(taskData: Partial<Task>): Promise<Task | null> {
    const result = await this.request<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
    return result.success && result.data ? result.data : null;
  }

  async updateTask(id: string, taskData: Partial<Task>): Promise<Task | null> {
    const result = await this.request<Task>(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
    return result.success && result.data ? result.data : null;
  }

  async deleteTask(id: string): Promise<boolean> {
    const result = await this.request<null>(`/tasks/${id}`, {
      method: 'DELETE',
    });
    return result.success;
  }

  async toggleTask(id: string, completed: boolean): Promise<Task | null> {
    return await this.updateTask(id, { completed });
  }

  async toggleTaskCompletion(id: string): Promise<Task | null> {
    const task = await this.getTask(id);
    if (!task) return null;

    return await this.updateTask(id, { ...task, completed: !task.completed });
  }

  async patch(endpoint: string, data: any): Promise<any> {
    return await this.request(`${endpoint}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }
}

export const api = new ApiClient();