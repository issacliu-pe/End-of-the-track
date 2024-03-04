# module
import flet as ft
from flet import *
import random
import time

class GenerateGrid(UserControl):
    def __init__(self, difficulty):
        self.grid = Column(opacity=0, animate_opacity=300)
        self.blue_titles: int = 0
        self.difficulty: int = difficulty
        super().__init__()

    def build(self):
        # grid (4r x 4c)
        rows: list = [
            Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Container(
                        width=54,
                        height=54,
                        animate=300,
                        # border=border.all(1, "white"),
                        on_click=None, # change later
                    )
                    for _ in range(5)

                ],
            )
            for _ in range(5)

        ]

        # randomly put color in boxes
        colors: list = ["#5c443b", "#4cbbb5"]

        for row in rows:
            for container in row.controls[:]: # row.controls[:] = 4x containers()

                # make game harder everytime the player guesses all
                container.bgcolor = random.choices(colors, weights=[10, self.difficulty])[0]
                # store original color as part of container data, in order to check it when user play
                container.data = container.bgcolor
                # need to record how many blue tiles the instance
                if container.bgcolor == "#4cbbb5":
                    self.blue_titles += 1


        self.grid.controls = rows
        return self.grid


def main(page: ft.page):
    # some dimensions
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # UI's that will change with the course of the game
    stage = Text(size=13, weight=FontWeight.BOLD)
    result = Text(size=13, weight=FontWeight.BOLD)

    # start button that runs the game
    start_button = Container(
        content=ElevatedButton(
            on_click=lambda e: start_game(e, GenerateGrid(2)),
            content=Text("Start!", size=13, weight=FontWeight.BOLD),
            style=ButtonStyle(
                shape={"":RoundedRectangleBorder(radius=8)}, color={"": "white"},
            ),
            height=45,
            width=255,
        )
    )

    # set up the game loop
    def start_game(e, level):
        # create a variable of the instance
        grid = level
        page.controls.insert(3, grid)
        page.update()

        grid.grid.opacity = 1
        grid.grid.update()

        # change stage number
        stage.value = f"Stage: {grid.difficulty - 1}"
        stage.update()

        # disable the button to prevent the player from clicking it twice
        start_button.disabled = True
        start_button.update()

        time.sleep(1.5) # time for how long the blue tiles are shown

        # after 1.5 seconds, hide the blue tiles
        for rows in grid.controls[0].controls[:]:
            for container in rows.controls[:]:
                if container.bgcolor == "#4cbbb5":
                    pass # implement this later

    #main page add
    page.add(
        Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Text("Memory Matrix",
                     size=22,
                     weight=FontWeight.BOLD,
                )
            ],
        ),

        # result row
        Row(alignment=MainAxisAlignment.CENTER, controls=[result]),
        Divider(height=10, color="transparent"),
        Divider(height=10, color="transparent"),
        # test the class
        # GenerateGrid(2),
        # stage of the game row
        Row(alignment=MainAxisAlignment.CENTER, controls=[stage]),
        Divider(height=10, color="transparent"),
        # start button
        Row(alignment=MainAxisAlignment.CENTER, controls=[start_button]),
    )

    page.update()

if __name__ == '__main__':
    ft.app(target=main) # view in app
    # ft.app(target=main, view=ft.AppView.WEB_BROWSER) # view in web browser