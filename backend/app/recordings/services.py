"""
Serviços de negócio para gravações
Autor: GuacPlayer Team
Data: 2025
Descrição: Lógica de negócio para operações com gravações
"""

from app.nfs_handler import NFSHandler
from app.database import GuacamoleQueries
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class RecordingService:
    """Serviço para gerenciar operações com gravações"""
    
    def __init__(self):
        """Inicializa o serviço"""
        self.nfs = NFSHandler()
        self.db = GuacamoleQueries()
    
    def get_recording_info(self, history_uuid):
        """
        Obtém informações de uma gravação
        
        Args:
            history_uuid: UUID da gravação
        
        Returns:
            dict: Informações da gravação
        """
        try:
            info = self.nfs.get_recording_info(history_uuid)
            
            if not info:
                logger.warning(f"Gravação {history_uuid} não encontrada")
                return None
            
            logger.info(f"Informações da gravação {history_uuid} recuperadas")
            return info
        
        except Exception as e:
            logger.error(f"Erro ao obter informações da gravação {history_uuid}: {str(e)}")
            raise
    
    def get_recording_video(self, history_uuid):
        """
        Obtém o arquivo de vídeo de uma gravação
        
        Args:
            history_uuid: UUID da gravação
        
        Returns:
            Path: Caminho do arquivo de vídeo
        """
        try:
            video_file = self.nfs.get_video_file(history_uuid)
            
            if not video_file:
                logger.warning(f"Arquivo de vídeo não encontrado para gravação {history_uuid}")
                return None
            
            logger.info(f"Arquivo de vídeo encontrado para gravação {history_uuid}")
            return video_file
        
        except Exception as e:
            logger.error(f"Erro ao obter vídeo da gravação {history_uuid}: {str(e)}")
            raise
    
    def get_recording_files(self, history_uuid):
        """
        Lista todos os arquivos de uma gravação
        
        Args:
            history_uuid: UUID da gravação
        
        Returns:
            list: Lista de arquivos
        """
        try:
            files = self.nfs.get_recording_files(history_uuid)
            
            logger.info(f"Arquivos da gravação {history_uuid} listados: {len(files)} arquivos")
            return files
        
        except Exception as e:
            logger.error(f"Erro ao listar arquivos da gravação {history_uuid}: {str(e)}")
            raise
    
    def validate_recording_access(self, history_uuid):
        """
        Valida se uma gravação existe e é acessível
        
        Args:
            history_uuid: UUID da gravação
        
        Returns:
            bool: True se gravação é acessível
        """
        try:
            recording_path = self.nfs.get_recording_path(history_uuid)
            
            if not recording_path:
                logger.warning(f"Gravação {history_uuid} não é acessível")
                return False
            
            logger.info(f"Gravação {history_uuid} validada com sucesso")
            return True
        
        except Exception as e:
            logger.error(f"Erro ao validar gravação {history_uuid}: {str(e)}")
            return False
