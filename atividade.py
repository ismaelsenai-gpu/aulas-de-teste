import flet as ft 

def main(page: ft.Page):
    page.title = "PizzaDev"

    titulo = ft.Text("PizzaDev",size=40,  weight=ft.FontWeight.BOLD)
    slogan = ft.Text("Mais pizza e menos guerra! ", size=32, weight=ft.FontWeight.BOLD)
    orientacao = ft.Text("Para pedir, peça! ")
    dupla = ft.Text("Dupla é SAMUEL")
    dados = ft.Text("Dados temporarios durante execução", size=40, weight=ft.FontWeight.NORMAL)
    page.add(titulo, slogan,orientacao, dupla, dados)




    

ft.run(main)