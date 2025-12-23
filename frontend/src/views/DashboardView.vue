<template>
  <div class="min-h-screen bg-caixa-light">
    <Header />

    <main class="max-w-7xl mx-auto px-4 py-8">
      <!-- Bem-vindo -->
      <div class="card mb-8 gradient-caixa text-white border-none">
        <h1 class="text-3xl font-bold mb-2">Bem-vindo, {{ authStore.user?.username }}!</h1>
        <p class="text-blue-100">Gerencie suas conexões Guacamole e reproduza gravações de sessões</p>
      </div>

      <!-- Grid de Estatísticas -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <!-- Card: Total de Conexões -->
        <div class="card">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm">Total de Conexões</p>
              <p class="text-3xl font-bold text-caixa-primary mt-2">
                {{ connectionsStore.totalConnections }}
              </p>
            </div>
            <div class="text-4xl">🔗</div>
          </div>
        </div>

        <!-- Card: Últimas Gravações -->
        <div class="card">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm">Últimas Gravações</p>
              <p class="text-3xl font-bold text-caixa-accent mt-2">
                {{ recentRecordings }}
              </p>
            </div>
            <div class="text-4xl">📹</div>
          </div>
        </div>

        <!-- Card: Status -->
        <div class="card">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm">Status do Sistema</p>
              <p class="text-lg font-bold text-caixa-success mt-2">✓ Operacional</p>
            </div>
            <div class="text-4xl">✅</div>
          </div>
        </div>
      </div>

      <!-- Ações Rápidas -->
      <div class="card mb-8">
        <h2 class="text-xl font-bold mb-4">Ações Rápidas</h2>
        <div class="flex flex-wrap gap-3">
          <router-link to="/connections" class="btn-primary">
            🔍 Ver Conexões
          </router-link>
          <button @click="refreshData" class="btn-secondary">
            🔄 Atualizar
          </button>
        </div>
      </div>

      <!-- Conexões Recentes -->
      <div class="card">
        <h2 class="text-xl font-bold mb-4">Conexões Recentes</h2>

        <div v-if="connectionsStore.isLoading" class="text-center py-8">
          <div class="spinner mx-auto"></div>
        </div>

        <div v-else-if="connectionsStore.hasConnections" class="space-y-3">
          <div
            v-for="connection in connectionsStore.connections.slice(0, 5)"
            :key="connection.connection_id"
            class="flex items-center justify-between p-4 bg-caixa-light rounded-lg hover:bg-gray-200 transition-colors"
          >
            <div>
              <p class="font-semibold">{{ connection.connection_name }}</p>
              <p class="text-sm text-gray-600">{{ connection.protocol }}</p>
            </div>
            <router-link
              :to="`/connections`"
              class="text-caixa-primary hover:text-caixa-accent font-semibold"
            >
              Ver →
            </router-link>
          </div>
        </div>

        <div v-else class="text-center py-8 text-gray-600">
          <p>Nenhuma conexão encontrada</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useConnectionsStore } from '../stores/connections'
import Header from '../components/Header.vue'

const authStore = useAuthStore()
const connectionsStore = useConnectionsStore()
const recentRecordings = ref(0)

async function loadData() {
  try {
    await connectionsStore.fetchConnections(1, 5)
  } catch (error) {
    console.error('Erro ao carregar dados:', error)
  }
}

function refreshData() {
  loadData()
}

onMounted(() => {
  loadData()
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
