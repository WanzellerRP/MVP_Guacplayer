# Dockerfile para Frontend GuacPlayer
# Autor: GuacPlayer Team
# Data: 2025

# Stage 1: Build
FROM node:22-alpine AS builder

WORKDIR /app

# Copiar package.json e package-lock.json
COPY package*.json ./

# Instalar dependências
RUN npm install

# Copiar código
COPY . .

# Build
RUN npm run build

# Stage 2: Serve
FROM node:22-alpine

WORKDIR /app

# Instalar servidor HTTP simples
RUN npm install -g http-server

# Copiar arquivos buildados do stage anterior
COPY --from=builder /app/dist ./dist

# Expor porta
EXPOSE 3000

# Variáveis de ambiente
ENV NODE_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000/ || exit 1

# Comando de inicialização
CMD ["http-server", "dist", "-p", "3000", "--cors"]
