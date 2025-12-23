<template>
  <div class="video-player-container">
    <div class="relative bg-black rounded-lg overflow-hidden shadow-lg">
      <!-- Video Element -->
      <video
        ref="videoElement"
        class="w-full h-auto"
        controls
        controlsList="nodownload"
        @play="onPlay"
        @pause="onPause"
        @ended="onEnded"
      >
        <source :src="videoSource" type="video/mp4">
        Seu navegador não suporta reprodução de vídeo HTML5.
      </video>

      <!-- Loading Spinner -->
      <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
        <div class="spinner"></div>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-75">
        <div class="text-center text-white">
          <p class="text-lg font-semibold mb-2">Erro ao carregar vídeo</p>
          <p class="text-sm">{{ error }}</p>
        </div>
      </div>
    </div>

    <!-- Controles Adicionais -->
    <div class="mt-4 flex gap-3">
      <button
        @click="handleDownload"
        :disabled="!videoSource || isLoading"
        class="btn-secondary btn-small"
      >
        📥 Baixar
      </button>
      <button
        @click="handleFullscreen"
        :disabled="!videoSource || isLoading"
        class="btn-primary btn-small"
      >
        🖥️ Tela Cheia
      </button>
    </div>

    <!-- Informações do Vídeo -->
    <div v-if="recordingInfo" class="mt-4 card">
      <h3 class="text-lg font-semibold mb-3">Informações da Gravação</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <p class="text-sm text-gray-600">Tamanho</p>
          <p class="font-semibold">{{ formatFileSize(recordingInfo.size_bytes) }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-600">Data de Criação</p>
          <p class="font-semibold">{{ formatDate(recordingInfo.created_at) }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-600">Total de Arquivos</p>
          <p class="font-semibold">{{ recordingInfo.files?.length || 0 }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-600">UUID</p>
          <p class="font-semibold text-xs truncate">{{ recordingInfo.uuid }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import * as recordingsService from '../services/recordings'

const props = defineProps({
  historyUuid: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['play', 'pause', 'ended', 'error'])

// Refs
const videoElement = ref(null)
const isLoading = ref(false)
const error = ref(null)
const recordingInfo = ref(null)

// Computed
const videoSource = computed(() => {
  return props.historyUuid ? recordingsService.getRecordingStreamUrl(props.historyUuid) : null
})

// Métodos
async function loadRecordingInfo() {
  try {
    isLoading.value = true
    const response = await recordingsService.getRecordingInfo(props.historyUuid)
    recordingInfo.value = response.data
  } catch (err) {
    error.value = err.error || 'Erro ao carregar informações da gravação'
    emit('error', error.value)
  } finally {
    isLoading.value = false
  }
}

function onPlay() {
  emit('play')
}

function onPause() {
  emit('pause')
}

function onEnded() {
  emit('ended')
}

function handleDownload() {
  recordingsService.downloadRecording(props.historyUuid)
}

function handleFullscreen() {
  if (videoElement.value) {
    if (videoElement.value.requestFullscreen) {
      videoElement.value.requestFullscreen()
    } else if (videoElement.value.webkitRequestFullscreen) {
      videoElement.value.webkitRequestFullscreen()
    }
  }
}

function formatFileSize(bytes) {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

function formatDate(timestamp) {
  return new Date(timestamp * 1000).toLocaleString('pt-BR')
}

// Lifecycle
onMounted(() => {
  loadRecordingInfo()
})

onUnmounted(() => {
  if (videoElement.value) {
    videoElement.value.pause()
    videoElement.value.src = ''
  }
})
</script>

<style scoped>
.video-player-container {
  width: 100%;
}

video {
  display: block;
  width: 100%;
  height: auto;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
