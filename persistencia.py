"""
persistencia.py
---------------
Camada de leitura/escrita de dados do Geladeira Zero.

Responsabilidade: ler e gravar os arquivos JSON (base de alimentos,
inventario, historico e usuario) e exportar o historico para CSV.

Conteudos de APC: manipulacao de arquivos, dicionarios, listas,
tratamento de excecoes, modulos (json, csv, os).
"""

import json
import csv
import os

# Pasta onde ficam todos os arquivos de dados (relativa a ESTE arquivo,
# para o programa achar os dados rodando de qualquer lugar).
PASTA_DADOS = os.path.join(os.path.dirname(__file__), "data")


def garantir_pasta_dados():
    """Cria a pasta data/ caso ainda nao exista (evita erro na 1a execucao)."""
    if not os.path.exists(PASTA_DADOS):
        os.makedirs(PASTA_DADOS)


def caminho(nome_arquivo):
    """Monta o caminho completo de um arquivo dentro da pasta data/."""
    return os.path.join(PASTA_DADOS, nome_arquivo)


def carregar_json(nome_arquivo, padrao):
    """
    Le um arquivo JSON e devolve seu conteudo.

    Se o arquivo nao existir ou estiver corrompido, devolve 'padrao'
    (uma lista ou dicionario vazio) em vez de quebrar o programa.
    """
    garantir_pasta_dados()
    caminho_completo = caminho(nome_arquivo)
    try:
        with open(caminho_completo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        # Primeira execucao: ainda nao existe esse arquivo.
        return padrao
    except json.JSONDecodeError:
        # Arquivo existe mas esta corrompido: avisa e usa o padrao.
        print(f"[aviso] {nome_arquivo} esta corrompido. Usando dados vazios.")
        return padrao


def salvar_json(nome_arquivo, dados):
    """Grava 'dados' (lista ou dicionario) em um arquivo JSON legivel."""
    garantir_pasta_dados()
    caminho_completo = caminho(nome_arquivo)
    with open(caminho_completo, "w", encoding="utf-8") as arquivo:
        # indent=2 deixa o arquivo legivel; ensure_ascii=False mantem acentos.
        json.dump(dados, arquivo, indent=2, ensure_ascii=False)


def exportar_csv(historico, base, nome_arquivo="historico.csv"):
    """
    Exporta o historico de itens consumidos/descartados para CSV (RF11).
    Cada linha = um item, com nome, categoria, status, quantidade e datas.
    """
    garantir_pasta_dados()
    caminho_completo = caminho(nome_arquivo)
    colunas = ["alimento", "categoria", "status", "quantidade",
               "unidade", "data_compra", "data_validade"]

    with open(caminho_completo, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        for item in historico:
            alimento = buscar_alimento_na_base(base, item["alimento_id"])
            escritor.writerow({
                "alimento": alimento["nome"] if alimento else item["alimento_id"],
                "categoria": alimento["categoria"] if alimento else "?",
                "status": item["status"],
                "quantidade": item["quantidade"],
                "unidade": item["unidade"],
                "data_compra": item["data_compra"],
                "data_validade": item["data_validade"],
            })
    return caminho_completo


def buscar_alimento_na_base(base, alimento_id):
    """Busca rapida de um alimento pelo id dentro da base. Devolve None se nao achar."""
    for alimento in base:
        if alimento["id"] == alimento_id:
            return alimento
    return None
