"""
Sistema de logging da aplicação GuacPlayer
Autor: GuacPlayer Team
Data: 2025
Descrição: Configuração centralizada de logging com suporte a múltiplos níveis
"""

import logging
import json
from datetime import datetime
from app.config import Config


class JSONFormatter(logging.Formatter):
    """Formatter customizado para logs em formato JSON"""
    
    def format(self, record):
        """
        Formata registro de log como JSON
        
        Args:
            record: Registro de log
        
        Returns:
            str: JSON formatado
        """
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)


def setup_logger(name):
    """
    Configura logger para um módulo específico
    
    Args:
        name: Nome do módulo
    
    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    # Definir nível de logging
    log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Usar JSON formatter
    formatter = JSONFormatter()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger
