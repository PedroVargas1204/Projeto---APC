# Geladeira Zero 🥗

Software em **Python 3** que ajuda a **reduzir o desperdício de alimentos**: mantém um
inventário do que existe em casa, alerta sobre itens próximos do vencimento, sugere
receitas com IA Generativa usando o que está para estragar e calcula o impacto evitado
(kg de alimento salvo, CO₂, água e dinheiro).

Disciplina **APC — 2026/1**. Tema: **IA e meio ambiente**. Equipe: *Cientistas da Computaria*.

## Como rodar
Copiar o repositório, usar o comando cd(change directory para acessar a pasta clonada e rodar o programa usando o comando python main.py

Caso não funcione o comando git acessar esse link e fazer download para windowns x64 https://git-scm.com/install/windows

```bash
git clone https://github.com/PedroVargas1204/Projeto---APC
cd Projeto---APC
python main.py
```

Os dados são salvos automaticamente em `data/*.json` entre execuções. Sem chave de API,
a IA cai no **fallback** e o programa funciona offline.

### IA de receitas (opcional)
```bash
export IA_API_KEY="sua_chave"
export IA_API_URL="https://endpoint-da-sua-api"
pip install requests
```

## Organização do código

Todos os arquivos ficam na raiz (estrutura plana, fácil de importar). Dois princípios
guiam a organização para facilitar alterações:

1. **Tudo que é ajuste fica em `config.py`** — limite de alerta, timeout da IA, período
   do impacto, peso por unidade, nomes dos arquivos. Mudar um parâmetro é editar uma
   linha lá, sem caçar números pelos módulos.
2. **Lógica separada da tela** — funções de cálculo (`calcular_alertas`,
   `calcular_impacto`, `sugerir_validade`, `consultar_ia`...) não usam `print`/`input`;
   quem desenha as telas são as funções `exibir_*`. Isso permite trocar a interface
   (ex.: CLI → Streamlit) sem mexer na lógica.

| Arquivo            | Responsabilidade                                          |
|--------------------|-----------------------------------------------------------|
| `config.py`        | **Todos os ajustes do sistema num lugar só.**             |
| `main.py`          | Loop do menu; integra todos os módulos.                   |
| `interface.py`     | Telas (CLI) e validação de entrada.                       |
| `inventario.py`    | Cadastrar/listar itens, busca, validade estimada.         |
| `alertas.py`       | Quais itens vencem e ordenação por urgência.              |
| `ia.py`            | Prompt, chamada à IA, timeout, cache e fallback.          |
| `impacto.py`       | kg salvo, CO₂, água e dinheiro; agregação por categoria.  |
| `persistencia.py`  | Lê/grava JSON e exporta CSV.                              |

Dados em `data/`: `base_alimentos.json` (catálogo, versionado) e os arquivos de runtime
(`inventario`, `historico`, `usuario`, `receitas_cache`), que o programa recria sozinho.

## Próximos passos (melhorias por integrante)
- **A:** abrir alertas na entrada; refatorar o menu para dicionário de funções; cores ANSI.
- **B:** ampliar a base para 80+; busca difusa (`difflib`); corrigir o `or 7`.
- **C:** conectar a API real (Gemini); filtrar ingredientes por alergia antes do prompt.
- **D:** registrar `data_evento` ao consumir; backup antes de salvar; peso por unidade na base.

Licença: MIT.
