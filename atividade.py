import flet as ft


pizzas = [
    {
        "sabor": "Calabresa",
        "Descricao": "Calabresa, cebola e azeitona",
        "preços": {
            "M": 32,
            "G": 42
        }
    },
    {
        "sabor": "Cebola",
        "Descricao": "Cebola roxa, cebola verde e cebola vermelha",
        "preços": {
            "M": 32,
            "G": 42
        }
    },
    {
        "sabor": "Muçarela",
        "Descricao": "Muçarela, alho frito e azeitona",
        "preços": {
            "M": 32,
            "G": 42
        }
    },
    {
        "sabor": "Pepperoni",
        "Descricao": "Pepperoni, cebola e azeitona",
        "preços": {
            "M": 32,
            "G": 42
        }
    }
]


def criar_cartao(pizza, selecionar):
    status = ft.Text(
        "",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text(
                    pizza["sabor"],
                    size=25,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Text(pizza["Descricao"]),
                ft.Text(
                    f"M: R$ {pizza['preços']['M']:.2f}"
                ),
                ft.Text(
                    f"G: R$ {pizza['preços']['G']:.2f}"
                ),
                status,
                ft.Button(
                    content="Selecionar",
                    on_click=lambda e: selecionar(pizza, status)
                )
            ]),
            padding=20
        )
    )


