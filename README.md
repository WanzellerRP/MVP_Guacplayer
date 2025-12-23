# GuacPlayer - Visualizador de Conexões e Gravações Guacamole

![GuacPlayer](https://img.shields.io/badge/GuacPlayer-v1.0.0-blue?style=for-the-badge&logo=appveyor)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-green?style=for-the-badge&logo=vue.js)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?style=for-the-badge&logo=docker)

**GuacPlayer** é uma aplicação MVP (Minimum Viável Product) desenvolvida para visualizar conexões do **Apache Guacamole** e reproduzir vídeos de sessões gravadas. A aplicação foi construída de forma modular, seguindo as melhores práticas de desenvolvimento e prevendo evoluções futuras.

## ✨ Funcionalidades

- **Visualização de Conexões**: Lista paginada de todas as conexões configuradas no Guacamole.
- **Player de Vídeo Integrado**: Reprodução de gravações de sessões diretamente no navegador, utilizando um player HTML5.
- **Identidade Visual CAIXA**: Interface segue rigorosamente a identidade visual da CAIXA Econômica Federal.
- **Backend em Python**: API RESTful desenvolvida com Flask para gerenciar conexões e gravações.
- **Frontend em Vue.js**: Interface reativa e moderna construída com Vue.js 3 e Vite.
- **Containerização**: Aplicação totalmente containerizada com Docker e Docker Compose para fácil deploy.
- **Acesso a Gravações via NFS**: O backend é capaz de ler os arquivos de vídeo gravados e disponibilizá-los para o frontend.

## 🏛️ Arquitetura

A solução é baseada em uma arquitetura de microsserviços, com um backend responsável pela lógica de negócio e um frontend para a interface com o usuário.

- **Backend (Python/Flask)**: Conecta-se ao banco de dados PostgreSQL do Guacamole para consultar informações sobre as conexões e acessa o sistema de arquivos de rede (NFS) para ler os vídeos das sessões gravadas.
- **Frontend (Vue.js)**: Consome a API do backend para exibir a lista de conexões e reproduzir os vídeos.

Para mais detalhes, consulte o documento de arquitetura: `ARCHITECTURE.md`.

## 🚀 Tecnologias Utilizadas

- **Backend**: Python 3.11, Flask, Psycopg2
- **Frontend**: Vue.js 3, Vite, Pinia, Axios, TailwindCSS
- **Banco de Dados**: PostgreSQL
- **Containerização**: Docker, Docker Compose

## 🏁 Começando

Siga os passos abaixo para executar a aplicação em seu ambiente local.

### Pré-requisitos

- Docker
- Docker Compose

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/guacplayer.git
   cd guacplayer
   ```

2. **Configure as variáveis de ambiente:**
   Copie o arquivo `.env.example` para `.env` e ajuste as configurações, se necessário.
   ```bash
   cp .env.example .env
   ```

3. **Suba os containers:**
   ```bash
   docker-compose up --build -d
   ```

### Acesso

- **Frontend**: `http://localhost:3000`
- **Backend**: `http://localhost:5000`

## ⚙️ Configuração

As principais configurações da aplicação podem ser ajustadas no arquivo `.env` na raiz do projeto. Consulte os arquivos `.env.example` nos diretórios `backend` e `frontend` para mais detalhes.

## API Endpoints

O backend expõe uma API RESTful para o frontend. A documentação completa dos endpoints pode ser encontrada no código-fonte, nos diretórios `backend/app/*/routes.py`.

## 📁 Estrutura de Diretórios

A estrutura do projeto foi organizada da seguinte forma:

```
guacplayer/
├── backend/         # Código-fonte do backend
├── frontend/        # Código-fonte do frontend
├── docker-compose.yml # Orquestração dos containers
├── ARCHITECTURE.md  # Documentação da arquitetura
├── README.md        # Este arquivo
└── ...
```

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
