import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCapabilitiesStore } from '@/stores/capabilities'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/projects' },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/LoginView.vue'),
      meta: { public: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/auth/RegisterView.vue'),
      meta: { public: true },
    },
    {
      path: '/projects',
      name: 'projects',
      component: () => import('@/views/projects/ProjectListView.vue'),
    },
    {
      path: '/projects/new',
      name: 'project-new',
      component: () => import('@/views/projects/ProjectFormView.vue'),
    },
    {
      path: '/projects/:id',
      name: 'project-detail',
      component: () => import('@/views/projects/ProjectDetailView.vue'),
      props: true,
    },
    {
      path: '/projects/:id/edit',
      name: 'project-edit',
      component: () => import('@/views/projects/ProjectFormView.vue'),
      props: true,
    },
    {
      path: '/tasks',
      name: 'tasks',
      component: () => import('@/views/tasks/TaskListView.vue'),
    },
    {
      path: '/tasks/new',
      name: 'task-new',
      component: () => import('@/views/tasks/TaskFormView.vue'),
    },
    {
      path: '/tasks/:id',
      name: 'task-detail',
      component: () => import('@/views/tasks/TaskDetailView.vue'),
      props: true,
    },
    {
      path: '/users',
      name: 'users',
      component: () => import('@/views/users/UserListView.vue'),
      meta: { requiresUserWrite: true },
    },
    {
      path: '/users/new',
      name: 'user-new',
      component: () => import('@/views/users/UserFormView.vue'),
      meta: { requiresUserWrite: true },
    },
    {
      path: '/users/:id/edit',
      name: 'user-edit',
      component: () => import('@/views/users/UserFormView.vue'),
      props: true,
      meta: { requiresUserWrite: true },
    },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  const caps = useCapabilitiesStore()

  if (to.meta.public) {
    if (auth.isAuthenticated) return { path: '/projects' }
    return true
  }

  if (!auth.isAuthenticated) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }

  if (!caps.loaded) {
    await caps.probe()
  }

  if (to.meta.requiresUserWrite && !caps.canManageUsers) {
    return { path: '/projects' }
  }
  return true
})

export default router
