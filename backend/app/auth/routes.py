"""
Rotas de autenticação
Autor: GuacPlayer Team
Data: 2025
Descrição: Endpoints para login, logout e verificação de autenticação
"""

from flask import Blueprint, request, jsonify
from app.database import GuacamoleQueries
from app.auth.utils import generate_jwt_token, verify_jwt_token, verify_password_guacamole
from app.utils.decorators import handle_errors, validate_json, token_required
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# Criar blueprint de autenticação
auth_bp = Blueprint('auth', __name__)

# Instanciar queries do Guacamole
db_queries = GuacamoleQueries()


@auth_bp.route('/login', methods=['POST'])
@handle_errors
@validate_json('username', 'password')
def login(data):
    """
    Endpoint para autenticação de usuário
    
    Args:
        data: JSON com username e password
    
    Returns:
        dict: Token JWT e informações do usuário
    """
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        logger.warning("Username ou password vazios")
        return jsonify({'error': 'Username e password são obrigatórios'}), 400
    
    try:
        # Buscar usuário no banco de dados
        user = db_queries.get_user_by_username(username)
        
        if not user:
            logger.warning(f"Tentativa de login com usuário inexistente: {username}")
            return jsonify({'error': 'Credenciais inválidas'}), 401
        
        # Verificar se usuário está desabilitado
        if user.get('disabled'):
            logger.warning(f"Tentativa de login com usuário desabilitado: {username}")
            return jsonify({'error': 'Usuário desabilitado'}), 401
        
        # Verificar senha
        password_hash = user.get('password_hash')
        password_salt = user.get('password_salt')
        
        if not verify_password_guacamole(password, password_hash, password_salt):
            logger.warning(f"Tentativa de login com senha incorreta: {username}")
            return jsonify({'error': 'Credenciais inválidas'}), 401
        
        # Gerar token JWT
        token = generate_jwt_token(user['user_id'], username)
        
        logger.info(f"Usuário {username} autenticado com sucesso")
        
        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'id': user['user_id'],
                'username': username
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Erro durante autenticação: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500


@auth_bp.route('/verify', methods=['GET'])
@handle_errors
@token_required
def verify(current_user):
    """
    Endpoint para verificar se o token é válido
    
    Args:
        current_user: ID do usuário extraído do token
    
    Returns:
        dict: Status de verificação
    """
    try:
        # Buscar informações do usuário
        user = db_queries.get_user_by_id(current_user)
        
        if not user:
            logger.warning(f"Usuário {current_user} não encontrado durante verificação")
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        logger.info(f"Token verificado para usuário {user['username']}")
        
        return jsonify({
            'valid': True,
            'user': {
                'id': user['user_id'],
                'username': user['username']
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Erro durante verificação de token: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500


@auth_bp.route('/logout', methods=['POST'])
@handle_errors
@token_required
def logout(current_user):
    """
    Endpoint para logout (apenas para registro)
    
    Args:
        current_user: ID do usuário extraído do token
    
    Returns:
        dict: Status de logout
    """
    try:
        user = db_queries.get_user_by_id(current_user)
        logger.info(f"Usuário {user['username']} realizou logout")
        
        return jsonify({
            'success': True,
            'message': 'Logout realizado com sucesso'
        }), 200
    
    except Exception as e:
        logger.error(f"Erro durante logout: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
