from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# Modelo de dados para uma licitação
class Licitacao(BaseModel):
    id: int
    titulo: str
    orgao: str
    categoria: str
    data_publicacao: datetime
    url: str

# Banco de dados temporário (simulando um banco real)
db_licitacoes = []

# Rota para adicionar uma nova licitação
@app.post("/licitacoes", response_model=Licitacao)
def adicionar_licitacao(licitacao: Licitacao):
    db_licitacoes.append(licitacao)
    return licitacao

# Rota para listar todas as licitações
@app.get("/licitacoes", response_model=List[Licitacao])
def listar_licitacoes():
    return db_licitacoes

# Rota para obter detalhes de uma licitação específica
@app.get("/licitacoes/{id}", response_model=Licitacao)
def obter_licitacao(id: int):
    for licitacao in db_licitacoes:
        if licitacao.id == id:
            return licitacao
    raise HTTPException(status_code=404, detail="Licitação não encontrada")

# Rota para buscar licitações com filtros
@app.get("/licitacoes/search", response_model=List[Licitacao])
def buscar_licitacoes(orgao: Optional[str] = None, categoria: Optional[str] = None):
    resultados = db_licitacoes
    if orgao:
        resultados = [l for l in resultados if l.orgao.lower() == orgao.lower()]
    if categoria:
        resultados = [l for l in resultados if l.categoria.lower() == categoria.lower()]
    return resultados
