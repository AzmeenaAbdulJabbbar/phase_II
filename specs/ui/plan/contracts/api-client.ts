// API Client Contract: Phase II Frontend UI Core
// This file defines the TypeScript interface contract for the API client (lib/api.ts)
// Purpose: Centralized API communication with automatic JWT Bearer token injection

import type { Task, TaskCreate, TaskUpdate } from '../../../types/task'
import type { ApiSuccessResponse } from '../../../types/api'

/**
 * Configuration options for the API client.
 */
export interface ApiClientConfig {
  baseUrl: string
  timeout?: number
  retryAttempts?: number
}

/**
 * Request options for API calls.
 */
export interface RequestOptions extends Omit<RequestInit, 'body'> {
  params?: Record<string, string | number | boolean>
  body?: unknown
}

/**
 * API Client interface that ALL implementations must satisfy.
 * This contract ensures consistent API communication patterns.
 */
export interface IApiClient {
  /**
   * Core HTTP methods with automatic Bearer token injection
   */
  get<T>(path: string, options?: RequestOptions): Promise<T>
  post<T>(path: string, body?: unknown, options?: RequestOptions): Promise<T>
  put<T>(path: string, body?: unknown, options?: RequestOptions): Promise<T>
  patch<T>(path: string, body?: unknown, options?: RequestOptions): Promise<T>
  delete<T>(path: string, options?: RequestOptions): Promise<T>

  /**
   * Set or update the authentication token.
   * This method is called automatically by the auth layer.
   */
  setAuthToken(token: string | null): void

  /**
   * Get current configuration.
   */
  getConfig(): ApiClientConfig
}

/**
 * Task API endpoints contract.
 * Defines all task-related operations.
 */
export interface ITaskApi {
  /**
   * Get all tasks for the authenticated user.
   * Backend filters by user_id from JWT.
   */
  list(): Promise<Task[]>

  /**
   * Get a single task by ID.
   * Returns 404 if task doesn't exist or belongs to another user.
   */
  get(id: string): Promise<Task>

  /**
   * Create a new task.
   * user_id is automatically extracted from JWT by backend.
   */
  create(data: TaskCreate): Promise<Task>

  /**
   * Update an existing task.
   * Only title, description, and completed fields can be updated.
   */
  update(id: string, data: TaskUpdate): Promise<Task>

  /**
   * Delete a task.
   * Returns 404 if task doesn't exist or belongs to another user.
   */
  delete(id: string): Promise<void>

  /**
   * Toggle task completion status.
   * Convenience method for patch({completed: !current}).
   */
  toggleComplete(id: string, completed: boolean): Promise<Task>
}

/**
 * Complete API surface combining all resource APIs.
 */
export interface IApi {
  client: IApiClient
  tasks: ITaskApi
}

/**
 * Error class for API errors.
 */
export class ApiError extends Error {
  constructor(
    public status: number,
    public code: string,
    message: string,
    public details?: Record<string, unknown>
  ) {
    super(message)
    this.name = 'ApiError'
  }

  /**
   * Check if error is due to authentication failure.
   */
  isAuthError(): boolean {
    return this.status === 401 || this.status === 403
  }

  /**
   * Check if error is due to resource not found.
   */
  isNotFoundError(): boolean {
    return this.status === 404
  }

  /**
   * Check if error is due to validation failure.
   */
  isValidationError(): boolean {
    return this.status === 422
  }
}

/**
 * Usage Example:
 *
 * ```typescript
 * // Implementation in lib/api.ts
 * import { authClient } from './auth'
 * import type { IApiClient, ITaskApi, IApi } from './contracts/api-client'
 *
 * class ApiClient implements IApiClient {
 *   private authToken: string | null = null
 *
 *   async get<T>(path: string, options?: RequestOptions): Promise<T> {
 *     const headers = await this.getHeaders()
 *     const response = await fetch(`${this.config.baseUrl}${path}`, {
 *       ...options,
 *       method: 'GET',
 *       headers: {
 *         ...headers,
 *         ...options?.headers,
 *       },
 *     })
 *     return this.handleResponse<T>(response)
 *   }
 *
 *   private async getHeaders(): Promise<HeadersInit> {
 *     const headers: HeadersInit = {
 *       'Content-Type': 'application/json',
 *     }
 *
 *     // Auto-inject Bearer token from Better Auth session
 *     if (!this.authToken) {
 *       const session = await authClient.getSession()
 *       this.authToken = session?.token || null
 *     }
 *
 *     if (this.authToken) {
 *       headers['Authorization'] = `Bearer ${this.authToken}`
 *     }
 *
 *     return headers
 *   }
 *
 *   // ... other methods
 * }
 *
 * class TaskApi implements ITaskApi {
 *   constructor(private client: IApiClient) {}
 *
 *   async list(): Promise<Task[]> {
 *     return this.client.get<Task[]>('/tasks')
 *   }
 *
 *   async create(data: TaskCreate): Promise<Task> {
 *     return this.client.post<Task>('/tasks', data)
 *   }
 *
 *   // ... other methods
 * }
 *
 * // Export singleton
 * const client = new ApiClient({ baseUrl: process.env.NEXT_PUBLIC_API_URL! })
 * export const api: IApi = {
 *   client,
 *   tasks: new TaskApi(client),
 * }
 * ```
 */
