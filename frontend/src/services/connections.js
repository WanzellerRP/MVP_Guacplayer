/**
 * Serviço de conexões
 * Autor: GuacPlayer Team
 * Data: 2025
 * Descrição: Funções para gerenciar conexões e histórico
 */

import api from './api'

/**
 * Obtém lista de conexões com paginação
 * @param {number} page - Número da página
 * @param {number} perPage - Itens por página
 * @param {string} search - Termo de busca (opcional)
 * @returns {Promise} Lista de conexões
 */
export async function getConnections(page = 1, perPage = 20, search = '') {
  try {
    const params = {
      page,
      per_page: perPage
    }
    
    if (search) {
      params.search = search
    }
    
    const response = await api.get('/connections', { params })
    return response.data
  } catch (error) {
    throw error.response?.data || { error: 'Erro ao buscar conexões' }
  }
}

/**
 * Obtém detalhes de uma conexão específica
 * @param {number} connectionId - ID da conexão
 * @returns {Promise} Detalhes da conexão
 */
export async function getConnectionDetail(connectionId) {
  try {
    const response = await api.get(`/connections/${connectionId}`)
    return response.data
  } catch (error) {
    throw error.response?.data || { error: 'Erro ao buscar conexão' }
  }
}

/**
 * Obtém histórico de sessões de uma conexão
 * @param {number} connectionId - ID da conexão
 * @param {number} page - Número da página
 * @param {number} perPage - Itens por página
 * @returns {Promise} Histórico paginado
 */
export async function getConnectionHistory(connectionId, page = 1, perPage = 20) {
  try {
    const params = {
      page,
      per_page: perPage
    }
    
    const response = await api.get(`/connections/${connectionId}/history`, { params })
    return response.data
  } catch (error) {
    throw error.response?.data || { error: 'Erro ao buscar histórico' }
  }
}
