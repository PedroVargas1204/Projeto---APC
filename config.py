"""
config.py
---------
Todos os ajustes do Geladeira Zero num lugar so.

Mudar um parametro do sistema (limite de alerta, timeout da IA, periodo do
impacto, etc.) e uma edicao de UMA linha aqui — sem precisar caçar o numero
espalhado pelos modulos nem mexer na logica.
"""

# ----- Alertas -----
DIAS_ALERTA = 3             # itens que vencem em ate X dias geram alerta (RF05)
DIAS_RECEITA_AMPLIADO = 7   # janela maior usada na receita quando nao ha urgencias

# ----- IA -----
TIMEOUT_IA = 10             # segundos de paciencia com a API antes de desistir
TEMPO_PREPARO_PADRAO = 40   # minutos (usado se o usuario nao definiu preferencia)

# ----- Impacto -----
PESO_UNIDADE_KG = 0.15      # peso medio aproximado de "1 unid" em kg
PERIODO_IMPACTO_DIAS = 30   # janela padrao do calculo de impacto

# ----- Interface -----
LARGURA_TELA = 60           # largura interna das telas (a borda usa +2)

# ----- Arquivos de dados (dentro da pasta data/) -----
ARQ_BASE = "base_alimentos.json"
ARQ_INVENTARIO = "inventario.json"
ARQ_HISTORICO = "historico.json"
ARQ_USUARIO = "usuario.json"
ARQ_CACHE = "receitas_cache.json"
