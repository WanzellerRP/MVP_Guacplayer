/**
 * Serviço de autenticação
 * Autor: GuacPlayer Team
 * Data: 2025
 * Descrição: Funções para login, logout e verificação de autenticação
 */

import api from './api'

/**
 * Realiza login do usuário
 * @param {string} username - Nome de usuário
 * @param {string} password - Senha
 * @returns {Promise} Resposta do servidor
 */
export async function login(username, password) {
  try {
    const response = await api.post('/auth/login', {
      username,
      password
    })
    
    if (response.data.success) {
      // Armazenar token e informações do usuário
      localStorage.setItem('auth_token', response.data.token)
      localStorage.setItem('user', JSON.stringify(response.data.user))
    }
    
    return response.data
  } catch (error) {
    throw error.response?.data || { error: 'Erro ao fazer login' }
  }
}

/**
 * Realiza logout do usuário
 * @returns {Promise} Resposta do servidor
 */
export async function logout() {
  try {
    await api.post('/auth/logout')
  } catch (error) {
    console.error('Erro ao fazer logout:', error)
  } finally {
    // Limpar dados locais
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')
  }
}

/**
 * Verifica se o token é válido
 * @returns {Promise} Dados do usuário se válido
 */
export async function verifyToken() {
  try {
    const response = await api.get('/auth/verify')
    return response.data
  } catch (error) {
    throw error.response?.data || { error: 'Token inválido' }
  }
}

/**
 * Obtém o usuário autenticado do localStorage
 * @returns {Object|null} Dados do usuário ou null
 */
export function getCurrentUser() {
  const user = localStorage.getItem('user')
  return user ? JSON.parse(user) : null
}

/**
 * Obtém o token de autenticação
 * @returns {string|null} Token ou null
 */
export function getAuthToken() {
  return localStorage.getItem('auth_token')
}

/**
 * Verifica se o usuário está autenticado
 * @returns {boolean} True se autenticado
 */
export function isAuthenticated() {
  return !!getAuthToken()
}
