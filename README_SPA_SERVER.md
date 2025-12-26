# 🚀 Servidor SPA para Frontend GuacPlayer

## 📋 Visão Geral

O GuacPlayer utiliza Vue.js com Vue Router, que requer um servidor HTTP que suporte **Single Page Applications (SPA)**. O servidor padrão Python `http.server` não suporta rotas SPA, causando erros 404 ao acessar rotas como `/`, `/dashboard`, etc.

Este documento explica como usar o servidor SPA customizado incluído no projeto.

---

## 🎯 Problema e Solução

### ❌ Problema
```bash
# Servidor Python padrão
python3 -m http.server 8080 --directory dist/

# Resultado:
GET / → 404 Not Found
GET /dashboard → 404 Not Found
GET /login → 404 Not Found
```

### ✅ Solução
```bash
# Servidor SPA customizado
python3 simple_spa_server.py

# Resultado:
GET / → index.html (Vue Router processa)
GET /dashboard → index.html (Vue Router processa)
GET /login → index.html (Vue Router processa)
```

---

## 🔧 Como Usar

### Opção 1: Desenvolvimento Local

```bash
# 1. Navegar para o diretório do frontend
cd frontend

# 2. Fazer build (se ainda não fez)
npm run build

# 3. Iniciar servidor SPA
python3 simple_spa_server.py
```

**Acesse**: http://localhost:8084

### Opção 2: Desenvolvimento com Hot Reload

```bash
# Usar Vite dev server (já suporta SPA)
cd frontend
npm run dev
```

**Acesse**: http://localhost:5173

### Opção 3: Docker Compose (Produção)

```bash
# O Nginx no container já está configurado para SPA
docker-compose up -d
```

**Acesse**: http://localhost:3000

---

## ⚙️ Configuração do Servidor

### Arquivo: `frontend/simple_spa_server.py`

```python
PORT = 8084  # Porta do servidor
DIRECTORY = "/home/ubuntu/guacplayer/frontend/dist"  # Diretório do build
```

### Funcionalidades

1. **Serve arquivos estáticos**
   - CSS, JS, imagens em `/assets/`
   - Favicon, manifest, etc.

2. **Redireciona rotas SPA**
   - Qualquer rota não encontrada → `index.html`
   - Vue Router processa a rota no cliente

3. **CORS habilitado**
   - Permite requisições do backend
   - Headers configurados

4. **Cache desabilitado**
   - Facilita desenvolvimento
   - Sempre serve versão mais recente

---

## 🌐 Rotas Suportadas

Todas as rotas do Vue Router funcionam:

| Rota | Componente | Autenticação |
|------|------------|--------------|
| `/` | Redirect → `/login` | Não |
| `/login` | LoginView | Não |
| `/dashboard` | DashboardView | Sim |
| `/connections` | ConnectionsView | Sim |
| `/connections/:id` | ConnectionDetailView | Sim |
| `/recording/:uuid` | RecordingView | Sim |

---

## 🐛 Troubleshooting

### Erro: "Address already in use"

**Causa**: Porta 8084 já está em uso

**Solução**:
```bash
# Encontrar processo
lsof -i :8084

# Matar processo
kill -9 <PID>

# Ou mudar a porta no arquivo
# Editar: PORT = 8085
```

### Erro: "Permission denied"

**Causa**: Arquivo não tem permissão de execução

**Solução**:
```bash
chmod +x simple_spa_server.py
```

### Erro: "Failed to fetch" no frontend

**Causa**: Backend não está rodando

**Solução**:
```bash
cd ../backend
python3 run.py
```

### Erro: 404 em arquivos CSS/JS

**Causa**: Build não foi feito ou está desatualizado

**Solução**:
```bash
npm run build
```

---

## 📊 Comparação de Servidores

| Servidor | SPA Support | CORS | Cache | Produção |
|----------|-------------|------|-------|----------|
| `python -m http.server` | ❌ | ❌ | ✅ | ❌ |
| `simple_spa_server.py` | ✅ | ✅ | ❌ | ⚠️ |
| `npm run dev` (Vite) | ✅ | ✅ | ❌ | ❌ |
| Nginx (Docker) | ✅ | ✅ | ✅ | ✅ |

**Recomendação**:
- **Desenvolvimento**: `npm run dev` (Vite)
- **Teste local**: `simple_spa_server.py`
- **Produção**: Docker Compose (Nginx)

---

## 🔒 Segurança

### ⚠️ Avisos

1. **Não usar em produção**
   - Este servidor é para desenvolvimento/teste
   - Use Nginx ou Apache em produção

2. **CORS aberto**
   - Aceita requisições de qualquer origem
   - Configure adequadamente em produção

3. **Sem HTTPS**
   - Tráfego não criptografado
   - Use proxy reverso com SSL em produção

---

## 🚀 Deploy em Produção

### Opção 1: Docker Compose (Recomendado)

```bash
# docker-compose.yml já configurado
docker-compose up -d
```

O Nginx está configurado para:
- ✅ Suportar rotas SPA
- ✅ Servir arquivos estáticos
- ✅ Proxy reverso para backend
- ✅ Compressão gzip
- ✅ Cache de assets

### Opção 2: Nginx Manual

```nginx
server {
    listen 80;
    server_name seu-dominio.com;
    root /var/www/guacplayer/dist;
    index index.html;

    # Serve arquivos estáticos
    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA fallback
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy para backend
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📝 Logs

### Ver logs do servidor

```bash
# Se rodando em background
tail -f /tmp/simple-spa.log

# Se rodando em foreground
# Logs aparecem no terminal
```

### Exemplo de logs

```
✓ Servidor SPA rodando em http://0.0.0.0:8084
✓ Servindo: /home/ubuntu/guacplayer/frontend/dist
✓ Suporte a Vue Router habilitado
Pressione Ctrl+C para parar

127.0.0.1 - - [26/Dec/2025 16:10:00] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [26/Dec/2025 16:10:01] "GET /assets/index.js HTTP/1.1" 200 -
127.0.0.1 - - [26/Dec/2025 16:10:02] "GET /dashboard HTTP/1.1" 200 -
```

---

## ✅ Checklist

Antes de usar o servidor SPA:

- [ ] Build do frontend feito (`npm run build`)
- [ ] Diretório `dist/` existe
- [ ] Porta 8084 está livre
- [ ] Backend está rodando (se precisar testar integração)
- [ ] Variáveis de ambiente configuradas (`.env`)

---

## 📚 Recursos Adicionais

- [Vue Router - HTML5 History Mode](https://router.vuejs.org/guide/essentials/history-mode.html)
- [Nginx SPA Configuration](https://router.vuejs.org/guide/essentials/history-mode.html#example-server-configurations)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

**Servidor SPA pronto para uso! 🎉**