def main(page: ft.Page):

    page.title = "PizzaDev"
    page.padding = 20
    page.window.maximized = True

    titulo = ft.Text(
        "PizzaDev",
        size=40,
        weight=ft.FontWeight.BOLD
    )

    estado = {
        "pizza": None,
        "tamanho": None,
        "pedidos": []
    }

    mensagem = ft.Text(
        "",
        size=20,
        weight=ft.FontWeight.BOLD
    )

    resultado = ft.Text(
        "",
        size=25,
        weight=ft.FontWeight.BOLD
    )

    lista_pizzas = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    def selecionar_pizza(pizza, status):
        estado["pizza"] = pizza["sabor"]

        for pedido in estado["pedidos"]:
            if pedido["pizza"]["sabor"] == pizza["sabor"]:
                status.value = "✓ Já selecionada"
                mensagem.value = f"{pizza['sabor']} já está no pedido."
                page.update()
                return

        estado["pedidos"].append({
            "pizza": pizza,
            "quantidade": 1,
            "tamanho": "M"
        })

        estado["tamanho"] = "M"

        status.value = "✓ Selecionada"
        mensagem.value = f"{pizza['sabor']} adicionada ao pedido."

        page.update()

    for pizza in pizzas:
        lista_pizzas.controls.append(
            criar_cartao(
                pizza,
                selecionar_pizza
            )
        )

    def mostrar_inicio(e=None):
        area_central.content = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Bem-vindo ao PizzaDev!",
                    size=30,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Text(
                    "Monte seu pedido de forma simples e rápida.",
                    size=18
                ),
                ft.Button(
                    content="Ver Cardápio",
                    on_click=mostrar_cardapio
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
            ),
            alignment=ft.Alignment(0, 0),
            expand=True
        )

        page.update()

    def mostrar_cardapio(e=None):
        area_central.content = ft.Column([
            ft.Text(
                "Cardápio",
                size=30,
                weight=ft.FontWeight.BOLD
            ),
            ft.Text(
                "Escolha uma ou mais pizzas:",
                size=18
            ),
            lista_pizzas,
            ft.Row([
                ft.Button(
                    content="Voltar",
                    on_click=mostrar_inicio
                ),
                ft.Button(
                    content="Avançar",
                    on_click=mostrar_selecao
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        ],
        expand=True)

        page.update()

    def calcular(e):

        if not estado["pedidos"]:
            mensagem.value = "Selecione pelo menos uma pizza."
            resultado.value = ""
            page.update()
            return

        subtotal = 0
        detalhes = []

        for pedido in estado["pedidos"]:

            pizza = pedido["pizza"]
            quantidade = pedido["quantidade"]
            tamanho = pedido["tamanho"]

            if not isinstance(quantidade, int):
                mensagem.value = f"Quantidade inválida para {pizza['sabor']}."
                resultado.value = ""
                page.update()
                return

            if quantidade < 1 or quantidade > 10:
                mensagem.value = (
                    f"A quantidade da {pizza['sabor']} "
                    "deve estar entre 1 e 10."
                )
                resultado.value = ""
                page.update()
                return

            if tamanho not in ("M", "G"):
                mensagem.value = (
                    f"Escolha o tamanho da {pizza['sabor']}."
                )
                resultado.value = ""
                page.update()
                return

            preco = pizza["preços"][tamanho]
            total_pizza = quantidade * preco

            subtotal += total_pizza

            detalhes.append(
                f"{pizza['sabor']} - "
                f"{quantidade}x {tamanho} - "
                f"R$ {total_pizza:.2f}"
            )

        if subtotal >= 100:
            desconto = subtotal * 0.05
            frete = 0
        else:
            desconto = 0
            frete = 10

        total = subtotal - desconto + frete

        mensagem.value = "Pedido calculado!"

        resultado.value = (
            "\n".join(detalhes)
            + "\n\n"
            + f"Subtotal: R$ {subtotal:.2f}\n"
            + f"Desconto: R$ {desconto:.2f}\n"
            + f"Frete: R$ {frete:.2f}\n"
            + f"Total: R$ {total:.2f}"
        )

        page.update()

    def mostrar_selecao(e=None):

        lista_selecao = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        if not estado["pedidos"]:
            lista_selecao.controls.append(
                ft.Text(
                    "Nenhuma pizza selecionada.",
                    size=22,
                    weight=ft.FontWeight.BOLD
                )
            )

        for pedido in estado["pedidos"]:

            pizza = pedido["pizza"]

            quantidade = ft.TextField(
                label="Quantidade",
                value=str(pedido["quantidade"]),
                width=150,
                keyboard_type=ft.KeyboardType.NUMBER
            )

            tamanho = ft.RadioGroup(
                value=pedido["tamanho"],
                content=ft.Row([
                    ft.Radio(
                        value="M",
                        label=f"M - R$ {pizza['preços']['M']:.2f}"
                    ),
                    ft.Radio(
                        value="G",
                        label=f"G - R$ {pizza['preços']['G']:.2f}"
                    )
                ])
            )

            def alterar_quantidade(e, pedido=pedido):
                valor = e.control.value.strip()

                if valor == "":
                    return

                if valor.isdigit():
                    pedido["quantidade"] = int(valor)

            def alterar_tamanho(e, pedido=pedido):
                pedido["tamanho"] = e.control.value
                estado["tamanho"] = e.control.value

            quantidade.on_change = alterar_quantidade
            tamanho.on_change = alterar_tamanho

            lista_selecao.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(
                                f"✓ {pizza['sabor']}",
                                size=24,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                pizza["Descricao"]
                            ),
                            quantidade,
                            tamanho
                        ]),
                        padding=20
                    )
                )
            )

        if estado["pizza"] is not None:
            pizza_guardada = ft.Text(
                f"Pizza guardada: {estado['pizza']}",
                size=18,
                weight=ft.FontWeight.BOLD
            )
        else:
            pizza_guardada = ft.Text(
                "Nenhuma pizza guardada.",
                size=18
            )

        area_central.content = ft.Column([
            ft.Text(
                "Seleção",
                size=30,
                weight=ft.FontWeight.BOLD
            ),
            pizza_guardada,
            lista_selecao,
            mensagem,
            resultado,
            ft.Row([
                ft.Button(
                    content="Voltar",
                    on_click=mostrar_cardapio
                ),
                ft.Button(
                    content="Calcular",
                    on_click=calcular
                ),
                ft.Button(
                    content="Início",
                    on_click=mostrar_inicio
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        ],
        expand=True)

        page.update()

    area_central = ft.Container(
        expand=True,
        border_radius=10,
        padding=20
    )

    page.add(
        titulo,
        area_central
    )

    mostrar_inicio()


ft.run(main)