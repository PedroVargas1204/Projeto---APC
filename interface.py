"""
interface.py
------------
Camada de interface em modo texto (CLI) do Geladeira Zero.

Responsabilidade: desenhar as telas, exibir o menu e validar TODA
entrada do usuario (datas, numeros, opcoes) para nao quebrar o programa.

Conteudos de APC: strings, condicionais, lacos while, funcoes.
"""

import os
from datetime import datetime


def limpar_tela():
    """Limpa o terminal (funciona em Windows, Linux e Mac)."""
    os.system("cls" if os.name == "nt" else "clear")


def linha(texto=""):
    """Imprime uma linha dentro da 'moldura' de 62 colunas das telas."""
    print(f"| {texto:<60} |")


def borda():
    """Imprime a borda horizontal das telas."""
    print("+" + "-" * 62 + "+")


def exibir_cabecalho(usuario, total_itens, qtd_alertas, impacto):
    """Cabecalho com saudacao e os numeros do mes (telas principais)."""
    nome = usuario.get("nome", "Visitante")
    salvo = impacto.get("kg_salvo", 0.0)
    economia = impacto.get("economia", 0.0)
    borda()
    linha("GELADEIRA ZERO - Desperdicio Zero")
    borda()
    linha(f"Ola, {nome}!  Itens: {total_itens}   Vencem em 3 dias: {qtd_alertas}")
    linha(f"Salvo este mes: {salvo:.1f} kg   Economia: R$ {economia:.2f}")
    borda()


def exibir_menu():
    """Desenha o menu principal com as 8 opcoes + sair."""
    linha("")
    linha("[1] Adicionar item ao inventario")
    linha("[2] Ver inventario (ordenado por validade)")
    linha("[3] Ver alertas de vencimento")
    linha("[4] Sugerir receita com o que tenho")
    linha("[5] Marcar item como consumido / descartado")
    linha("[6] Ver impacto e economia")
    linha("[7] Configuracoes (preferencias alimentares)")
    linha("[8] Exportar historico (CSV)")
    linha("[0] Sair")
    linha("")
    borda()


def ler_opcao(minimo, maximo):
    """
    Le um numero inteiro do menu entre 'minimo' e 'maximo'.
    Repete a pergunta ate o usuario digitar algo valido (RNF03).
    """
    while True:
        entrada = input("Escolha uma opcao: ").strip()
        if entrada.isdigit() and minimo <= int(entrada) <= maximo:
            return int(entrada)
        print(f"  Opcao invalida. Digite um numero de {minimo} a {maximo}.")


def ler_texto(rotulo, obrigatorio=True):
    """Le um texto. Se obrigatorio, nao aceita vazio."""
    while True:
        valor = input(rotulo).strip()
        if valor or not obrigatorio:
            return valor
        print("  Esse campo nao pode ficar vazio.")


def ler_float(rotulo, minimo=0.0):
    """Le um numero decimal valido e maior ou igual a 'minimo'."""
    while True:
        entrada = input(rotulo).strip().replace(",", ".")
        try:
            valor = float(entrada)
            if valor >= minimo:
                return valor
            print(f"  O valor precisa ser >= {minimo}.")
        except ValueError:
            print("  Digite um numero valido (ex: 1.5).")


def ler_inteiro(rotulo, minimo=0):
    """Le um inteiro valido e maior ou igual a 'minimo'."""
    while True:
        entrada = input(rotulo).strip()
        if entrada.isdigit() and int(entrada) >= minimo:
            return int(entrada)
        print(f"  Digite um inteiro >= {minimo}.")


def ler_data(rotulo):
    """
    Le uma data no formato DD/MM/AAAA e devolve no formato AAAA-MM-DD
    (padrao usado internamente). Valida que a data realmente existe.
    """
    while True:
        entrada = input(rotulo).strip()
        try:
            data = datetime.strptime(entrada, "%d/%m/%Y")
            return data.strftime("%Y-%m-%d")
        except ValueError:
            print("  Data invalida. Use o formato DD/MM/AAAA (ex: 20/06/2026).")


def ler_sim_nao(rotulo):
    """Le uma resposta S/N e devolve True para sim, False para nao."""
    while True:
        resposta = input(rotulo).strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("  Responda com S ou N.")


def pausar():
    """Pausa a tela ate o usuario apertar Enter."""
    input("\n[Enter] para voltar ao menu...")
