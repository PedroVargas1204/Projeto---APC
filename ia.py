"""
ia.py
-----
Geracao de receitas com IA Generativa (nucleo do produto, RF06).

Monta o prompt a partir dos ingredientes que estao para vencer, chama
a API da IA com timeout e, se algo falhar, usa um cache local ou uma
receita generica (RNF05 - fallback).

Conteudos de APC: strings (montar prompt), condicionais,
tratamento de excecoes (try/except), modulos (requests, os).

OBSERVACAO: para usar a IA de verdade, defina a variavel de ambiente
com a chave da API. Sem chave, o programa cai automaticamente no
fallback e continua funcionando (otimo para demonstrar offline).
"""

import os

import interface
import persistencia
import alertas as mod_alertas

# Tente importar requests; se nao estiver instalado, o fallback assume.
try:
    import requests
    TEM_REQUESTS = True
except ImportError:
    TEM_REQUESTS = False

TIMEOUT_SEGUNDOS = 10


def selecionar_ingredientes(inventario, base):
    """
    Etapa 1: escolhe os ingredientes prioritarios (os que vencem antes).
    Usa itens com <= 3 dias; se nao houver, amplia para <= 7 dias.
    Devolve uma lista de nomes de alimentos.
    """
    urgentes = mod_alertas.calcular_alertas(inventario, dias_limite=3)
    if not urgentes:
        urgentes = mod_alertas.calcular_alertas(inventario, dias_limite=7)

    nomes = []
    for item, _dias in urgentes:
        alimento = persistencia.buscar_alimento_na_base(base, item["alimento_id"])
        nomes.append(alimento["nome"] if alimento else item["alimento_id"])
    return nomes


def montar_prompt(ingredientes, preferencias):
    """Etapa 2/3: monta o texto enviado a IA, incluindo restricoes."""
    lista = ", ".join(ingredientes)
    restricoes = []
    if preferencias.get("vegetariano"):
        restricoes.append("vegetariana")
    if preferencias.get("vegano"):
        restricoes.append("vegana")
    for alergia in preferencias.get("alergias", []):
        restricoes.append(f"sem {alergia}")
    tempo = preferencias.get("tempo_max_min", 40)

    texto_restricoes = ("Restricoes: " + ", ".join(restricoes) + "."
                        if restricoes else "")
    prompt = (
        "Voce e um chef que combate o desperdicio de alimentos. "
        f"Crie UMA receita simples usando principalmente: {lista}. "
        f"{texto_restricoes} "
        f"Tempo maximo de preparo: {tempo} minutos. "
        "Liste ingredientes e modo de preparo de forma curta."
    )
    return prompt


def consultar_ia(prompt):
    """
    Etapa 4: chama a API da IA. Lanca excecao se nao houver chave,
    requests ou se a requisicao falhar/estourar o timeout.
    (A funcao orquestradora trata essas excecoes com o fallback.)
    """
    chave = os.environ.get("IA_API_KEY")
    if not TEM_REQUESTS or not chave:
        raise RuntimeError("IA indisponivel (sem requests ou sem chave).")

    # Exemplo generico de chamada HTTP. Cada equipe ajusta para a sua API
    # (Gemini, OpenAI, Claude...). Mantido simples de proposito.
    resposta = requests.post(
        os.environ.get("IA_API_URL", "https://api.exemplo.com/gerar"),
        headers={"Authorization": f"Bearer {chave}"},
        json={"prompt": prompt},
        timeout=TIMEOUT_SEGUNDOS,
    )
    resposta.raise_for_status()
    return resposta.json().get("texto", "").strip()


def receita_de_fallback(ingredientes, cache):
    """
    Plano B (RNF05): tenta achar uma receita no cache para esses
    ingredientes; se nao houver, monta uma receita generica simples.
    """
    chave = "+".join(sorted(i.lower() for i in ingredientes))
    if chave in cache:
        return cache[chave]

    principais = ", ".join(ingredientes) if ingredientes else "o que voce tiver"
    return (
        f"Refogado rapido de {principais}\n\n"
        "Ingredientes: os itens acima + alho, sal e azeite.\n"
        "Modo de preparo:\n"
        "1. Pique os ingredientes em pedacos pequenos.\n"
        "2. Aqueca o azeite e doure o alho.\n"
        "3. Acrescente os ingredientes e refogue por ~10 minutos.\n"
        "4. Tempere a gosto e sirva.\n"
        "(receita generica de fallback - sem internet)"
    )


def sugerir_receita(inventario, base, usuario, cache):
    """
    Orquestra todo o fluxo de receita (RF06): seleciona ingredientes,
    monta o prompt, tenta a IA, cai no fallback se preciso e exibe.
    Devolve a receita (texto) para que main.py possa salva-la se quiser.
    """
    interface.limpar_tela()
    interface.borda()
    interface.linha("RECEITA SUGERIDA")
    interface.borda()

    ingredientes = selecionar_ingredientes(inventario, base)
    if not ingredientes:
        interface.linha("Nao ha itens proximos do vencimento para a receita.")
        interface.borda()
        interface.pausar()
        return None

    prompt = montar_prompt(ingredientes, usuario.get("preferencias", {}))

    try:
        receita = consultar_ia(prompt)
        cache["+".join(sorted(i.lower() for i in ingredientes))] = receita
    except Exception:
        # Qualquer falha (sem chave, timeout, erro de rede) -> fallback.
        receita = receita_de_fallback(ingredientes, cache)

    interface.linha(f"Usando: {', '.join(ingredientes)}")
    interface.borda()
    print()
    print(receita)
    print()
    interface.pausar()
    return receita
