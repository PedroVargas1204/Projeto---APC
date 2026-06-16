"""
impacto.py
----------
Calculo de impacto ambiental e economico (RF08 + RF09).

A partir do historico de itens CONSUMIDOS (aproveitados no prazo),
soma kg de alimento salvo, CO2 evitado, agua economizada e dinheiro
poupado. Tambem agrega por categoria para os graficos.

Conteudos de APC: lacos for, floats, tuplas (retorno multiplo),
dicionarios, condicionais.
"""

from datetime import datetime

import interface
import persistencia


def converter_para_kg(quantidade, unidade):
    """
    Converte a quantidade para kg, para uniformizar o calculo.
    'unid' e tratado como ~0.15 kg (valor medio simples por unidade).
    """
    unidade = unidade.lower()
    if unidade == "kg":
        return quantidade
    if unidade == "g":
        return quantidade / 1000.0
    if unidade in ("l", "litro", "litros"):
        return quantidade  # aproxima 1 L ~ 1 kg
    if unidade in ("unid", "un", "unidade", "unidades"):
        return quantidade * 0.15
    return quantidade  # fallback: assume que ja esta em kg


def calcular_impacto(historico, base, periodo_dias=30):
    """
    Soma o impacto dos itens CONSUMIDOS no periodo. Considera 'salvo'
    o alimento que foi aproveitado (consumido) em vez de descartado.
    Devolve uma tupla: (kg_salvo, co2_evitado, agua_economizada, economia).
    """
    kg_salvo = 0.0
    co2_evitado = 0.0
    agua_economizada = 0.0
    economia = 0.0

    hoje = datetime.now()
    for item in historico:
        if item["status"] != "consumido":
            continue
        # Filtra pelo periodo (usa a data de compra como referencia).
        compra = datetime.strptime(item["data_compra"], "%Y-%m-%d")
        if (hoje - compra).days > periodo_dias:
            continue

        alimento = persistencia.buscar_alimento_na_base(base, item["alimento_id"])
        if alimento is None:
            continue

        qtd_kg = converter_para_kg(item["quantidade"], item["unidade"])
        kg_salvo += qtd_kg
        co2_evitado += qtd_kg * alimento.get("co2_kg_por_kg", 0.0)
        agua_economizada += qtd_kg * alimento.get("agua_l_por_kg", 0.0)
        economia += qtd_kg * alimento.get("preco_medio_kg", 0.0)

    return (kg_salvo, co2_evitado, agua_economizada, economia)


def resumo_impacto(historico, base, periodo_dias=30):
    """Devolve o impacto como dicionario, pratico para o cabecalho/telas."""
    kg, co2, agua, economia = calcular_impacto(historico, base, periodo_dias)
    return {
        "kg_salvo": kg,
        "co2_evitado": co2,
        "agua_economizada": agua,
        "economia": economia,
    }


def agregar_por_categoria(historico, base):
    """
    Conta quantos itens consumidos por categoria (para o grafico de
    'categorias mais salvas'). Devolve dicionario {categoria: contagem}.
    """
    contagem = {}
    for item in historico:
        if item["status"] != "consumido":
            continue
        alimento = persistencia.buscar_alimento_na_base(base, item["alimento_id"])
        categoria = alimento["categoria"] if alimento else "Outros"
        contagem[categoria] = contagem.get(categoria, 0) + 1
    return contagem


def exibir_impacto(historico, base):
    """Tela 'Meu impacto e economia' (RF08 + RF09)."""
    interface.limpar_tela()
    interface.borda()
    interface.linha("MEU IMPACTO E ECONOMIA (ultimos 30 dias)")
    interface.borda()

    consumidos = [i for i in historico if i["status"] == "consumido"]
    descartados = [i for i in historico if i["status"] == "descartado"]
    total = len(consumidos) + len(descartados)
    taxa = (len(consumidos) / total * 100) if total else 0.0

    kg, co2, agua, economia = calcular_impacto(historico, base)

    interface.linha(f"Itens aproveitados: {len(consumidos)}")
    interface.linha(f"Itens descartados: {len(descartados)}")
    interface.linha(f"Taxa de aproveitamento: {taxa:.0f}%")
    interface.linha("")
    interface.linha(f"Alimento salvo: {kg:.1f} kg")
    interface.linha(f"CO2 evitado: {co2:.1f} kg")
    interface.linha(f"Agua economizada: {agua:.0f} L")
    interface.linha(f"Dinheiro economizado: R$ {economia:.2f}")
    interface.linha("")

    categorias = agregar_por_categoria(historico, base)
    if categorias:
        interface.linha("Categorias mais salvas:")
        for categoria, qtd in sorted(categorias.items(),
                                     key=lambda par: par[1], reverse=True):
            barra = "#" * qtd
            interface.linha(f"  {categoria:<16} {barra} {qtd}")
    interface.borda()
    interface.pausar()
