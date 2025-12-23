"""
Rotas de gravações
Autor: GuacPlayer Team
Data: 2025
Descrição: Endpoints para gerenciamento de gravações
"""

from flask import Blueprint, request, jsonify, send_file
from app.recordings.services import RecordingService
from app.utils.decorators import handle_errors, token_required
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# Criar blueprint de gravações
recordings_bp = Blueprint('recordings', __name__)

# Instanciar serviço
service = RecordingService()


@recordings_bp.route('/<history_uuid>', methods=['GET'])
@handle_errors
@token_required
def get_recording_info(history_uuid, current_user):
    """
    Endpoint para obter informações de uma gravação
    
    Args:
        history_uuid: UUID da gravação
    
    Returns:
        dict: Informações da gravação
    """
    try:
        logger.info(f"Obtendo informações da gravação {history_uuid}")
        
        # Validar acesso
        if not service.validate_recording_access(history_uuid):
            logger.warning(f"Acesso negado à gravação {history_uuid}")
            return jsonify({'error': 'Gravação não encontrada'}), 404
        
        # Obter informações
        info = service.get_recording_info(history_uuid)
        
        if not info:
            logger.warning(f"Gravação {history_uuid} não encontrada")
            return jsonify({'error': 'Gravação não encontrada'}), 404
        
        return jsonify({
            'success': True,
            'data': {
                'uuid': info['uuid'],
                'path': info['path'],
                'video_file': info['video_file'],
                'files': info['files'],
                'size_bytes': info['size_bytes'],
                'created_at': info['created_at'],
                'metadata': info['metadata']
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Erro ao obter informações da gravação {history_uuid}: {str(e)}")
        return jsonify({'error': 'Erro ao obter informações da gravação'}), 500


@recordings_bp.route('/<history_uuid>/stream', methods=['GET'])
@handle_errors
@token_required
def stream_recording(history_uuid, current_user):
    """
    Endpoint para fazer stream de um arquivo de vídeo
    
    Query Parameters:
        range: Range HTTP para streaming (opcional)
    
    Args:
        history_uuid: UUID da gravação
    
    Returns:
        file: Arquivo de vídeo
    """
    try:
        logger.info(f"Iniciando stream da gravação {history_uuid}")
        
        # Validar acesso
        if not service.validate_recording_access(history_uuid):
            logger.warning(f"Acesso negado ao stream da gravação {history_uuid}")
            return jsonify({'error': 'Gravação não encontrada'}), 404
        
        # Obter arquivo de vídeo
        video_file = service.get_recording_video(history_uuid)
        
        if not video_file:
            logger.warning(f"Arquivo de vídeo não encontrado para gravação {history_uuid}")
            return jsonify({'error': 'Arquivo de vídeo não encontrado'}), 404
        
        # Enviar arquivo
        logger.info(f"Enviando arquivo de vídeo: {video_file}")
        
        return send_file(
            str(video_file),
            mimetype='video/mp4',
            as_attachment=False
        ), 200
    
    except Exception as e:
        logger.error(f"Erro ao fazer stream da gravação {history_uuid}: {str(e)}")
        return jsonify({'error': 'Erro ao fazer stream da gravação'}), 500


@recordings_bp.route('/<history_uuid>/download', methods=['GET'])
@handle_errors
@token_required
def download_recording(history_uuid, current_user):
    """
    Endpoint para baixar um arquivo de gravação
    
    Args:
        history_uuid: UUID da gravação
    
    Returns:
        file: Arquivo para download
    """
    try:
        logger.info(f"Iniciando download da gravação {history_uuid}")
        
        # Validar acesso
        if not service.validate_recording_access(history_uuid):
            logger.warning(f"Acesso negado ao download da gravação {history_uuid}")
            return jsonify({'error': 'Gravação não encontrada'}), 404
        
        # Obter arquivo de vídeo
        video_file = service.get_recording_video(history_uuid)
        
        if not video_file:
            logger.warning(f"Arquivo de vídeo não encontrado para gravação {history_uuid}")
            return jsonify({'error': 'Arquivo de vídeo não encontrado'}), 404
        
        # Enviar arquivo para download
        logger.info(f"Enviando arquivo para download: {video_file}")
        
        return send_file(
            str(video_file),
            mimetype='video/mp4',
            as_attachment=True,
            download_name=f'{history_uuid}.mp4'
        ), 200
    
    except Exception as e:
        logger.error(f"Erro ao baixar gravação {history_uuid}: {str(e)}")
        return jsonify({'error': 'Erro ao baixar gravação'}), 500


@recordings_bp.route('/<history_uuid>/files', methods=['GET'])
@handle_errors
@token_required
def list_recording_files(history_uuid, current_user):
    """
    Endpoint para listar arquivos de uma gravação
    
    Args:
        history_uuid: UUID da gravação
    
    Returns:
        dict: Lista de arquivos
    """
    try:
        logger.info(f"Listando arquivos da gravação {history_uuid}")
        
        # Validar acesso
        if not service.validate_recording_access(history_uuid):
            logger.warning(f"Acesso negado aos arquivos da gravação {history_uuid}")
            return jsonify({'error': 'Gravação não encontrada'}), 404
        
        # Listar arquivos
        files = service.get_recording_files(history_uuid)
        
        return jsonify({
            'success': True,
            'uuid': history_uuid,
            'files': files
        }), 200
    
    except Exception as e:
        logger.error(f"Erro ao listar arquivos da gravação {history_uuid}: {str(e)}")
        return jsonify({'error': 'Erro ao listar arquivos'}), 500
