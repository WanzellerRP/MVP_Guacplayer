"""
Módulo para acesso a arquivos de gravação via NFS
Autor: GuacPlayer Team
Data: 2025
Descrição: Gerencia leitura de arquivos de vídeo armazenados em NFS
"""

import os
import json
from pathlib import Path
from app.config import Config
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class NFSHandler:
    """Gerenciador de acesso a arquivos NFS"""
    
    def __init__(self):
        """Inicializa o gerenciador NFS"""
        self.recordings_path = Path(Config.NFS_MOUNT_PATH)
        self._validate_path()
    
    def _validate_path(self):
        """Valida se o caminho NFS está acessível"""
        if not self.recordings_path.exists():
            logger.warning(f"Caminho NFS não existe: {self.recordings_path}")
            # Criar diretório se não existir (para desenvolvimento)
            try:
                self.recordings_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Diretório NFS criado: {self.recordings_path}")
            except Exception as e:
                logger.error(f"Erro ao criar diretório NFS: {str(e)}")
        else:
            logger.info(f"Caminho NFS validado: {self.recordings_path}")
    
    def get_recording_path(self, history_uuid):
        """
        Obtém o caminho completo de uma gravação
        
        Args:
            history_uuid: UUID da gravação
        
        Returns:
            Path: Caminho da gravação ou None se não existir
        """
        recording_dir = self.recordings_path / history_uuid
        
        if not recording_dir.exists():
            logger.warning(f"Diretório de gravação não encontrado: {recording_dir}")
            return None
        
        logger.info(f"Caminho de gravação encontrado: {recording_dir}")
        return recording_dir
    
    def get_recording_files(self, history_uuid):
        """
        Lista todos os arquivos de uma gravação
        
        Args:
            history_uuid: UUID da gravação
        
        Returns:
            list: Lista de arquivos encontrados
        """
        recording_dir = self.get_recording_path(history_uuid)
        
        if not recording_dir:
            return []
        
        try:
            files = []
            for file in recording_dir.iterdir():
                if file.is_file():
                    files.append({
                        'name': file.name,
                        'path': str(file),
                        'size': file.stat().st_size,
                        'modified': file.stat().st_mtime
                    })
            
            logger.info(f"Encontrados {len(files)} arquivos para gravação {history_uuid}")
            return sorted(files, key=lambda x: x['modified'], reverse=True)
        
        except Exception as e:
            logger.error(f"Erro ao listar arquivos de gravação {history_uuid}: {str(e)}")
            return []
    
    def get_video_file(self, history_uuid):
        """
        Obtém o arquivo de vídeo principal de uma gravação
        
        Args:
            history_uuid: UUID da gravação
        
        Returns:
            Path: Caminho do arquivo de vídeo ou None
        """
        recording_dir = self.get_recording_path(history_uuid)
        
        if not recording_dir:
            return None
        
        # Procurar por arquivos de vídeo (mp4, mkv, webm, etc)
        video_extensions = ['.mp4', '.mkv', '.webm', '.avi', '.mov']
        
        try:
            for file in recording_dir.iterdir():
                if file.is_file() and file.suffix.lower() in video_extensions:
                    logger.info(f"Arquivo de vídeo encontrado: {file}")
                    return file
            
            logger.warning(f"Nenhum arquivo de vídeo encontrado em {recording_dir}")
            return None
        
        except Exception as e:
            logger.error(f"Erro ao procurar arquivo de vídeo em {recording_dir}: {str(e)}")
            return None
    
    def get_recording_metadata(self, history_uuid):
        """
        Obtém metadados de uma gravação (se existirem)
        
        Args:
            history_uuid: UUID da gravação
        
        Returns:
            dict: Metadados ou dicionário vazio
        """
        recording_dir = self.get_recording_path(history_uuid)
        
        if not recording_dir:
            return {}
        
        metadata_file = recording_dir / 'metadata.json'
        
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    logger.info(f"Metadados carregados para gravação {history_uuid}")
                    return metadata
            except Exception as e:
                logger.error(f"Erro ao ler metadados de {history_uuid}: {str(e)}")
                return {}
        
        return {}
    
    def get_recording_info(self, history_uuid):
        """
        Obtém informações completas de uma gravação
        
        Args:
            history_uuid: UUID da gravação
        
        Returns:
            dict: Informações da gravação
        """
        recording_dir = self.get_recording_path(history_uuid)
        
        if not recording_dir:
            logger.warning(f"Gravação não encontrada: {history_uuid}")
            return None
        
        try:
            video_file = self.get_video_file(history_uuid)
            metadata = self.get_recording_metadata(history_uuid)
            files = self.get_recording_files(history_uuid)
            
            info = {
                'uuid': history_uuid,
                'path': str(recording_dir),
                'exists': True,
                'video_file': str(video_file) if video_file else None,
                'files': files,
                'metadata': metadata,
                'size_bytes': sum(f['size'] for f in files),
                'created_at': recording_dir.stat().st_ctime
            }
            
            logger.info(f"Informações de gravação {history_uuid} recuperadas")
            return info
        
        except Exception as e:
            logger.error(f"Erro ao obter informações de gravação {history_uuid}: {str(e)}")
            return None
    
    def file_exists(self, file_path):
        """
        Verifica se um arquivo existe e está dentro do caminho permitido
        
        Args:
            file_path: Caminho do arquivo
        
        Returns:
            bool: True se arquivo existe e está permitido
        """
        try:
            full_path = Path(file_path).resolve()
            base_path = self.recordings_path.resolve()
            
            # Verificar se o arquivo está dentro do diretório permitido
            if not str(full_path).startswith(str(base_path)):
                logger.warning(f"Tentativa de acesso a arquivo fora do diretório permitido: {file_path}")
                return False
            
            exists = full_path.exists() and full_path.is_file()
            
            if exists:
                logger.info(f"Arquivo validado: {file_path}")
            else:
                logger.warning(f"Arquivo não encontrado: {file_path}")
            
            return exists
        
        except Exception as e:
            logger.error(f"Erro ao validar arquivo {file_path}: {str(e)}")
            return False
