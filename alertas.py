"""
alertas.py
----------
Logica de alertas de vencimento: descobre quais itens vencem nos
proximos dias e os ordena por urgencia (RF05).

Separacao: calcular_alertas() e logica pura (sem tela); exibir_alertas()
e a tela.

Conteudos de APC: datetime, condicionais, lacos for, tuplas, listas.
"""

from datetime import datetime

import config
import interface
import persistencia


def dias_ate_vencer(item):
    """Quantos dias faltam ate o item vencer (negativo = ja venceu)."""
    validade = datetime.strptime(item["data_validade"], "%Y-%m-%d")
    return (validade - datetime.now()).days


def calcular_alertas(inventario, dias_limite=config.DIAS_ALERTA):
    """
    Devolve uma lista de tuplas (item, dias_restantes) para itens ativos
    que vencem dentro do limite, ordenada do mais urgente para o menos.
    """
    alertas = []
    for item in inventario:
        if item["status"] != "ativo":
            continue
        dias = dias_ate_vencer(item)
        if dias <= dias_limite:
            alertas.append((item, dias))
    # Ordena pela quantidade de dias restantes (crescente = mais urgente 1o).
    alertas.sort(key=lambda par: par[1])
    return alertas


def exibir_alertas(inventario, base):
    """Mostra a tela de alertas de vencimento (RF05)."""
    interface.limpar_tela()
    interface.borda()
    interface.linha("ALERTAS DE VENCIMENTO")
    interface.borda()

    alertas = calcular_alertas(inventario)
    if not alertas:
        interface.linha("Nenhum item vence nos proximos dias. Tudo certo!")
        interface.borda()
        interface.pausar()
        return

    interface.linha(f"{len(alertas)} item(ns) precisam de atencao:")
    interface.linha("")
    for item, dias in alertas:
        alimento = persistencia.buscar_alimento_na_base(base, item["alimento_id"])
        nome = alimento["nome"] if alimento else item["alimento_id"]
        if dias < 0:
            quando = "JA VENCEU"
        elif dias == 0:
            quando = "vence hoje"
        else:
            quando = f"vence em {dias} dia(s)"
        interface.linha(f"- {nome} ({item['quantidade']:g} {item['unidade']}) {quando}")
    interface.borda()
    interface.pausar()
