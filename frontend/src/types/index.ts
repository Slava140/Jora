export type TaskStatus = 'open' | 'in_progress' | 'finished'

export interface User {
  id: number
  username: string
  email: string
  create_datetime: string
  update_datetime: string
}

export interface LoggedInUser extends User {
  access_token: string
}

export interface Project {
  id: number
  title: string
  description: string | null
  created_at: string
  updated_at: string
  owner_id: number
}

export interface Task {
  id: number
  title: string
  description: string
  status: TaskStatus
  due_date: string | null
  project_id: number
  finished_at: string | null
  created_at: string
  updated_at: string
  assignee_id: number | null
  author_id: number
}

export interface TaskMedia {
  id: number
  url: string
  filename: string
}

export interface TaskWithMedia extends Task {
  media: TaskMedia[]
}

export interface Comment {
  id: number
  content: string
  task_id: number
  created_at: string
  author_id: number
}

export interface Media {
  id: number
  filename: string
  has_original: boolean
  task_id: number
  author_id: number
  created_at: string
}

export interface PaginationParams {
  page?: number
  limit?: number
}

export interface TaskFilters extends PaginationParams {
  project_id?: number
  status?: TaskStatus
  author_id?: number
  assignee_id?: number
  title?: string
  from?: string
  to?: string
}

export interface CommentFilters extends PaginationParams {
  task_id?: number
  author_id?: number
}

export interface ApiError {
  message: string
}

export interface ValidationErrorItem {
  type: string
  loc: string[]
  msg: string
  input?: unknown
}

export interface CreateUserBody {
  username: string
  email: string
  password: string
}

export interface UpdateUserBody {
  username: string
  email: string
}

export interface LoginBody {
  email: string
  password: string
}

export interface CreateProjectBody {
  title: string
  description?: string | null
}

export interface CreateTaskBody {
  title: string
  description: string
  status?: TaskStatus
  due_date?: string | null
  project_id: number
}

export interface UpdateTaskBody {
  assignee_id?: number | null
  assignee_email?: string | null
  status: TaskStatus
  description: string
  due_date?: string | null
}

export interface CreateCommentBody {
  content: string
  task_id: number
}
