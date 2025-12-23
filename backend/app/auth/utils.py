"""
Utilitários de autenticação
Autor: GuacPlayer Team
Data: 2025
Descrição: Funções para geração e validação de tokens JWT
"""

import jwt
import hashlib
import binascii
from datetime import datetime, timedelta
from app.config import Config
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def generate_jwt_token(user_id, username):
    """
    Gera um token JWT para o usuário
    
    Args:
        user_id: ID do usuário
        username: Nome de usuário
    
    Returns:
        str: Token JWT
    """
    try:
        payload = {
            'user_id': user_id,
            'username': username,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
        }
        
        token = jwt.encode(
            payload,
            Config.JWT_SECRET_KEY,
            algorithm='HS256'
        )
        
        logger.info(f"Token JWT gerado para usuário {username}")
        return token
    
    except Exception as e:
        logger.error(f"Erro ao gerar token JWT: {str(e)}")
        raise


def verify_jwt_token(token):
    """
    Verifica e decodifica um token JWT
    
    Args:
        token: Token JWT a verificar
    
    Returns:
        dict: Dados do token se válido
    
    Raises:
        jwt.InvalidTokenError: Se token for inválido
    """
    try:
        payload = jwt.decode(
            token,
            Config.JWT_SECRET_KEY,
            algorithms=['HS256']
        )
        
        logger.info(f"Token JWT validado para usuário {payload.get('username')}")
        return payload
    
    except jwt.ExpiredSignatureError:
        logger.warning("Token JWT expirado")
        raise
    except jwt.InvalidTokenError as e:
        logger.warning(f"Token JWT inválido: {str(e)}")
        raise


def hash_password_guacamole(password, salt=None):
    """
    Gera hash de senha no formato do Guacamole (SHA256 + salt)
    
    Args:
        password: Senha em texto plano
        salt: Salt a usar (gerado aleatoriamente se não fornecido)
    
    Returns:
        tuple: (hash_hex, salt_hex)
    """
    try:
        import os
        
        # Usar salt fornecido ou gerar novo
        if salt is None:
            salt = os.urandom(32)
        elif isinstance(salt, str):
            salt = binascii.unhexlify(salt)
        
        # Combinar senha + salt e fazer hash
        password_bytes = password.encode('utf-8')
        hash_obj = hashlib.sha256(password_bytes + salt)
        hash_hex = hash_obj.hexdigest()
        salt_hex = binascii.hexlify(salt).decode('utf-8')
        
        logger.info("Hash de senha gerado com sucesso")
        return hash_hex, salt_hex
    
    except Exception as e:
        logger.error(f"Erro ao gerar hash de senha: {str(e)}")
        raise


def verify_password_guacamole(password, password_hash, password_salt):
    """
    Verifica se a senha corresponde ao hash armazenado
    
    Args:
        password: Senha em texto plano
        password_hash: Hash armazenado
        password_salt: Salt armazenado
    
    Returns:
        bool: True se senha é válida
    """
    try:
        # Regenerar hash com a senha fornecida e o salt armazenado
        new_hash, _ = hash_password_guacamole(password, password_salt)
        
        # Comparar hashes
        is_valid = new_hash == password_hash
        
        if is_valid:
            logger.info("Senha validada com sucesso")
        else:
            logger.warning("Senha inválida")
        
        return is_valid
    
    except Exception as e:
        logger.error(f"Erro ao verificar senha: {str(e)}")
        return False
