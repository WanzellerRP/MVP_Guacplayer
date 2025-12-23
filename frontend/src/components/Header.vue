<template>
  <header class="header-caixa sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
      <!-- Logo e Título -->
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
          <span class="text-caixa-primary font-bold text-lg">G</span>
        </div>
        <div>
          <h1 class="text-xl font-bold">GuacPlayer</h1>
          <p class="text-xs text-blue-100">CAIXA Econômica Federal</p>
        </div>
      </div>

      <!-- Menu de Navegação -->
      <nav class="hidden md:flex items-center gap-6">
        <router-link
          to="/dashboard"
          class="hover:text-blue-100 transition-colors"
          :class="{ 'border-b-2 border-white': $route.path === '/dashboard' }"
        >
          Dashboard
        </router-link>
        <router-link
          to="/connections"
          class="hover:text-blue-100 transition-colors"
          :class="{ 'border-b-2 border-white': $route.path === '/connections' }"
        >
          Conexões
        </router-link>
      </nav>

      <!-- Usuário e Logout -->
      <div class="flex items-center gap-4">
        <div v-if="authStore.user" class="text-right hidden sm:block">
          <p class="text-sm font-semibold">{{ authStore.user.username }}</p>
          <p class="text-xs text-blue-100">Conectado</p>
        </div>
        <button
          @click="handleLogout"
          class="px-4 py-2 bg-caixa-accent hover:bg-orange-600 text-white rounded-lg transition-colors"
        >
          Sair
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
header {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
