/**
 * Serviço de gravações
 * Autor: GuacPlayer Team
 * Data: 2025
 * Descrição: Funções para gerenciar gravações e vídeos
 */

import api from './api'

/**
 * Obtém informações de uma gravação
 * @param {string} historyUuid - UUID da gravação
 * @returns {Promise} Informações da gravação
 */
export async function getRecordingInfo(historyUuid) {
  try {
    const response = await api.get(`/recordings/${historyUuid}`)
    return response.data
  } catch (error) {
    throw error.response?.data || { error: 'Erro ao buscar informações da gravação' }
  }
}

/**
 * Obtém URL para streaming de vídeo
 * @param {string} historyUuid - UUID da gravação
 * @returns {string} URL do stream
 */
export function getRecordingStreamUrl(historyUuid) {
  const token = localStorage.getItem('auth_token')
  return `${import.meta.env.VITE_API_URL || 'http://localhost:5000/api'}/recordings/${historyUuid}/stream?token=${token}`
}

/**
 * Obtém URL para download de vídeo
 * @param {string} historyUuid - UUID da gravação
 * @returns {string} URL do download
 */
export function getRecordingDownloadUrl(historyUuid) {
  const token = localStorage.getItem('auth_token')
  return `${import.meta.env.VITE_API_URL || 'http://localhost:5000/api'}/recordings/${historyUuid}/download?token=${token}`
}

/**
 * Lista arquivos de uma gravação
 * @param {string} historyUuid - UUID da gravação
 * @returns {Promise} Lista de arquivos
 */
export async function getRecordingFiles(historyUuid) {
  try {
    const response = await api.get(`/recordings/${historyUuid}/files`)
    return response.data
  } catch (error) {
    throw error.response?.data || { error: 'Erro ao listar arquivos' }
  }
}

/**
 * Baixa um arquivo de gravação
 * @param {string} historyUuid - UUID da gravação
 */
export function downloadRecording(historyUuid) {
  const url = getRecordingDownloadUrl(historyUuid)
  const link = document.createElement('a')
  link.href = url
  link.download = `recording_${historyUuid}.mp4`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
