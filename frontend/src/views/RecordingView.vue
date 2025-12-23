<template>
  <div class="min-h-screen bg-caixa-light">
    <Header />

    <main class="max-w-7xl mx-auto px-4 py-8">
      <!-- Voltar -->
      <router-link to="/connections" class="text-caixa-primary hover:text-caixa-accent mb-6 inline-block">
        ← Voltar para Conexões
      </router-link>

      <!-- Cabeçalho -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-caixa-primary mb-2">Gravação</h1>
        <p class="text-gray-600">{{ recordingUuid }}</p>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="text-center py-12">
        <div class="spinner mx-auto mb-4"></div>
        <p class="text-gray-600">Carregando gravação...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="alert alert-error mb-6">
        {{ error }}
      </div>

      <!-- Conteúdo -->
      <div v-else class="space-y-8">
        <!-- Player de Vídeo -->
        <VideoPlayer
          :history-uuid="recordingUuid"
          @play="onPlay"
          @pause="onPause"
          @ended="onEnded"
          @error="onError"
        />

        <!-- Informações da Gravação -->
        <div class="card">
          <h2 class="text-2xl font-bold mb-4 text-caixa-primary">Detalhes</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <p class="text-sm text-gray-600 mb-1">UUID da Gravação</p>
              <p class="font-semibold break-all">{{ recordingUuid }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600 mb-1">Status</p>
              <span class="badge badge-success">✓ Disponível</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Header from '../components/Header.vue'
import VideoPlayer from '../components/VideoPlayer.vue'

const route = useRoute()
const recordingUuid = ref(route.params.uuid || '')
const isLoading = ref(false)
const error = ref(null)

function onPlay() {
  console.log('Vídeo iniciado')
}

function onPause() {
  console.log('Vídeo pausado')
}

function onEnded() {
  console.log('Vídeo finalizado')
}

function onError(err) {
  error.value = err
}

onMounted(() => {
  if (!recordingUuid.value) {
    error.value = 'UUID da gravação não fornecido'
  }
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
