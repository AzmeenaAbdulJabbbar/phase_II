// Task entity (matches backend Pydantic model)
export interface Task {
  id: string
  user_id: string
  title: string
  description: string
  completed: boolean
  created_at: string  // ISO 8601 datetime string
  updated_at: string  // ISO 8601 datetime string
}

// Create task payload
export interface TaskCreate {
  title: string        // Required, 1-200 chars
  description?: string // Optional
}

// Update task payload
export interface TaskUpdate {
  title?: string
  description?: string
  completed?: boolean
}

// Task filter types
export type TaskFilter = 'all' | 'active' | 'completed'
