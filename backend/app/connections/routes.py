"""
Rotas de conexões
Autor: GuacPlayer Team
Data: 2025
Descrição: Endpoints para gerenciamento de conexões
"""

from flask import Blueprint, request, jsonify
from app.connections.services import ConnectionService
from app.utils.decorators import handle_errors, token_required
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# Criar blueprint de conexões
connections_bp = Blueprint('connections', __name__)

# Instanciar serviço
service = ConnectionService()


@connections_bp.route('', methods=['GET'])
@handle_errors
@token_required
def list_connections(current_user):
    """
    Endpoint para listar conexões com paginação
    
    Query Parameters:
        page: Número da página (padrão: 1)
        per_page: Itens por página (padrão: 20)
        search: Termo de busca (opcional)
    
    Returns:
        dict: Lista de conexões paginada
    """
    try:
        # Obter parâmetros de paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '', type=str).strip()
        
        # Validar parâmetros
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
        
        logger.info(f"Listando conexões: página {page}, per_page {per_page}, search '{search}'")
        
        # Buscar conexões
        if search:
            result = service.search_connections(search, page, per_page)
        else:
            result = service.get_connections_paginated(page, per_page)
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Erro ao listar conexões: {str(e)}")
        return jsonify({'error': 'Erro ao listar conexões'}), 500


@connections_bp.route('/<int:connection_id>', methods=['GET'])
@handle_errors
@token_required
def get_connection(connection_id, current_user):
    """
    Endpoint para obter detalhes de uma conexão
    
    Args:
        connection_id: ID da conexão
    
    Returns:
        dict: Detalhes da conexão
    """
    try:
        logger.info(f"Obtendo detalhes da conexão {connection_id}")
        
        connection = service.get_connection_detail(connection_id)
        
        if not connection:
            logger.warning(f"Conexão {connection_id} não encontrada")
            return jsonify({'error': 'Conexão não encontrada'}), 404
        
        return jsonify({
            'success': True,
            'data': connection
        }), 200
    
    except Exception as e:
        logger.error(f"Erro ao obter conexão {connection_id}: {str(e)}")
        return jsonify({'error': 'Erro ao obter conexão'}), 500


@connections_bp.route('/<int:connection_id>/history', methods=['GET'])
@handle_errors
@token_required
def get_connection_history(connection_id, current_user):
    """
    Endpoint para obter histórico de sessões de uma conexão
    
    Query Parameters:
        page: Número da página (padrão: 1)
        per_page: Itens por página (padrão: 20)
    
    Args:
        connection_id: ID da conexão
    
    Returns:
        dict: Histórico paginado
    """
    try:
        # Obter parâmetros de paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Validar parâmetros
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
        
        logger.info(f"Obtendo histórico da conexão {connection_id}: página {page}")
        
        result = service.get_connection_history_paginated(connection_id, page, per_page)
        
        if not result:
            logger.warning(f"Conexão {connection_id} não encontrada")
            return jsonify({'error': 'Conexão não encontrada'}), 404
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Erro ao obter histórico da conexão {connection_id}: {str(e)}")
        return jsonify({'error': 'Erro ao obter histórico'}), 500
