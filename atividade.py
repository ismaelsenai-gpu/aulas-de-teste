import asyncio
import random
from math import pi
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
    page.window.width = 360
    page.window.height = 800
    page.title = "PizzaDev"
    page.padding = 15
    page.window.resizable = False
    """page.window.maximized = True"""

    tela_atual = 0

    tamanho_quadrado = 7
    espaco = 1
    duracao_animacao = 1400

    cores_letras = [
        ft.Colors.PINK_500,
        ft.Colors.AMBER_500,
        ft.Colors.LIGHT_GREEN_500,
        ft.Colors.DEEP_PURPLE_500,
        ft.Colors.BLUE_500,
        ft.Colors.DEEP_ORANGE_500,
        ft.Colors.CYAN_500,
        ft.Colors.RED_500,
    ]

    formatos_letras = [
        [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2)],
        [(0, 0), (1, 0), (2, 0), (1, 1), (1, 2), (1, 3), (0, 4), (1, 4), (2, 4)],
        [(0, 0), (1, 0), (2, 0), (2, 1), (1, 2), (0, 3), (0, 4), (1, 4), (2, 4)],
        [(0, 0), (1, 0), (2, 0), (2, 1), (1, 2), (0, 3), (0, 4), (1, 4), (2, 4)],
        [(1, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2), (0, 3), (2, 3), (0, 4), (2, 4)],
        [(0, 0), (1, 0), (0, 1), (2, 1), (0, 2), (2, 2), (0, 3), (2, 3), (0, 4), (1, 4)],
        [(0, 0), (1, 0), (2, 0), (0, 1), (0, 2), (1, 2), (2, 2), (0, 3), (0, 4), (1, 4)],
        [(0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2), (0, 3), (2, 3), (1, 4)],
    ]

    pecas_logo = [
        (indice_letra * 4 + x, y, cores_letras[indice_letra])
        for indice_letra, formato in enumerate(formatos_letras)
        for x, y in formato
    ]

    largura_logo = 31 * (tamanho_quadrado + espaco)
    altura_logo = 5 * (tamanho_quadrado + espaco)

    logo = ft.Stack(
        width=largura_logo,
        height=altura_logo,
        animate_scale=duracao_animacao,
        animate_opacity=duracao_animacao,
    )

    for _ in pecas_logo:
        logo.controls.append(
            ft.Container(
                animate=duracao_animacao,
                animate_position=duracao_animacao,
                animate_rotation=duracao_animacao,
            )
        )

    cores_sorteadas = [
        ft.Colors.AMBER_400,
        ft.Colors.BLUE_400,
        ft.Colors.BROWN_400,
        ft.Colors.CYAN_700,
        ft.Colors.DEEP_ORANGE_500,
        ft.Colors.INDIGO_600,
        ft.Colors.PINK,
        ft.Colors.RED_600,
        ft.Colors.GREEN_400,
        ft.Colors.TEAL_ACCENT_200,
        ft.Colors.LIGHT_BLUE_500,
    ]

    def espalhar_logo():
        for peca in logo.controls:
            tamanho = random.randrange(4, 15)
            peca.left = random.randrange(0, largura_logo)
            peca.top = random.randrange(0, altura_logo)
            peca.bgcolor = random.choice(cores_sorteadas)
            peca.width = tamanho
            peca.height = tamanho
            peca.border_radius = random.randrange(0, 4)
            peca.rotate = random.randrange(0, 90) * 2 * pi / 360

        logo.scale = 1.4
        logo.opacity = 0.35

    def montar_logo():
        for indice, (esquerda, topo, cor) in enumerate(pecas_logo):
            peca = logo.controls[indice]
            peca.left = esquerda * (tamanho_quadrado + espaco)
            peca.top = topo * (tamanho_quadrado + espaco)
            peca.bgcolor = cor
            peca.width = tamanho_quadrado
            peca.height = tamanho_quadrado
            peca.border_radius = 2
            peca.rotate = 0

        logo.scale = 1
        logo.opacity = 1
        page.update()

    titulo = ft.Container(
        content=logo,
        width=300,
        height=65,
        alignment=ft.Alignment(0, 0),
        visible=True,
    )

    carrinho = []

    estado = {
        "pizza": None,
        "tamanho": None,
        "entrega": None,
        "taxa_entrega": 0
    }

    mensagem = ft.Text(
        "",
        size=20,
        weight=ft.FontWeight.BOLD
    )

    nome = ft.TextField(
        label="Nome"
    )

    telefone = ft.TextField(
        label="Telefone",
        keyboard_type=ft.KeyboardType.NUMBER
    )

    tipo_entrega = ft.RadioGroup(
        value="retirada",
        content=ft.Row([
            ft.Radio(
                value="retirada",
                label="Retirada"
            ),
            ft.Radio(
                value="entrega",
                label="Entrega"
            )
        ])
    )

    rua = ft.TextField(
        label="Rua",
        visible=False
    )

    numero = ft.TextField(
        label="Número",
        visible=False
    )

    bairro = ft.TextField(
        label="Bairro",
        visible=False
    )

    complemento = ft.TextField(
        label="Complemento",
        visible=False
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

    botao_avancar = ft.Button(
        content="Avançar",
        disabled=not carrinho,
        
    )

    def mostrar_snackbar(texto):
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(texto)
            )
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
                            ),
                            ft.Button(
                                content="Remover",
                                on_click=lambda e, item=item: remover_item(item)
                            )
                        ]),
                        padding=15
                    )
                )
            )

        subtotal_carrinho.value = f"Subtotal: R$ {subtotal:.2f}"
        botao_avancar.disabled = not carrinho
        page.update()

    def buscar_pizza(nome):
        for pizza in pizzas:
            if pizza["sabor"] == nome:
                return pizza
        return None

    def remover_item(item):
        nome = item["nome"]
        carrinho.remove(item)

        if estado["pizza"] == nome:
            estado["pizza"] = None

        atualizar_carrinho()
        mostrar_snackbar(f"{nome} removida do carrinho.")

    def confirmar_limpeza(e):
        carrinho.clear()
        estado["pizza"] = None
        estado["tamanho"] = None
        page.pop_dialog()
        atualizar_carrinho()
        mostrar_snackbar("Carrinho limpo.")

    def cancelar_limpeza(e):
        page.pop_dialog()

    def limpar_carrinho(e):
        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Limpar carrinho"),
            content=ft.Text("Deseja realmente limpar o carrinho?"),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=cancelar_limpeza
                ),
                ft.TextButton(
                    "Confirmar",
                    on_click=confirmar_limpeza
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.show_dialog(dialogo)

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
        titulo.visible = True
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
        titulo.visible = False
        botao_avancar.on_click = mostrar_selecao

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
                ft.IconButton(
                    icon=ft.Icons.SHOPPING_CART,
                    tooltip="Carrinho",
                    on_click=mostrar_carrinho
                
                ),
                botao_avancar
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        ],
        expand=True)

        atualizar_carrinho()

    def atualizar_tipo_entrega(e=None):
        entrega = tipo_entrega.value == "entrega"

        rua.visible = entrega
        numero.visible = entrega
        bairro.visible = entrega
        complemento.visible = entrega
        estado["entrega"] = tipo_entrega.value
        estado["taxa_entrega"] = 6 if entrega else 0

    tipo_entrega.on_change = atualizar_tipo_entrega

    def validar_dados():
        nome_cliente = nome.value.strip()
        telefone_cliente = "".join(c for c in telefone.value if c.isdigit())

        if nome_cliente == "":
            mensagem.value = "Informe o nome."
            resultado.value = ""
            return False

        if len(telefone_cliente) not in (10, 11):
            mensagem.value = "O telefone deve ter 10 ou 11 dígitos."
            resultado.value = ""
            return False

        if tipo_entrega.value == "entrega" and rua.value.strip() == "":
            mensagem.value = "Informe a rua para realizar a entrega."
            resultado.value = ""
            return False

        return True

    def calcular(e=None):

        if not carrinho:
            mensagem.value = "Selecione pelo menos uma pizza."
            resultado.value = ""
            page.update()
            return

        if not validar_dados():
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

        desconto = 0
        frete = 6 if tipo_entrega.value == "entrega" else 0
        estado["taxa_entrega"] = frete

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
        titulo.visible = False

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
        atualizar_tipo_entrega()

        area_central.content = ft.Column([
            ft.Text(
                "Seleção",
                size=30,
                weight=ft.FontWeight.BOLD
            ),
            nome,
            telefone,
            tipo_entrega,
            ft.Row([
                rua,
                numero
            ]),
            ft.Row([
                bairro,
                complemento
            ]),
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
                    content="Avançar",
                    on_click=calcular
                ),
                ft.Button(
                    ft.IconButton(
                        icon=ft.Icons.SHOPPING_CART,
                        tooltip="Carrinho",
                        on_click=mostrar_carrinho)

                ),
                ft.IconButton(
                    icon=ft.Icons.HOME,
                    tooltip="Início",
                    on_click=mostrar_inicio
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        ],
        expand=True)

        page.update()

    def mostrar_carrinho(e=None):
        titulo.visible = False
        atualizar_carrinho()

        area_central.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "Meu carrinho",
                            size=30,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.TextButton(
                            "Remover tudo",
                            on_click=limpar_carrinho
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Container(
                    content=lista_carrinho,
                    expand=True
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            subtotal_carrinho,
                            mensagem,
                            ft.Button(
                                content="Continuar",
                                on_click=mostrar_selecao,
                                disabled=not carrinho
                            ),
                            ft.TextButton(
                                "Voltar ao cardápio",
                                on_click=mostrar_cardapio
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8
                    ),
                   
                )
            ],
            expand=True,
            spacing=10
        )

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
    espalhar_logo()
    page.update()

    async def animar_abertura():
        await asyncio.sleep(0.2)
        montar_logo()

    page.run_task(animar_abertura)


ft.run(main)
