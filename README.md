# Processador de Arquivo

Essa aplicação FastAPI recebe um arquivo csv, o processa usando Celery e salva informações sobre esse arquivo numa base Postgres.

## Principais dependências do projeto


- uv
- FastAPI
- Uvicorn
- Celery
- Redis
- SQLAlchemy
- Alembic
- Pytest

## Estrutura do Projeto 


- `src/`: Código da aplicação
  - `main.py`: Aplicativo do Fastapi
  - `api/`: Rotas da aplicação
  - `core/`: Arquivos de configuracão de banco de dados e de variáveis de ambiente
  - `models/`: Modelo de Banco de Dados usando SQLAlchemy 
  - `schemas/`: Schemas do Pydantic
  - `tasks/`: Tasks Celery para processar o arquivo
- `tests/`: Arquivo de testes
- `alembic/`: Arquivos de migração do banco de dados
- `entrypoint.sh`: Ponto de entrada da aplicação ao ser executada pelo container
- `docker-compose.yml`: Arquivo de configuração usado pelo ```docker compose```



## Rodando a aplicação

Para rodar a aplicação você precisar ter o ```Docker``` e o ```Docker Compose``` instalados.
Com isso ok, basta executar

```
$ docker compose up --build
```
ou dependendo da sua versão instalada
```
$ docker-compose up --build
```

Pronto, agora basta acessar a ```http://localhost:8000/docs``` para visualizar a documentação interativa e poder
fazer uso da API desenvolvida.
Existe o endpoint que recebe o arquivo a ser processado e os endpoints para consultar ```Users```, ```Addresses``` e ```UserEvents```.

## Setup local e Tests 

Esse projeto usa a biblioteca ```uv``` para gerenciar as suas dependências e também o ambiente virtual.

Etapas:

1 - Criar ambiente virtual
```
$ uv venv
```

2 - Criar ambiente virtual
```
$ source ./venv/bin/activate
```

3 - Instalar dependências
```
$ uv pip install -e .
```

4 - Rodar Tests

```
$ make tests
```
