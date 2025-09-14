# Sistema RAG - Busca Semântica com LangChain

Sistema de busca semântica inteligente que utiliza **RAG (Retrieval-Augmented Generation)** para responder perguntas baseadas em documentos PDF. O sistema processa documentos, cria embeddings vetoriais e permite consultas em linguagem natural com respostas contextualmente relevantes.

## 🎯 Finalidade do Projeto

Este projeto implementa um sistema RAG básico que:

- **Processa documentos PDF** e os fragmenta em chunks menores
- **Gera embeddings vetoriais** usando a API do Google Generative AI
- **Armazena vetores** em banco PostgreSQL com extensão pgvector
- **Realiza buscas semânticas** por similaridade no banco de dados Postgres + pgvector
- **Gera respostas contextuais** através do resultado da busca semântica e consultas em modelos de IA
- **Oferece interface de chat** interativa no terminal


### Tecnologias Utilizadas
- **Ubunut 24.04** - Sistema Operacional utilizado
- **Python 3.12+** - Linguagem principal
- **LangChain** - Framework para aplicações com LLM
- **PostgreSQL + pgvector** - Banco de dados vetorial
- **Google Generative AI** - Embeddings e modelo de chat
- **Docker** - Containerização do banco de dados
- **PyPDF** - Processamento de documentos PDF

## 📁 Estrutura do Projeto

```
semantic_search_langchain/
├── 📄 README.md                 # Documentação do projeto
├── 📋 requirements.txt          # Dependências Python
├── ⚙️ pyproject.toml           # Configurações de formatação
├── 🐳 docker-compose.yml       # Configuração do PostgreSQL
├── 📄 document.pdf             # Documento de exemplo
├── 🚫 .gitignore              # Arquivos ignorados pelo Git
└── 📁 src/                    # Código fonte
    ├── 📊 ingest.py           # Processamento e ingestão de PDFs
    ├── 🔍 search.py           # Lógica de busca semântica
    └── 💬 chat.py             # Interface de chat interativa
```

### Descrição dos Módulos

#### `src/ingest.py`
- **Função**: Processa documentos PDF e os insere no banco vetorial
- **Responsabilidades**:
  - Carrega e fragmenta documentos PDF
  - Gera embeddings usando Google Generative AI
  - Armazena vetores no PostgreSQL com pgvector
  - Enriquece metadados dos documentos

#### `src/search.py`
- **Função**: Implementa a lógica de busca semântica
- **Responsabilidades**:
  - Conecta com o banco de dados vetorial
  - Transforma perguntas em embeddings
  - Realiza busca por similaridade
  - Retorna documentos mais relevantes

#### `src/chat.py`
- **Função**: Interface de chat interativa
- **Responsabilidades**:
  - Gerencia loop de conversação
  - Integra busca semântica com geração de respostas
  - Formata e exibe respostas ao usuário
  - Trata erros e comandos especiais

## 🚀 Como Executar o Projeto

### Pré-requisitos

- **Python 3.12+**
- **Docker e Docker Compose**
- **Chave de API do Google Generative AI**

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/alexanco/semantic_search_langchain.git
cd semantic_search_langchain
```

### Passo 2: Configurar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Configurar Variáveis de Ambiente

#### Obs: Esse projeto foi amplamente testado utilizando o Gemini 


- Crie uma API Key da Google.
- Modelo de embeddings: models/embedding-001
- Modelo de LLM para responder: gemini-2.5-flash-lite

1. **Copie o arquivo de exemplo**:

```bash
cp .env.example .env
```

2. **Configure as variáveis no arquivo `.env`**:
```env
# API do Google Generative AI
GOOGLE_API_KEY=sua_chave_google_aqui
GOOGLE_EMBEDDING_MODEL=models/embedding-001

# Configurações do Banco de Dados
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=gpt5_collection

# Caminho do documento PDF
PDF_PATH=/caminho/absoluto/para/document.pdf
```

### Passo 5: Subir o Banco de Dados

```bash
# Iniciar PostgreSQL com pgvector
docker compose up -d postgres

# Aguardar o banco estar pronto
docker compose logs postgres

# Instalar extensão vector
docker exec postgres_rag psql -U postgres -d rag -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### Passo 6: Processar Documento

```bash
# Executar ingestão do PDF
python src/ingest.py
```

**Saída esperada**:
```
✅ Documento processado com sucesso!
📊 67 fragmentos inseridos no banco de dados
```

### Passo 7: Executar o Chat

```bash
# Iniciar interface de chat
python src/chat.py
```

**Exemplo de uso**:
```
🤖 Chat RAG - Sistema de Busca Semântica
==================================================
Digite suas perguntas sobre o documento carregado.
Comandos: 'sair', 'exit', 'quit' para encerrar
==================================================
✅ Sistema inicializado com sucesso!

🧑 Você: Qual o faturamento da empresa Alfa Agronegócio?
🔍 Buscando informações relevantes...
💭 Gerando resposta...
🤖 Bot: Com base no documento, a empresa Alfa Agronegócio Indústria possui um faturamento de R$ 85.675.568,77 e foi fundada em 1931.

🧑 Você: sair
👋 Obrigado por usar o chat! Até logo!
```


### Verificar Status do Banco

```bash
# Verificar se o banco está rodando
docker compose ps

# Ver logs do PostgreSQL
docker compose logs postgres

# Conectar diretamente ao banco
docker exec -it postgres_rag psql -U postgres -d rag

# Verificar documentos inseridos
docker exec postgres_rag psql -U postgres -d rag -c "SELECT COUNT(*) FROM langchain_pg_embedding;"
```

