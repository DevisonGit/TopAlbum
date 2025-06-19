# 📚 Top Albums – Top Albums 

Neste projeto vamos construir uma API para gerenciar albums.

---

## 🧾 Descrição

A proposta do Top Albums é permitir o cadastro, listagem, atualização e remoção de albums. A aplicação é baseada em uma API REST desenvolvida com **FastAPI** e utiliza **Mongo** como banco de dados.

---

## 🚀 Funcionalidades

- 📚 Cadastrar novos Albums
- 🔍 Buscar Albums por título, artista ou ano de lançamento
- ✏️ Atualizar informações de Albums
- 🗑️ Remover Albums do acervo
- 🌐 API RESTful com documentação automática via Swagger

---

## ⚙️ Tecnologias utilizadas

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Mongo](https://www.mongodb.com/)
- [Beanie](https://beanie-odm.dev/) para validação de dados
- [Uvicorn](https://www.uvicorn.org/) como servidor ASGI
- [Docker](https://www.docker.com/)

---

## 📦 Requisitos

- Python 3.12+
- Poetry (ou pip)
- Mongo
- Docker

---

## 🛠️ Instalação

```bash 
  # Clone o repositório
git clone https://github.com/DevisonGit/TopAlbum.git
cd TopAlbum

# Instale as dependências com Poetry
poetry install

# Ativar o ambiente 
eval $(poetry env activate)
```

## ▶️ Como usar
```bash
  # Iniciar a aplicação
task run
```
Acesse a documentação interativa da API em:  
📄 http://localhost:8000/docs

## 🧪 Executar os testes
```bash
  # Executar os testes
task test
```