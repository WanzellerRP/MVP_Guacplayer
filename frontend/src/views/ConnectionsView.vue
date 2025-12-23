<template>
  <div class="min-h-screen bg-caixa-light">
    <Header />

    <main class="max-w-7xl mx-auto px-4 py-8">
      <!-- Cabeçalho -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-caixa-primary mb-2">Conexões</h1>
        <p class="text-gray-600">Gerencie e visualize todas as conexões Guacamole</p>
      </div>

      <!-- Barra de Busca -->
      <div class="card mb-6">
        <div class="flex gap-3">
          <input
            v-model="searchQuery"
            type="text"
            class="input-field flex-1"
            placeholder="Buscar conexão por nome ou protocolo..."
            @keyup.enter="handleSearch"
          />
          <button @click="handleSearch" class="btn-primary">
            🔍 Buscar
          </button>
          <button @click="clearSearch" class="btn-outline">
            Limpar
          </button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="connectionsStore.isLoading" class="text-center py-12">
        <div class="spinner mx-auto mb-4"></div>
        <p class="text-gray-600">Carregando conexões...</p>
      </div>

      <!-- Error -->
      <div v-else-if="connectionsStore.error" class="alert alert-error mb-6">
        {{ connectionsStore.error }}
      </div>

      <!-- Lista de Conexões -->
      <div v-else-if="connectionsStore.hasConnections" class="space-y-4 mb-8">
        <div
          v-for="connection in connectionsStore.connections"
          :key="connection.connection_id"
          class="card hover:shadow-lg transition-all cursor-pointer"
          @click="viewConnectionHistory(connection.connection_id)"
        >
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <h3 class="text-lg font-bold text-caixa-primary">
                {{ connection.connection_name }}
              </h3>
              <div class="flex gap-3 mt-2 flex-wrap">
                <span class="badge">{{ connection.protocol }}</span>
                <span v-if="connection.max_connections" class="text-sm text-gray-600">
                  Max: {{ connection.max_connections }} conexões
                </span>
                <span v-if="connection.proxy_hostname" class="text-sm text-gray-600">
                  {{ connection.proxy_hostname }}:{{ connection.proxy_port }}
                </span>
              </div>
            </div>
            <div class="text-3xl">→</div>
          </div>
        </div>
      </div>

      <!-- Sem Resultados -->
      <div v-else class="card text-center py-12">
        <p class="text-gray-600 text-lg">Nenhuma conexão encontrada</p>
      </div>

      <!-- Paginação -->
      <Pagination
        v-if="connectionsStore.hasConnections"
        :pagination="connectionsStore.pagination"
        @page-change="handlePageChange"
      />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useConnectionsStore } from '../stores/connections'
import Header from '../components/Header.vue'
import Pagination from '../components/Pagination.vue'

const router = useRouter()
const connectionsStore = useConnectionsStore()
const searchQuery = ref('')

async function loadConnections(page = 1) {
  try {
    await connectionsStore.fetchConnections(page, 20, searchQuery.value)
  } catch (error) {
    console.error('Erro ao carregar conexões:', error)
  }
}

function handleSearch() {
  loadConnections(1)
}

function clearSearch() {
  searchQuery.value = ''
  loadConnections(1)
}

function handlePageChange(page) {
  loadConnections(page)
}

function viewConnectionHistory(connectionId) {
  router.push({
    path: '/connections',
    query: { connectionId }
  })
}

onMounted(() => {
  loadConnections()
})
</script>

<style scoped>
.spinner {
  display: inline-block;
  width: 40px;
  height: 40px;
  border: 4px solid rgba(6, 67, 170, 0.3);
  border-top-color: #0643AA;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
