"""
Módulo de acesso ao banco de dados PostgreSQL do Guacamole
Autor: GuacPlayer Team
Data: 2025
Descrição: Gerencia conexão com PostgreSQL e consultas ao banco Guacamole
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from app.config import Config
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class DatabaseConnection:
    """Gerenciador de conexão com PostgreSQL"""
    
    def __init__(self):
        """Inicializa o gerenciador de conexão"""
        self.config = {
            'host': Config.DB_HOST,
            'port': Config.DB_PORT,
            'database': Config.DB_NAME,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD
        }
    
    @contextmanager
    def get_connection(self):
        """
        Context manager para obter conexão com o banco de dados
        
        Yields:
            psycopg2.connection: Conexão com o banco
        """
        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            logger.info("Conexão com PostgreSQL estabelecida")
            yield conn
            conn.commit()
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Erro ao conectar ao PostgreSQL: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
                logger.info("Conexão com PostgreSQL fechada")
    
    @contextmanager
    def get_cursor(self):
        """
        Context manager para obter cursor com dicionário
        
        Yields:
            psycopg2.cursor: Cursor com resultados como dicionário
        """
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            try:
                yield cursor
            finally:
                cursor.close()


class GuacamoleQueries:
    """Classe com consultas específicas do Guacamole"""
    
    def __init__(self):
        """Inicializa o gerenciador de queries"""
        self.db = DatabaseConnection()
    
    def get_connections(self, offset=0, limit=20):
        """
        Obtém lista paginada de conexões
        
        Args:
            offset: Número de registros a pular
            limit: Número máximo de registros a retornar
        
        Returns:
            tuple: (lista de conexões, total de registros)
        """
        try:
            with self.db.get_cursor() as cursor:
                # Contar total de conexões
                cursor.execute("SELECT COUNT(*) as total FROM guacamole_connection")
                total = cursor.fetchone()['total']
                
                # Buscar conexões com paginação
                query = """
                    SELECT 
                        connection_id,
                        connection_name,
                        protocol,
                        parent_id,
                        max_connections,
                        max_connections_per_user,
                        proxy_hostname,
                        proxy_port
                    FROM guacamole_connection
                    ORDER BY connection_name
                    LIMIT %s OFFSET %s
                """
                
                cursor.execute(query, (limit, offset))
                connections = cursor.fetchall()
                
                logger.info(f"Recuperadas {len(connections)} conexões (offset: {offset}, limit: {limit})")
                return connections, total
        
        except psycopg2.Error as e:
            logger.error(f"Erro ao buscar conexões: {str(e)}")
            raise
    
    def get_connection_by_id(self, connection_id):
        """
        Obtém detalhes de uma conexão específica
        
        Args:
            connection_id: ID da conexão
        
        Returns:
            dict: Detalhes da conexão
        """
        try:
            with self.db.get_cursor() as cursor:
                query = """
                    SELECT 
                        connection_id,
                        connection_name,
                        protocol,
                        parent_id,
                        max_connections,
                        max_connections_per_user,
                        proxy_hostname,
                        proxy_port
                    FROM guacamole_connection
                    WHERE connection_id = %s
                """
                
                cursor.execute(query, (connection_id,))
                connection = cursor.fetchone()
                
                if connection:
                    logger.info(f"Conexão {connection_id} recuperada com sucesso")
                    return connection
                else:
                    logger.warning(f"Conexão {connection_id} não encontrada")
                    return None
        
        except psycopg2.Error as e:
            logger.error(f"Erro ao buscar conexão {connection_id}: {str(e)}")
            raise
    
    def get_connection_parameters(self, connection_id):
        """
        Obtém parâmetros de uma conexão
        
        Args:
            connection_id: ID da conexão
        
        Returns:
            dict: Parâmetros da conexão
        """
        try:
            with self.db.get_cursor() as cursor:
                query = """
                    SELECT 
                        parameter_name,
                        parameter_value
                    FROM guacamole_connection_parameter
                    WHERE connection_id = %s
                """
                
                cursor.execute(query, (connection_id,))
                params = cursor.fetchall()
                
                # Converter para dicionário
                parameters = {param['parameter_name']: param['parameter_value'] for param in params}
                
                logger.info(f"Parâmetros da conexão {connection_id} recuperados")
                return parameters
        
        except psycopg2.Error as e:
            logger.error(f"Erro ao buscar parâmetros da conexão {connection_id}: {str(e)}")
            raise
    
    def get_connection_history(self, connection_id, offset=0, limit=20):
        """
        Obtém histórico de sessões de uma conexão
        
        Args:
            connection_id: ID da conexão
            offset: Número de registros a pular
            limit: Número máximo de registros a retornar
        
        Returns:
            tuple: (lista de sessões, total de registros)
        """
        try:
            with self.db.get_cursor() as cursor:
                # Contar total de sessões
                count_query = """
                    SELECT COUNT(*) as total 
                    FROM guacamole_connection_history 
                    WHERE connection_id = %s
                """
                cursor.execute(count_query, (connection_id,))
                total = cursor.fetchone()['total']
                
                # Buscar histórico com paginação
                query = """
                    SELECT 
                        history_id,
                        connection_id,
                        user_id,
                        start_date,
                        end_date,
                        remote_host
                    FROM guacamole_connection_history
                    WHERE connection_id = %s
                    ORDER BY start_date DESC
                    LIMIT %s OFFSET %s
                """
                
                cursor.execute(query, (connection_id, limit, offset))
                history = cursor.fetchall()
                
                logger.info(f"Histórico da conexão {connection_id} recuperado ({len(history)} registros)")
                return history, total
        
        except psycopg2.Error as e:
            logger.error(f"Erro ao buscar histórico da conexão {connection_id}: {str(e)}")
            raise
    
    def get_user_by_id(self, user_id):
        """
        Obtém informações de um usuário
        
        Args:
            user_id: ID do usuário
        
        Returns:
            dict: Informações do usuário
        """
        try:
            with self.db.get_cursor() as cursor:
                query = """
                    SELECT 
                        user_id,
                        username,
                        password_hash,
                        disabled
                    FROM guacamole_user
                    WHERE user_id = %s
                """
                
                cursor.execute(query, (user_id,))
                user = cursor.fetchone()
                
                if user:
                    logger.info(f"Usuário {user_id} recuperado com sucesso")
                    return user
                else:
                    logger.warning(f"Usuário {user_id} não encontrado")
                    return None
        
        except psycopg2.Error as e:
            logger.error(f"Erro ao buscar usuário {user_id}: {str(e)}")
            raise
    
    def get_user_by_username(self, username):
        """
        Obtém informações de um usuário pelo nome de usuário
        
        Args:
            username: Nome de usuário
        
        Returns:
            dict: Informações do usuário
        """
        try:
            with self.db.get_cursor() as cursor:
                query = """
                    SELECT 
                        user_id,
                        username,
                        password_hash,
                        password_salt,
                        disabled
                    FROM guacamole_user
                    WHERE username = %s
                """
                
                cursor.execute(query, (username,))
                user = cursor.fetchone()
                
                if user:
                    logger.info(f"Usuário '{username}' recuperado com sucesso")
                    return user
                else:
                    logger.warning(f"Usuário '{username}' não encontrado")
                    return None
        
        except psycopg2.Error as e:
            logger.error(f"Erro ao buscar usuário '{username}': {str(e)}")
            raise
