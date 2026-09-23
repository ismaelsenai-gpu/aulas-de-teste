import flet as ft


def main(page: ft.Page):
    page.title = "PizzaDev"

    
    titulo = ft.Text(
        "PizzaDev",
        size=40,
        weight=ft.FontWeight.BOLD
    )

    slogan = ft.Text(
        "Mais pizza e menos guerra!",
        size=32,
        weight=ft.FontWeight.BOLD
    )

    orientacao = ft.Text("Para pedir, peça!")

    dupla = ft.Text("Dupla é SAMUEL")

    dados = ft.Text(
        "Dados temporários durante execução",
        size=30
    )

    
    mensagem = ft.Text(
        "Nenhuma pizza selecionada.",
        size=25,
        weight=ft.FontWeight.BOLD
    )

    

    def selecionar_pizza(nome, preco_m):

        def selecionar(e):
            mensagem.value = f"Selecionada: {nome} | Preço M: R$ {preco_m:.2f}"
            page.update()

        return selecionar

    

    def criar_card(nome, descricao, preco_p, preco_m):

        botao = ft.Button(
            content=f"Escolher {nome}",
            on_click=selecionar_pizza(nome, preco_m)
        )

        card = ft.Container(
            padding=15,
            border_radius=12,
            content=ft.Column([
                ft.Text(
                    nome,
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(descricao),

                ft.Row([
                    ft.Text(f"P: R$ {preco_p:.2f}"),
                    ft.Text(f"M: R$ {preco_m:.2f}")
                ]),

                botao
            ])
        )

        return card

   

    def limpar_selecao(e):
        mensagem.value = "Nenhuma pizza selecionada."
        page.update()

    limpar = ft.Button(
        content="Limpar seleção",
        on_click=limpar_selecao
    )

    

    card_calabresa = criar_card(
        "Calabresa",
        "Calabresa, cebola e muçarela",
        30,
        40
    )

    card_mussarela = criar_card(
        "Muçarela",
        "Muçarela, tomate e orégano",
        28,
        38
    )

    card_frango = criar_card(
        "Frango com Catupiry",
        "Frango, catupiry e muçarela",
        35,
        45
    )

  

    page.add(
        titulo,
        slogan,
        orientacao,
        dupla,
        dados,
        mensagem,

        ft.Column(
            [
                card_calabresa,
                card_mussarela,
                card_frango,
                limpar
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )


ft.run(main)