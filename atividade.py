import flet as ft


def main(page: ft.Page):

    page.title = "PizzaDev"

    titulo = ft.Text(
        "PizzaDev",
        size=40,
        weight=ft.FontWeight.BOLD
    )

    pizza = ft.Text(
        "Pizza Calabresa",
        size=30,
        weight=ft.FontWeight.BOLD
    )

    descricao = ft.Text(
        "Calabresa, cebola e muçarela"
    )

    preco = ft.Text(
        "M = R$ 32,00 | G = R$ 42,00"
    )

   
    quantidade = ft.TextField(
        label="Quantidade",
        hint_text="Digite de 1 a 10",
        width=300
    )

    
    tamanho = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="M", label="M - R$ 32,00"),
            ft.Radio(value="G", label="G - R$ 42,00"),
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

    
    def calcular(e):

        valor = quantidade.value.strip()

        
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
            preco_unitario = 32

        elif tamanho.value == "G":
            preco_unitario = 42

        else:
            mensagem.value = "Escolha o tamanho M ou G."
            resultado.value = ""
            page.update()
            return

        
        total = quantidade_num * preco_unitario

        mensagem.value = "Pedido calculado!"
        resultado.value = f"Parcial: R$ {total:.2f}"

        page.update()

    calcular_button = ft.Button(
        content="Calcular",
        on_click=calcular
    )

    page.add(
        titulo,
        pizza,
        descricao,
        preco,
        quantidade,
        tamanho,
        calcular_button,
        mensagem,
        resultado
    )


ft.run(main)