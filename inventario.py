"""
inventario.py
-------------
Gestao do inventario: cadastrar itens, listar por validade, buscar
alimentos na base (com tolerancia a sinonimos) e sugerir validade.

Separacao: as funcoes de LOGICA (buscar_alimento_por_nome, sugerir_validade,
proximo_id) nao usam print/input e podem ser reaproveitadas em qualquer
interface. As funcoes de TELA (adicionar_item, listar_inventario,
marcar_consumido_ou_descartado) e que conversam com o usuario.

Conteudos de APC: listas, dicionarios, condicionais, lacos for,
strings (normalizacao), funcoes.
"""

from datetime import datetime, timedelta

import interface
import persistencia


# ---------------------------------------------------------------------------
# LOGICA (sem tela) — reaproveitavel por qualquer interface
# ---------------------------------------------------------------------------

def normalizar(texto):
    """Coloca em minusculas e tira espacos das pontas, para comparar nomes."""
    return texto.strip().lower()


def buscar_alimento_por_nome(base, nome):
    """
    Procura um alimento na base pelo nome OU por um de seus sinonimos.
    Tolerante: ignora maiusculas/minusculas e espacos. Devolve None se nao achar.
    """
    alvo = normalizar(nome)
    for alimento in base:
        nomes_possiveis = [normalizar(alimento["nome"])]
        for sinonimo in alimento.get("sinonimos", []):
            nomes_possiveis.append(normalizar(sinonimo))
        if alvo in nomes_possiveis:
            return alimento
    # Segunda tentativa: nome contido (ex.: "tomate italiano" -> "tomate").
    for alimento in base:
        if normalizar(alimento["nome"]) in alvo:
            return alimento
    return None


def sugerir_validade(alimento, local, data_compra):
    """
    Sugere a data de validade a partir da base, somando os dias tipicos
    do local de armazenamento a data de compra (RF03).
    Devolve a data no formato AAAA-MM-DD.
    """
    dias = alimento["validade_dias"].get(local)
    if dias is None:
        # Local nao recomendado para esse alimento: usa geladeira como padrao.
        dias = alimento["validade_dias"].get("geladeira") or 7
    base_data = datetime.strptime(data_compra, "%Y-%m-%d")
    validade = base_data + timedelta(days=dias)
    return validade.strftime("%Y-%m-%d")


def proximo_id(inventario):
    """Gera o proximo id numerico do inventario (1, 2, 3, ...)."""
    if not inventario:
        return 1
    return max(item["id"] for item in inventario) + 1


# ---------------------------------------------------------------------------
# TELA (conversa com o usuario)
# ---------------------------------------------------------------------------

