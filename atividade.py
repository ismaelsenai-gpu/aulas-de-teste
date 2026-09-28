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
                ft.Button(
                    content="Selecionar",
                    on_click=lambda e: selecionar(pizza)
                )
            ]),
            padding=20
        )
    )


def main(page: ft.Page):

    page.title = "PizzaDev"

    titulo = ft.Text(
        "PizzaDev",
        size=40,
        weight=ft.FontWeight.BOLD
    )

    pizza_selecionada = None

    pizza_texto = ft.Text(
        "Nenhuma pizza selecionada",
        size=30,
        weight=ft.FontWeight.BOLD
    )

    quantidade = ft.TextField(
        label="Quantidade",
        hint_text="Digite de 1 a 10",
        width=300
    )

    tamanho = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(
                value="M",
                label="M"
            ),
            ft.Radio(
                value="G",
                label="G"
            )
        ])
    )

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

    def selecionar_pizza(pizza):
        nonlocal pizza_selecionada

        pizza_selecionada = pizza

        pizza_texto.value = f"Pizza selecionada: {pizza['sabor']}"

        mensagem.value = pizza["Descricao"]

        page.update()

    lista_pizzas = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    for pizza in pizzas:
        lista_pizzas.controls.append(
            criar_cartao(
                pizza,
                selecionar_pizza
            )
        )

    def calcular(e):

        valor = quantidade.value.strip()

        if pizza_selecionada is None:
            mensagem.value = "Selecione uma pizza."
            resultado.value = ""
            page.update()
            return

        if valor == "":
            mensagem.value = "Digite uma quantidade."
            resultado.value = ""
            page.update()
            return

        if not valor.isdigit():
            mensagem.value = "A quantidade deve ser um número."
            resultado.value = ""
            page.update()
            return

        quantidade_num = int(valor)

        if quantidade_num < 1 or quantidade_num > 10:
            mensagem.value = "A quantidade deve estar entre 1 e 10."
            resultado.value = ""
            page.update()
            return

        if tamanho.value == "M":
            preco_unitario = pizza_selecionada["preços"]["M"]

        elif tamanho.value == "G":
            preco_unitario = pizza_selecionada["preços"]["G"]

        else:
            mensagem.value = "Escolha o tamanho M ou G."
            resultado.value = ""
            page.update()
            return

        subtotal = quantidade_num * preco_unitario

        if subtotal >= 100:
            desconto = subtotal * 0.05
        else:
            desconto = 0

        subtotal_com_desconto = subtotal - desconto

        if subtotal >= 100:
            frete = 0
        else:
            frete = 10

        total = subtotal_com_desconto + frete

        mensagem.value = "Pedido calculado!"

        resultado.value = (
            f"Quantidade: {quantidade_num}\n"
            f"Preço unitário: R$ {preco_unitario:.2f}\n"
            f"Subtotal: R$ {subtotal:.2f}\n"
            f"Desconto: R$ {desconto:.2f}\n"
            f"Frete: R$ {frete:.2f}\n"
            f"Total: R$ {total:.2f}"
        )

        page.update()

    calcular_button = ft.Button(
        content="Calcular",
        on_click=calcular
    )

    area_calculo = ft.Column([
        pizza_texto,
        quantidade,
        tamanho,
        calcular_button,
        mensagem,
        resultado
    ])

    page.add(
        titulo,
        ft.Container(
            content=lista_pizzas,
            expand=True
        ),
        area_calculo
    )


ft.run(main)