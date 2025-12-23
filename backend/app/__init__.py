"""
GuacPlayer Backend - Aplicação Flask para gerenciamento de conexões Guacamole
Autor: GuacPlayer Team
Data: 2025
Descrição: Inicializa a aplicação Flask com todas as configurações necessárias
"""

from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.utils.logger import setup_logger

# Configurar logger
logger = setup_logger(__name__)


def create_app(config_class=Config):
    """
    Factory function para criar e configurar a aplicação Flask.
    
    Args:
        config_class: Classe de configuração (padrão: Config)
    
    Returns:
        Flask: Aplicação Flask configurada
    """
    app = Flask(__name__)
    
    # Carregar configurações
    app.config.from_object(config_class)
    
    # Configurar CORS para aceitar requisições do frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    logger.info("Aplicação Flask criada com sucesso")
    
    # Registrar blueprints
    from app.auth.routes import auth_bp
    from app.connections.routes import connections_bp
    from app.recordings.routes import recordings_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(connections_bp, url_prefix='/api/connections')
    app.register_blueprint(recordings_bp, url_prefix='/api/recordings')
    
    logger.info("Blueprints registrados com sucesso")
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Endpoint para verificar saúde da aplicação"""
        return {
            'status': 'healthy',
            'service': 'GuacPlayer Backend',
            'version': '1.0.0'
        }, 200
    
    logger.info("Aplicação Flask inicializada com sucesso")
    return app
