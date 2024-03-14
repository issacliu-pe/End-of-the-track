import flet as ft
import random
import time
from flet import *

class GenerateGrid(UserControl):
    def __init__(self, difficulty):
        self.grid = Column(opacity=0, animate_opacity=300)
        self.blue_titles: int = 0
        self.correct: int = 0
        self.incorrect: int = 0
        self.difficulty: int = difficulty
        super().__init__()

    def show_color(self, e):
        # when player click a box, check to see if the original color was blue or not
        if e.control.data == "#4cbbb5":
            e.control.bgcolor = "#4cbbb5"
            e.control.opacity = 1
            e.control.update()
            # we also need to increment the self.correct
            self.correct += 1
            e.page.update()
        else:
            e.control.bgcolor = "#982c33"
            e.control.opacity = 1
            e.control.update()
            self.incorrect += 1
            e.page.update()

    def build(self):
        # grid (4r x 4c)
        rows: list = [
            Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    ft.Image(
                        src="https://picsum.photos/150/150",  # Placeholder image URL
                        fit=ImageFit.NONE,
                        repeat=ImageRepeat.NO_REPEAT,
                        border_radius=border_radius.all(10),
                        width=54,
                        height=54,
                        # animate=300,
                        # on_click=lambda e: self.show_color(e),
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
        # clear the title
        result.value = ""

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

        time.sleep(1) # time for how long the blue tiles are shown

        # after 1.5 seconds, hide the blue tiles
        for rows in grid.controls[0].controls[:]:
            for container in rows.controls[:]:
                if container.bgcolor == "#4cbbb5":
                    container.bgcolor = "#5c443b"
                    container.update()

        # last thing, handle the updates we get from the class everytime a user clicks a box
        while True:
            if grid.correct == grid.blue_titles:
                # first disable the grid to prevent more clicking
                grid.grid.disabled: bool = True
                grid.grid.update()

                # update the win title
                result.value: str = "You Win!"
                result.color = "green700"
                result.update()

                # sleep before clearing the screen
                time.sleep(2)
                result.value = ""
                page.controls.remove(grid) # remove instance
                page.update()

                # increase the difficulty
                difficulty = grid.difficulty + 1

                # call the strat_game fun again to play the next round
                start_game(e, GenerateGrid(difficulty))
                break

            # now check if the user runs out of guess
            if grid.incorrect == 3:
                result.value = "You loss!"
                result.color = "red700"
                result.update()
                time.sleep(2)
                page.controls.remove(grid)
                page.update()
                start_button.disabled = False
                start_button.update()
                break

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
        # stage of the game row
        Row(alignment=MainAxisAlignment.CENTER, controls=[stage]),
        Divider(height=10, color="transparent"),
        # start button
        Row(alignment=MainAxisAlignment.CENTER, controls=[start_button]),
    )

    page.update()

if __name__ == '__main__':
    ft.app(target=main) # view in app
