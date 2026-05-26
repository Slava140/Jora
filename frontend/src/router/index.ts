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
      path: '/projects/:projectId',
      name: 'project-board',
      component: () => import('@/views/projects/ProjectBoardView.vue'),
      props: true,
    },
    {
      path: '/projects/:projectId/edit',
      name: 'project-edit',
      component: () => import('@/views/projects/ProjectFormView.vue'),
      props: true,
    },
    {
      path: '/projects/:projectId/tasks/new',
      name: 'task-new',
      component: () => import('@/views/tasks/TaskFormView.vue'),
      props: true,
    },
    {
      path: '/projects/:projectId/tasks/:taskId',
      name: 'task-detail',
      component: () => import('@/views/tasks/TaskDetailView.vue'),
      props: true,
    },
    {
      path: '/my-tasks',
      name: 'my-tasks',
      component: () => import('@/views/tasks/MyTasksView.vue'),
    },
    {
      path: '/tasks',
      redirect: '/my-tasks',
    },
    {
      path: '/tasks/new',
      redirect: () => ({ name: 'projects' }),
    },
    {
      path: '/tasks/:id',
      name: 'task-legacy-redirect',
      component: () => import('@/views/tasks/TaskLegacyRedirectView.vue'),
      props: true,
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

  return true
})

export default router
