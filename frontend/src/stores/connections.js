/**
 * Store de conexões (Pinia)
 * Autor: GuacPlayer Team
 * Data: 2025
 * Descrição: Gerencia estado de conexões e histórico
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as connectionsService from '../services/connections'

export const useConnectionsStore = defineStore('connections', () => {
  // Estado
  const connections = ref([])
  const currentConnection = ref(null)
  const connectionHistory = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const pagination = ref({
    page: 1,
    per_page: 20,
    total: 0,
    total_pages: 0
  })
  const searchQuery = ref('')

  // Computed
  const hasConnections = computed(() => connections.value.length > 0)
  const totalConnections = computed(() => pagination.value.total)

  // Actions
  async function fetchConnections(page = 1, perPage = 20, search = '') {
    isLoading.value = true
    error.value = null

    try {
      const response = await connectionsService.getConnections(page, perPage, search)
      connections.value = response.data
      pagination.value = response.pagination
      searchQuery.value = search
      return response
    } catch (err) {
      error.value = err.error || 'Erro ao buscar conexões'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchConnectionDetail(connectionId) {
    isLoading.value = true
    error.value = null

    try {
      const response = await connectionsService.getConnectionDetail(connectionId)
      currentConnection.value = response.data
      return response
    } catch (err) {
      error.value = err.error || 'Erro ao buscar detalhes da conexão'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchConnectionHistory(connectionId, page = 1, perPage = 20) {
    isLoading.value = true
    error.value = null

    try {
      const response = await connectionsService.getConnectionHistory(connectionId, page, perPage)
      connectionHistory.value = response.data
      pagination.value = response.pagination
      return response
    } catch (err) {
      error.value = err.error || 'Erro ao buscar histórico'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  function clearError() {
    error.value = null
  }

  function resetCurrentConnection() {
    currentConnection.value = null
  }

  return {
    // Estado
    connections,
    currentConnection,
    connectionHistory,
    isLoading,
    error,
    pagination,
    searchQuery,
    // Computed
    hasConnections,
    totalConnections,
    // Actions
    fetchConnections,
    fetchConnectionDetail,
    fetchConnectionHistory,
    clearError,
    resetCurrentConnection
  }
})
