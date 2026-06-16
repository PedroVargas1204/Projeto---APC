# Geladeira Zero 🥗

Software em **Python 3** que ajuda famílias e estudantes a **reduzir o desperdício
de alimentos**. Mantém um inventário do que existe em casa, alerta sobre itens
próximos do vencimento, sugere receitas com IA Generativa usando o que está para
estragar e calcula o impacto evitado (kg de alimento salvo, CO₂, água e dinheiro).

Projeto da disciplina **Algoritmos e Programação de Computadores (APC)** — 2026/1.
Tema: **IA e meio ambiente**. Equipe: *Cientistas da Computaria*.

## Como rodar

Não precisa instalar nada além do Python 3:

```bash
cd geladeira_zero
python main.py
```

Use o menu numerado. Os dados são salvos automaticamente em `data/*.json`
entre execuções.

### IA de receitas (opcional)

Sem chave de API, o programa funciona normalmente e gera receitas pelo
**fallback** (cache/receita genérica) — ótimo para demonstrar offline.
Para ativar a IA de verdade, defina as variáveis de ambiente:

```bash
export IA_API_KEY="sua_chave"
export IA_API_URL="https://endpoint-da-sua-api"
pip install requests
```

## Estrutura dos módulos

| Arquivo            | Responsabilidade                                              | Conteúdos de APC                          |
|--------------------|--------------------------------------------------------------|-------------------------------------------|
| `main.py`          | Loop principal do menu; integra todos os módulos.            | while, if/elif, funções, módulos          |
| `interface.py`     | Telas (CLI) e **validação de toda entrada** do usuário.      | strings, while, condicionais              |
| `inventario.py`    | Cadastrar/listar itens, busca por nome, validade estimada.   | listas, dicionários, for, strings         |
| `alertas.py`       | Quais itens vencem e ordenação por urgência.                 | datetime, for, tuplas, condicionais       |
| `ia.py`            | Monta prompt, chama a IA, timeout e fallback.                | strings, try/except, requests             |
| `impacto.py`       | kg salvo, CO₂, água e dinheiro; agregação por categoria.     | for, floats, tuplas (retorno múltiplo)    |
| `persistencia.py`  | Lê/grava JSON e exporta histórico para CSV.                  | json, csv, arquivos, exceções             |

## Dados (`data/`)

- `base_alimentos.json` — base de alimentos com validade típica, preço/kg, CO₂/kg e água/kg.
- `inventario.json` — itens atualmente em casa.
- `historico.json` — itens consumidos ou descartados (base do cálculo de impacto).
- `usuario.json` — perfil e preferências (vegetariano, alergias, tempo de preparo).
- `receitas_cache.json` — cache de receitas geradas pela IA (fallback).

## Requisitos atendidos

RF01–RF11 (menu, cadastro, validade estimada, inventário ordenado, alertas,
receita por IA, marcar consumido/descartado, impacto, economia, preferências, CSV)
e RNF01–RNF07 (Python puro, código comentado/docstrings, validação de entradas,
persistência JSON, timeout+fallback da IA, menu rápido).

## Próximos passos

- Ampliar `base_alimentos.json` para 80+ itens (com fontes EMBRAPA/CEMPRE).
- Integrar uma API de IA real (Gemini/OpenAI/Claude) em `ia.py`.
- Migrar a interface para **Streamlit** reaproveitando todo o backend.
- Rodar o experimento com voluntários e analisar com `pandas` + `scipy`.

Licença: MIT.
