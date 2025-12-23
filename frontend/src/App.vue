<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()

onMounted(async () => {
  // Verificar autenticação ao carregar a aplicação
  if (authStore.token && !authStore.user) {
    await authStore.verifyToken()
  }
})
</script>

<style>
@import './styles/main.css';
</style>
