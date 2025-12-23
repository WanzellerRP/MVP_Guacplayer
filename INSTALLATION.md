# Guia de Instalação - GuacPlayer

Este guia detalha os passos necessários para instalar e executar a aplicação GuacPlayer em um ambiente de desenvolvimento ou produção.

## 1. Pré-requisitos

Antes de começar, certifique-se de que os seguintes softwares estão instalados em sua máquina:

- **Docker**: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
- **Docker Compose**: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)
- **Git**: [https://git-scm.com/downloads](https://git-scm.com/downloads)

## 2. Instalação

### Passo 1: Clonar o Repositório

Clone o repositório do GuacPlayer para sua máquina local:

```bash
git clone https://github.com/seu-usuario/guacplayer.git
cd guacplayer
```

### Passo 2: Configurar Variáveis de Ambiente

A aplicação utiliza um arquivo `.env` para gerenciar as configurações. Copie o arquivo de exemplo e ajuste conforme necessário:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações específicas, como credenciais do banco de dados e chaves secretas.

### Passo 3: Build e Execução com Docker Compose

Com o Docker e Docker Compose instalados, execute o seguinte comando na raiz do projeto para construir as imagens e iniciar os containers:

```bash
docker-compose up --build -d
```

O comando acima irá:
- Construir as imagens do backend e frontend.
- Iniciar os containers em modo detached (`-d`).
- Criar uma rede interna para a comunicação entre os serviços.
- Criar volumes para persistência de dados.

## 3. Verificação

Após a execução do `docker-compose up`, verifique se os containers estão rodando corretamente:

```bash
docker-compose ps
```

Você deverá ver três containers em execução: `guacplayer-backend`, `guacplayer-frontend` e `guacplayer-postgres`.

### Acesso à Aplicação

- **Frontend**: Abra seu navegador e acesse `http://localhost:3000`.
- **Backend API**: A API estará disponível em `http://localhost:5000`.

## 4. Configuração Adicional

### Banco de Dados

O `docker-compose.yml` inclui um serviço PostgreSQL pré-configurado. Se você deseja utilizar um banco de dados externo, ajuste as variáveis de ambiente `DB_*` no arquivo `.env`.

### Armazenamento de Gravações (NFS)

O backend espera que o diretório de gravações do Guacamole esteja montado em `/recordings` dentro do container. Para isso, você pode ajustar o volume `recordings` no `docker-compose.yml` para montar um diretório local ou um volume NFS.

Exemplo para montar um diretório local:

```yaml
volumes:
  recordings:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /caminho/para/suas/gravacoes
```

## 5. Troubleshooting

- **Logs**: Para visualizar os logs dos containers, utilize o comando:
  ```bash
  docker-compose logs -f <nome-do-servico>
  # Ex: docker-compose logs -f backend
  ```

- **Problemas de Conexão**: Verifique se as portas `3000` e `5000` não estão sendo utilizadas por outros serviços em sua máquina.

- **Permissões de Arquivo**: Em ambientes Linux, certifique-se de que o Docker tem permissão para acessar os diretórios montados como volumes.

## 6. Deploy em Produção

Para um ambiente de produção, recomenda-se:

- Utilizar um proxy reverso (como Nginx ou Traefik) na frente da aplicação para gerenciar SSL e roteamento.
- Configurar as variáveis de ambiente com valores seguros e não utilizar as chaves padrão.
- Monitorar os containers e a saúde da aplicação.
- Realizar backups regulares do banco de dados.
