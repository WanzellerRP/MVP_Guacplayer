#!/usr/bin/env python3
"""
Servidor HTTP simples para Single Page Applications (SPA)
Redireciona todas as rotas não-existentes para index.html
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

PORT = 8084
DIRECTORY = "/home/ubuntu/guacplayer/frontend/dist"

class SPAHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_GET(self):
        # Tenta servir o arquivo solicitado
        # Se não existir, serve o index.html
        
        # Para arquivos na pasta assets, serve diretamente
        if self.path.startswith('/assets/'):
            return super().do_GET()
        
        # Para index.html explícito
        if self.path == '/' or self.path == '/index.html':
            self.path = '/index.html'
            return super().do_GET()
        
        # Para qualquer outra rota, tenta servir
        # Se falhar (404), serve index.html
        original_path = self.path
        result = super().do_GET()
        
        return result
    
    def send_error(self, code, message=None, explain=None):
        # Se for 404, serve o index.html ao invés de erro
        if code == 404:
            self.path = '/index.html'
            return super().do_GET()
        return super().send_error(code, message, explain)
    
    def end_headers(self):
        # CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    server = HTTPServer(('0.0.0.0', PORT), SPAHandler)
    print(f"✓ Servidor SPA rodando em http://0.0.0.0:{PORT}")
    print(f"✓ Servindo: {DIRECTORY}")
    print("✓ Suporte a Vue Router habilitado")
    print("Pressione Ctrl+C para parar\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Servidor encerrado")
