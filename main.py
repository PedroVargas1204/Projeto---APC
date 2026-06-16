"""
main.py
-------
Ponto de entrada do Geladeira Zero. Carrega os dados, mostra o menu
e chama a funcao certa para cada opcao (RF01).

Conteudos de APC: laco while (menu), condicionais (if/elif),
funcoes, modulos (importa todos os outros arquivos do projeto).

Para rodar:  python main.py
"""

import persistencia
import interface
import inventario as mod_inventario
import alertas as mod_alertas
import ia as mod_ia
import impacto as mod_impacto


def carregar_tudo():
    """Carrega base, inventario, historico, usuario e cache do disco."""
    base = persistencia.carregar_json("base_alimentos.json", [])
    inventario = persistencia.carregar_json("inventario.json", [])
    historico = persistencia.carregar_json("historico.json", [])
    usuario = persistencia.carregar_json("usuario.json", {
        "nome": "Visitante",
        "preferencias": {"vegetariano": False, "vegano": False,
                         "alergias": [], "tempo_max_min": 40},
    })
    cache = persistencia.carregar_json("receitas_cache.json", {})
    return base, inventario, historico, usuario, cache


def salvar_tudo(inventario, historico, usuario, cache):
    """Persiste tudo que pode ter mudado durante o uso (RNF04)."""
    persistencia.salvar_json("inventario.json", inventario)
    persistencia.salvar_json("historico.json", historico)
    persistencia.salvar_json("usuario.json", usuario)
    persistencia.salvar_json("receitas_cache.json", cache)


def configuracoes(usuario):
    """Tela de preferencias alimentares (RF10)."""
    interface.limpar_tela()
    interface.borda()
    interface.linha("CONFIGURACOES (preferencias)")
    interface.borda()
    prefs = usuario.setdefault("preferencias", {})

    usuario["nome"] = interface.ler_texto(
        f"Seu nome [{usuario.get('nome', 'Visitante')}]: ", obrigatorio=False
    ) or usuario.get("nome", "Visitante")
    prefs["vegetariano"] = interface.ler_sim_nao("Vegetariano? [S/N]: ")
    prefs["vegano"] = interface.ler_sim_nao("Vegano? [S/N]: ")
    alergias = interface.ler_texto(
        "Alergias (separadas por virgula, ou vazio): ", obrigatorio=False
    )
    prefs["alergias"] = [a.strip() for a in alergias.split(",") if a.strip()]
    prefs["tempo_max_min"] = interface.ler_inteiro(
        "Tempo maximo de preparo (min): ", minimo=5
    )
    print("\n  Preferencias salvas!")
    interface.pausar()


def exportar(historico, base):
    """Exporta o historico para CSV (RF11)."""
    caminho = persistencia.exportar_csv(historico, base)
    print(f"\n  Historico exportado para: {caminho}")
    interface.pausar()


def main():
    """Funcao principal: carrega dados e roda o loop do menu."""
    base, inventario, historico, usuario, cache = carregar_tudo()

    # Verifica alertas logo na entrada (item de UX da especificacao).
    sair = False
    while not sair:
        interface.limpar_tela()
        impacto = mod_impacto.resumo_impacto(historico, base)
        qtd_alertas = len(mod_alertas.calcular_alertas(inventario))
        ativos = len([i for i in inventario if i["status"] == "ativo"])

        interface.exibir_cabecalho(usuario, ativos, qtd_alertas, impacto)
        interface.exibir_menu()
        opcao = interface.ler_opcao(0, 8)

        if opcao == 1:
            mod_inventario.adicionar_item(inventario, base)
        elif opcao == 2:
            mod_inventario.listar_inventario(inventario, base)
        elif opcao == 3:
            mod_alertas.exibir_alertas(inventario, base)
        elif opcao == 4:
            mod_ia.sugerir_receita(inventario, base, usuario, cache)
        elif opcao == 5:
            mod_inventario.marcar_consumido_ou_descartado(inventario, historico)
        elif opcao == 6:
            mod_impacto.exibir_impacto(historico, base)
        elif opcao == 7:
            configuracoes(usuario)
        elif opcao == 8:
            exportar(historico, base)
        elif opcao == 0:
            sair = True

        # Salva a cada acao para nao perder dados (RNF04).
        salvar_tudo(inventario, historico, usuario, cache)

    print("\nAte logo! Dados salvos. Desperdicio zero!")


if __name__ == "__main__":
    main()
