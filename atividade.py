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

    carrinho = [
        {
            "nome": "Calabresa",
            "tamanho": "M",
            "quantidade": 1,
            "preco": 32
        },
        {
            "nome": "Pepperoni",
            "tamanho": "G",
            "quantidade": 2,
            "preco": 42
        }
    ]

    estado = {
        "pizza": None,
        "tamanho": None
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

    lista_carrinho = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=False
    )

    subtotal_carrinho = ft.Text(
        "Subtotal: R$ 0.00",
        size=22,
        weight=ft.FontWeight.BOLD
    )

    def atualizar_carrinho(e=None):
        lista_carrinho.controls.clear()
        subtotal = 0

        for item in carrinho:
            parcial = item["quantidade"] * item["preco"]
            subtotal += parcial

            lista_carrinho.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(
                                item["nome"],
                                size=22,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                f"Tamanho: {item['tamanho']}"
                            ),
                            ft.Text(
                                f"Quantidade: {item['quantidade']}"
                            ),
                            ft.Text(
                                f"Preço: R$ {item['preco']:.2f}"
                            ),
                            ft.Text(
                                f"Parcial: R$ {parcial:.2f}",
                                size=18,
                                weight=ft.FontWeight.BOLD
                            )
                        ]),
                        padding=15
                    )
                )
            )

        subtotal_carrinho.value = f"Subtotal: R$ {subtotal:.2f}"
        page.update()

    def buscar_pizza(nome):
        for pizza in pizzas:
            if pizza["sabor"] == nome:
                return pizza
        return None

    def selecionar_pizza(pizza, status):
        estado["pizza"] = pizza["sabor"]

        for item in carrinho:
            if item["nome"] == pizza["sabor"]:
                status.value = "✓ Já selecionada"
                mensagem.value = f"{pizza['sabor']} já está no pedido."
                page.update()
                return

        carrinho.append({
            "nome": pizza["sabor"],
            "tamanho": "M",
            "quantidade": 1,
            "preco": pizza["preços"]["M"]
        })

        estado["tamanho"] = "M"

        status.value = "✓ Selecionada"
        mensagem.value = f"{pizza['sabor']} adicionada ao pedido."

        atualizar_carrinho()

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
                ),
                ft.Button(
                    content="Ver Carrinho",
                    on_click=mostrar_carrinho
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
                    content="Carrinho",
                    on_click=mostrar_carrinho
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

    def calcular(e=None):

        if not carrinho:
            mensagem.value = "Selecione pelo menos uma pizza."
            resultado.value = ""
            page.update()
            return

        subtotal = 0
        detalhes = []

        for item in carrinho:
            nome = item["nome"]
            quantidade = item["quantidade"]
            tamanho = item["tamanho"]
            preco = item["preco"]

            if not isinstance(quantidade, int):
                mensagem.value = f"Quantidade inválida para {nome}."
                resultado.value = ""
                page.update()
                return

            if quantidade < 1 or quantidade > 10:
                mensagem.value = (
                    f"A quantidade da {nome} "
                    "deve estar entre 1 e 10."
                )
                resultado.value = ""
                page.update()
                return

            if tamanho not in ("M", "G"):
                mensagem.value = (
                    f"Escolha o tamanho da {nome}."
                )
                resultado.value = ""
                page.update()
                return

            total_pizza = quantidade * preco

            subtotal += total_pizza

            detalhes.append(
                f"{nome} - "
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

        atualizar_carrinho()

    def mostrar_selecao(e=None):

        lista_selecao = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        if not carrinho:
            lista_selecao.controls.append(
                ft.Text(
                    "Nenhuma pizza selecionada.",
                    size=22,
                    weight=ft.FontWeight.BOLD
                )
            )

        for item in carrinho:

            pizza = buscar_pizza(item["nome"])

            quantidade = ft.TextField(
                label="Quantidade",
                value=str(item["quantidade"]),
                width=150,
                keyboard_type=ft.KeyboardType.NUMBER
            )

            tamanho = ft.RadioGroup(
                value=item["tamanho"],
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

            def alterar_quantidade(e, item=item):
                valor = e.control.value.strip()

                if valor == "":
                    return

                if valor.isdigit():
                    item["quantidade"] = int(valor)
                    atualizar_carrinho()

            def alterar_tamanho(e, item=item, pizza=pizza):
                item["tamanho"] = e.control.value
                item["preco"] = pizza["preços"][e.control.value]
                estado["tamanho"] = e.control.value
                atualizar_carrinho()

            quantidade.on_change = alterar_quantidade
            tamanho.on_change = alterar_tamanho

            lista_selecao.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(
                                f"✓ {item['nome']}",
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

        atualizar_carrinho()

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
                    content="Carrinho",
                    on_click=mostrar_carrinho
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

    def mostrar_carrinho(e=None):
        atualizar_carrinho()

        area_central.content = ft.Column([
            ft.Text(
                "Carrinho",
                size=30,
                weight=ft.FontWeight.BOLD
            ),
            lista_carrinho,
            subtotal_carrinho,
            mensagem,
            ft.Row([
                ft.Button(
                    content="Voltar",
                    on_click=mostrar_cardapio
                ),
                ft.Button(
                    content="Atualizar Carrinho",
                    on_click=atualizar_carrinho
                ),
                ft.Button(
                    content="Calcular Pedido",
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

    atualizar_carrinho()
    mostrar_inicio()


ft.run(main)