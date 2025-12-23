/**
 * Store de autenticação (Pinia)
 * Autor: GuacPlayer Team
 * Data: 2025
 * Descrição: Gerencia estado de autenticação da aplicação
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as authService from '../services/auth'

export const useAuthStore = defineStore('auth', () => {
  // Estado
  const user = ref(authService.getCurrentUser())
  const token = ref(authService.getAuthToken())
  const isLoading = ref(false)
  const error = ref(null)

  // Computed
  const isAuthenticated = computed(() => !!token.value)

  // Actions
  async function login(username, password) {
    isLoading.value = true
    error.value = null

    try {
      const response = await authService.login(username, password)
      user.value = response.user
      token.value = response.token
      return response
    } catch (err) {
      error.value = err.error || 'Erro ao fazer login'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function logout() {
    isLoading.value = true

    try {
      await authService.logout()
      user.value = null
      token.value = null
      error.value = null
    } catch (err) {
      error.value = err.error || 'Erro ao fazer logout'
    } finally {
      isLoading.value = false
    }
  }

  async function verifyToken() {
    try {
      const response = await authService.verifyToken()
      if (response.valid) {
        user.value = response.user
        return true
      }
      return false
    } catch (err) {
      user.value = null
      token.value = null
      return false
    }
  }

  function clearError() {
    error.value = null
  }

  return {
    // Estado
    user,
    token,
    isLoading,
    error,
    // Computed
    isAuthenticated,
    // Actions
    login,
    logout,
    verifyToken,
    clearError
  }
})