def adicionar_item(inventario, base):
    """
    Tela de cadastro de um novo item no inventario (RF02 + RF03).
    Pergunta nome, quantidade, unidade, local, data de compra e
    sugere a validade automaticamente (com opcao de ajustar).
    """
    interface.limpar_tela()
    interface.borda()
    interface.linha("ADICIONAR ITEM AO INVENTARIO")
    interface.borda()
    print()

    nome = interface.ler_texto("Nome do alimento: ")
    alimento = buscar_alimento_por_nome(base, nome)

    if alimento is None:
        print(f"  '{nome}' nao esta na base. Cadastrando como item generico.")
        # Item generico: validade padrao de 7 dias, sem dados de impacto.
        alimento = {
            "id": normalizar(nome).replace(" ", "_"),
            "nome": nome.title(),
            "categoria": "Outros",
            "validade_dias": {"geladeira": 7, "ambiente": 5, "congelado": 30},
            "preco_medio_kg": 0.0, "co2_kg_por_kg": 0.0, "agua_l_por_kg": 0.0,
        }
    else:
        print(f"  Encontrado na base: {alimento['nome']} ({alimento['categoria']}).")

    quantidade = interface.ler_float("Quantidade: ", minimo=0.01)
    print("  Unidades: kg | g | L | unid")
    unidade = interface.ler_texto("Unidade: ").lower()
    print("  Locais: geladeira | ambiente | congelado")
    local = interface.ler_texto("Local de armazenamento: ").lower()
    if local not in ("geladeira", "ambiente", "congelado"):
        local = "geladeira"

    data_compra = interface.ler_data("Data de compra (DD/MM/AAAA): ")
    sugestao = sugerir_validade(alimento, local, data_compra)
    sugestao_br = datetime.strptime(sugestao, "%Y-%m-%d").strftime("%d/%m/%Y")
    print(f"  Validade estimada: {sugestao_br}")

    if interface.ler_sim_nao("Aceitar essa validade? [S/N]: "):
        data_validade = sugestao
    else:
        data_validade = interface.ler_data("Informe a validade (DD/MM/AAAA): ")

    novo = {
        "id": proximo_id(inventario),
        "alimento_id": alimento["id"],
        "quantidade": quantidade,
        "unidade": unidade,
        "data_compra": data_compra,
        "data_validade": data_validade,
        "local": local,
        "status": "ativo",
    }
    inventario.append(novo)
    print(f"\n  '{alimento['nome']}' adicionado com sucesso!")
    interface.pausar()


def listar_inventario(inventario, base):
    """
    Mostra o inventario ativo ordenado pela proximidade do vencimento (RF04).
    """
    interface.limpar_tela()
    interface.borda()
    interface.linha("INVENTARIO (ordenado por validade)")
    interface.borda()

    ativos = [item for item in inventario if item["status"] == "ativo"]
    if not ativos:
        interface.linha("Seu inventario esta vazio.")
        interface.borda()
        interface.pausar()
        return

    # Ordena a lista pela data de validade (mais proximo primeiro).
    ativos.sort(key=lambda item: item["data_validade"])

    hoje = datetime.now()
    for item in ativos:
        alimento = persistencia.buscar_alimento_na_base(base, item["alimento_id"])
        nome = alimento["nome"] if alimento else item["alimento_id"]
        validade = datetime.strptime(item["data_validade"], "%Y-%m-%d")
        dias = (validade - hoje).days
        if dias < 0:
            situacao = "VENCIDO"
        elif dias == 0:
            situacao = "vence hoje"
        else:
            situacao = f"vence em {dias} dia(s)"
        texto = f"{nome} ({item['quantidade']:g} {item['unidade']}) - {situacao}"
        interface.linha(texto)

    interface.borda()
    interface.pausar()


def marcar_consumido_ou_descartado(inventario, historico):
    """
    Move um item do inventario para o historico, marcando-o como
    'consumido' ou 'descartado' (RF07). Esse historico alimenta o
    calculo de impacto.
    """
    interface.limpar_tela()
    interface.borda()
    interface.linha("MARCAR ITEM (consumido / descartado)")
    interface.borda()

    ativos = [item for item in inventario if item["status"] == "ativo"]
    if not ativos:
        interface.linha("Nao ha itens ativos.")
        interface.borda()
        interface.pausar()
        return

    for indice, item in enumerate(ativos, start=1):
        print(f"  [{indice}] {item['alimento_id']} "
              f"({item['quantidade']:g} {item['unidade']})")

    escolha = interface.ler_inteiro("\nNumero do item (0 cancela): ", minimo=0)
    if escolha == 0 or escolha > len(ativos):
        return
    item = ativos[escolha - 1]

    print("  [1] Consumido (aproveitado)   [2] Descartado (estragou)")
    tipo = interface.ler_inteiro("Status: ", minimo=1)
    item["status"] = "consumido" if tipo == 1 else "descartado"

    # Tira do inventario ativo e guarda no historico.
    inventario.remove(item)
    historico.append(item)
    print(f"\n  Item marcado como '{item['status']}'.")
    interface.pausar()
