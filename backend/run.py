"""
Ponto de entrada da aplicação GuacPlayer Backend
Autor: GuacPlayer Team
Data: 2025
Descrição: Script para iniciar a aplicação Flask
"""

import os
from app import create_app
from app.config import config_by_name
from app.utils.logger import setup_logger

# Configurar logger
logger = setup_logger(__name__)

# Obter ambiente
env = os.getenv('FLASK_ENV', 'development')
logger.info(f"Ambiente: {env}")

# Criar aplicação
app = create_app(config_by_name.get(env, config_by_name['default']))

if __name__ == '__main__':
    # Configurações de execução
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Iniciando aplicação em {host}:{port}")
    logger.info(f"Debug: {debug}")
    
    # Executar aplicação
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug
    )
