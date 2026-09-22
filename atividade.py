import flet as ft 

def main(page: ft.Page):
    page.title = "PizzaDev"

    titulo = ft.Text("PizzaDev",size=40,  weight=ft.FontWeight.BOLD)
    slogan = ft.Text("Mais pizza e menos guerra! ", size=32, weight=ft.FontWeight.BOLD)
    orientacao = ft.Text("Para pedir, peça! ")
    dupla = ft.Text("Dupla é SAMUEL")
    dados = ft.Text("Dados temporarios durante execução", size=40, weight=ft.FontWeight.NORMAL)
    page.add(titulo, slogan,orientacao, dupla, dados)

    card = ft.Container(
    padding=15,
    border_radius=12,
    content=ft.Column([
    ft.Text("Calabresa", size=20, weight=ft.FontWeight.BOLD),
    ft.Text("calabresa, cebola e muçarela"),
    ft.Row([ft.Text("P: R$ 30"), ft.Text("G: R$ 40")])
    ])
    )
    page.add(ft.Column([card], scroll=ft.ScrollMode.AUTO))


    

ft.run(main)