"""
Serviços de negócio para conexões
Autor: GuacPlayer Team
Data: 2025
Descrição: Lógica de negócio para operações com conexões
"""

from app.database import GuacamoleQueries
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class ConnectionService:
    """Serviço para gerenciar operações com conexões"""
    
    def __init__(self):
        """Inicializa o serviço"""
        self.db = GuacamoleQueries()
    
    def get_connections_paginated(self, page=1, per_page=20):
        """
        Obtém conexões com paginação
        
        Args:
            page: Número da página (começa em 1)
            per_page: Quantidade de itens por página
        
        Returns:
            dict: Dados paginados
        """
        try:
            # Calcular offset
            offset = (page - 1) * per_page
            
            # Buscar conexões
            connections, total = self.db.get_connections(offset, per_page)
            
            # Enriquecer com parâmetros
            for conn in connections:
                conn['parameters'] = self.db.get_connection_parameters(conn['connection_id'])
            
            # Calcular paginação
            total_pages = (total + per_page - 1) // per_page
            
            logger.info(f"Conexões paginadas retornadas: página {page}, total {total}")
            
            return {
                'success': True,
                'data': connections,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'total_pages': total_pages
                }
            }
        
        except Exception as e:
            logger.error(f"Erro ao obter conexões paginadas: {str(e)}")
            raise
    
    def get_connection_detail(self, connection_id):
        """
        Obtém detalhes completos de uma conexão
        
        Args:
            connection_id: ID da conexão
        
        Returns:
            dict: Detalhes da conexão
        """
        try:
            # Buscar conexão
            connection = self.db.get_connection_by_id(connection_id)
            
            if not connection:
                logger.warning(f"Conexão {connection_id} não encontrada")
                return None
            
            # Adicionar parâmetros
            connection['parameters'] = self.db.get_connection_parameters(connection_id)
            
            logger.info(f"Detalhes da conexão {connection_id} recuperados")
            return connection
        
        except Exception as e:
            logger.error(f"Erro ao obter detalhes da conexão {connection_id}: {str(e)}")
            raise
    
    def get_connection_history_paginated(self, connection_id, page=1, per_page=20):
        """
        Obtém histórico de sessões de uma conexão com paginação
        
        Args:
            connection_id: ID da conexão
            page: Número da página
            per_page: Quantidade de itens por página
        
        Returns:
            dict: Dados paginados do histórico
        """
        try:
            # Verificar se conexão existe
            connection = self.db.get_connection_by_id(connection_id)
            if not connection:
                logger.warning(f"Conexão {connection_id} não encontrada")
                return None
            
            # Calcular offset
            offset = (page - 1) * per_page
            
            # Buscar histórico
            history, total = self.db.get_connection_history(connection_id, offset, per_page)
            
            # Calcular paginação
            total_pages = (total + per_page - 1) // per_page
            
            logger.info(f"Histórico da conexão {connection_id} recuperado: página {page}, total {total}")
            
            return {
                'success': True,
                'connection_id': connection_id,
                'connection_name': connection['connection_name'],
                'data': history,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'total_pages': total_pages
                }
            }
        
        except Exception as e:
            logger.error(f"Erro ao obter histórico da conexão {connection_id}: {str(e)}")
            raise
    
    def search_connections(self, query, page=1, per_page=20):
        """
        Busca conexões por nome ou protocolo
        
        Args:
            query: Termo de busca
            page: Número da página
            per_page: Quantidade de itens por página
        
        Returns:
            dict: Resultados da busca
        """
        try:
            # Para MVP, implementar busca simples em memória
            # Em produção, usar índice de busca no banco
            
            all_connections, total = self.db.get_connections(0, 1000)
            
            # Filtrar por query
            query_lower = query.lower()
            filtered = [
                conn for conn in all_connections
                if query_lower in conn['connection_name'].lower() or
                   query_lower in conn['protocol'].lower()
            ]
            
            # Aplicar paginação
            offset = (page - 1) * per_page
            paginated = filtered[offset:offset + per_page]
            
            total_filtered = len(filtered)
            total_pages = (total_filtered + per_page - 1) // per_page
            
            # Enriquecer com parâmetros
            for conn in paginated:
                conn['parameters'] = self.db.get_connection_parameters(conn['connection_id'])
            
            logger.info(f"Busca por '{query}' retornou {total_filtered} resultados")
            
            return {
                'success': True,
                'query': query,
                'data': paginated,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total_filtered,
                    'total_pages': total_pages
                }
            }
        
        except Exception as e:
            logger.error(f"Erro ao buscar conexões: {str(e)}")
            raise
