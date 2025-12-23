/**
 * Router do Vue.js
 * Autor: GuacPlayer Team
 * Data: 2025
 * Descrição: Configuração de rotas da aplicação
 */

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Views
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import ConnectionsView from '../views/ConnectionsView.vue'
import RecordingView from '../views/RecordingView.vue'

// Definir rotas
const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: {
      requiresAuth: false,
      title: 'Login - GuacPlayer'
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: {
      requiresAuth: true,
      title: 'Dashboard - GuacPlayer'
    }
  },
  {
    path: '/connections',
    name: 'Connections',
    component: ConnectionsView,
    meta: {
      requiresAuth: true,
      title: 'Conexões - GuacPlayer'
    }
  },
  {
    path: '/recordings/:uuid',
    name: 'Recording',
    component: RecordingView,
    meta: {
      requiresAuth: true,
      title: 'Gravação - GuacPlayer'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard'
  }
]

// Criar router
const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navegação
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Atualizar título da página
  document.title = to.meta.title || 'GuacPlayer'

  // Verificar autenticação
  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      // Tentar verificar token
      const isValid = await authStore.verifyToken()
      if (!isValid) {
        next('/login')
        return
      }
    }
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    // Se já está autenticado, redirecionar para dashboard
    next('/dashboard')
    return
  }

  next()
})

export default router
