/**
 * Cliente HTTP para comunicação com Backend
 * Autor: GuacPlayer Team
 * Data: 2025
 * Descrição: Configuração do Axios e interceptadores
 */

import axios from 'axios'

// Criar instância do Axios
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

/**
 * Interceptador de requisição
 * Adiciona token JWT ao header Authorization
 */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

/**
 * Interceptador de resposta
 * Trata erros e redirecionamentos
 */
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Se receber 401, limpar token e redirecionar para login
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    
    return Promise.reject(error)
  }
)

export default api
