"""
Decoradores customizados para a aplicação
Autor: GuacPlayer Team
Data: 2025
Descrição: Decoradores para autenticação, validação e tratamento de erros
"""

from functools import wraps
from flask import request, jsonify
import jwt
from app.config import Config
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def token_required(f):
    """
    Decorador para verificar se o token JWT é válido
    
    Args:
        f: Função a ser decorada
    
    Returns:
        function: Função decorada
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Verificar se token está no header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                logger.warning("Token malformado no header Authorization")
                return jsonify({'error': 'Token malformado'}), 401
        
        if not token:
            logger.warning("Token não fornecido")
            return jsonify({'error': 'Token não fornecido'}), 401
        
        try:
            # Decodificar e validar token
            data = jwt.decode(
                token,
                Config.JWT_SECRET_KEY,
                algorithms=['HS256']
            )
            current_user = data.get('user_id')
            
            if not current_user:
                logger.warning("Token inválido: user_id não encontrado")
                return jsonify({'error': 'Token inválido'}), 401
            
            # Passar user_id para a função
            kwargs['current_user'] = current_user
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token expirado")
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token inválido: {str(e)}")
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def handle_errors(f):
    """
    Decorador para tratamento centralizado de erros
    
    Args:
        f: Função a ser decorada
    
    Returns:
        function: Função decorada
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Erro de validação: {str(e)}")
            return jsonify({'error': f'Erro de validação: {str(e)}'}), 400
        except KeyError as e:
            logger.error(f"Campo obrigatório faltando: {str(e)}")
            return jsonify({'error': f'Campo obrigatório faltando: {str(e)}'}), 400
        except Exception as e:
            logger.error(f"Erro interno do servidor: {str(e)}", exc_info=True)
            return jsonify({'error': 'Erro interno do servidor'}), 500
    
    return decorated_function


def validate_json(*expected_fields):
    """
    Decorador para validar se o request contém JSON com campos obrigatórios
    
    Args:
        *expected_fields: Campos esperados no JSON
    
    Returns:
        function: Decorador
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                logger.warning("Request não contém JSON")
                return jsonify({'error': 'Request deve ser JSON'}), 400
            
            data = request.get_json()
            
            for field in expected_fields:
                if field not in data:
                    logger.warning(f"Campo obrigatório faltando: {field}")
                    return jsonify({'error': f'Campo obrigatório: {field}'}), 400
            
            kwargs['data'] = data
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator
