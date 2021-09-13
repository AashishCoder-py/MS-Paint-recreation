import tkinter as tk
from tkinter import colorchooser
from turtle import RawTurtle, TurtleScreen

CANVAS_HEIGHT = 350
CANVAS_WIDTH = 500


class MsPaint:
    def __init__(self, color_list: list, max_colors_in_row: int):
        self.max_colors_in_row = max_colors_in_row
        self.__raw_color_list: list = color_list
        if "#000000" not in self.__raw_color_list:
            self.__raw_color_list.append("#000000")
        self.color_list = list()
        self.windows = tk.Tk()
        self.canvas = tk.Canvas(self.windows)
        self.color_frame = tk.LabelFrame(self.windows)
        self.tool_frame = tk.LabelFrame(self.windows)

        self.size_chooser_spinbox = tk.Spinbox(master=self.tool_frame, from_=1, to=10, width=5)

        self.clear_button = tk.Button(self.tool_frame, text="Clear")

        self.color_chooser_image = tk.PhotoImage(file="./images/color.gif")
        self.current_color: str = ""
        self.current_color_label = tk.Label(self.windows)
        self.color_chooser = tk.Button(self.windows)

        self.pen_button = tk.Button(self.tool_frame)
        self.line_button = tk.Button(self.tool_frame)
        self.rectangle_button = tk.Button(self.tool_frame)
        self.circle_button = tk.Button(self.tool_frame)
        self.__button_list: list = [self.pen_button, self.line_button, self.rectangle_button, self.circle_button]
        self.__point_list: list[tuple] = list()

        self.coordinate_label = tk.Label(self.windows, text="x: ,y: ")

        self.screen = TurtleScreen(self.canvas)
        self.drawer = RawTurtle(self.screen, shape="classic")

    def setup(self):
        self.windows.title("MS Paint_recreation")

        self.tool_frame.config(
            labelanchor='n',
            text="Tools",
            padx=5,
            pady=5,
        )
        self.tool_frame.grid(column=2, row=0)

        # Canvas
        self.canvas.config(
            background="white",
            highlightthickness=0,
            cursor="plus",
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
        )
        self.canvas.bind("<Motion>", self.show_coordinates)

        self.coordinate_label.grid(column=0, row=3, padx=3, pady=10)
        self.canvas.grid(row=0, column=0, rowspan=2, columnspan=2)

        self.clear_button.config(command=self.clear_draw, font=("Calibri", 10, "bold"))
        self.clear_button.grid(column=0, row=1, padx=10, pady=10, ipadx=5, ipady=5)

        # Screen and Turtle movements
        self.drawer.penup()
        self.screen.tracer(0)

        # color buttons
        self.color_frame.config(
            labelanchor='sw',
            text="Color Section",
            padx=10,
            pady=5,
        )
        self.arrange_color_buttons()
        self.color_frame.grid(column=0, row=2, padx=25, pady=20)

        # Color picker
        self.color_chooser.config(
            padx=5,
            pady=5,
            image=self.color_chooser_image,
            command=self.choose_color,
        )
        self.color_chooser.grid(column=2, row=2, padx=20, pady=20)

        # Size spinbox
        self.size_chooser_spinbox.config(
            increment=0.1,
            command=lambda *args: self.drawer.pensize(self.size_chooser_spinbox.get()),
        )
        self.size_chooser_spinbox.grid(column=0, row=0, padx=10, pady=10)

        # Current color Label
        self.current_color_label.config(height=2, width=4, relief=tk.SUNKEN, fg="black", bg="black")
        self.current_color_label.grid(column=1, row=2)

        # Pen, Line, Rectangle, Circle
        self.pen_button.config(command=self.setup_pen, text="✏")
        self.pen_button.grid(column=0, row=2)
        self.line_button.config(command=self.setup_line, text="—")
        self.line_button.grid(column=0, row=3)
        self.rectangle_button.config(command=self.setup_rectangle, text="▬")
        self.rectangle_button.grid(column=0, row=4)
        self.circle_button.config(command=self.setup_circle, text="●")
        self.circle_button.grid(column=0, row=5)

        self.windows.mainloop()

    def show_coordinates(self, event):
        self.coordinate_label.config(text=f"x: {event.x}, y: {event.y}")

    def click_handler(self, x, y) -> None:
        """Executed on mouse click."""
        self.drawer.penup()
        self.drawer.setposition(x, y)
        self.drawer.pendown()
        self.screen.update()
        self.drawer.ondrag(self.drag_handler)

    def drag_handler(self, x, y) -> None:
        """Drag the turtle to draw on mouse click.."""
        self.drawer.ondrag(self.do_nothing)
        self.drawer.pendown()
        self.drawer.setheading(self.drawer.towards(x, y))
        self.drawer.setposition(x, y)
        self.screen.update()
        self.windows.update_idletasks()
        self.drawer.penup()
        self.drawer.ondrag(self.drag_handler)

    def release_handler(self, x, y) -> None:
        """Executed when mouse button is released."""
        self.drawer.penup()
        self.drawer.ondrag(self.do_nothing)

    def provide_color_grid_list(self) -> None:
        """Provide grid as per the position of elements in the color list."""
        c: list = self.__raw_color_list
        tmp_color_list = list()
        while c:
            removal: list = c[:self.max_colors_in_row] if len(c) >= self.max_colors_in_row else c[:len(c)]
            c = [element for element in c if element not in removal]
            tmp_color_list.append(removal)

        self.color_list: list[list[str]] = tmp_color_list

    def arrange_color_buttons(self) -> None:
        """Arrange the colors in color list"""
        self.provide_color_grid_list()

        for row in range(len(self.color_list)):
            for column in range(len(self.color_list[row])):
                button = tk.Button(self.color_frame)
                color: str = self.color_list[row][column]
                button.config(
                    background=color,
                    foreground=color,
                    text=" ",
                    height=1,
                    width=2,
                    # compound="center",
                    command=lambda c=color: self.select_color(c),
                )
                button.grid(column=column, row=row, in_=self.color_frame,
                            padx=2, pady=2,)

    def select_color(self, color) -> None:
        """Select a color."""
        self.current_color = color
        self.current_color_label.config(foreground=self.current_color,
                                        background=self.current_color)
        self.drawer.color(color)
    
    def choose_color(self):
        """Choose a color from tkinter color chooser."""
        color_data = colorchooser.askcolor(color="white")
        if all(color_data):
            color = color_data[1]

            self.__raw_color_list.append(color)
            self.arrange_color_buttons()

    def clear_draw(self):
        self.drawer.home()
        self.drawer.penup()
        self.drawer.clear()
        self.screen.update()

    def draw_line(self, x, y):
        self.drawer.pendown()
        self.drawer.goto(x, y)
        self.screen.update()

    def draw_circle(self, x, y):
        if len(self.__point_list) == 1:
            self.__point_list.append((x, y))

            x1, y1 = self.__point_list[0][0], self.__point_list[0][1]
            x2, y2 = self.__point_list[1][0], self.__point_list[1][1]
            radius: float = (((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5) / 2

            self.drawer.penup()
            self.drawer.setposition(x1, y1)
            self.drawer.setheading(self.drawer.towards(x2, y2) - 90)
            self.drawer.pendown()
            self.drawer.circle(radius)
            self.screen.update()
            self.__point_list = []
        else:
            self.__point_list.append((x, y))

    def draw_rectangle(self, x, y):
        if len(self.__point_list) == 1:
            self.__point_list.append((x, y))

            x1, y1 = self.__point_list[0][0], self.__point_list[0][1]
            x2, y2 = self.__point_list[1][0], self.__point_list[1][1]

            self.drawer.penup()
            self.drawer.setposition(x1, y1)
            self.drawer.pendown()
            path = [(x1, y2), (x2, y2), (x2, y1), (x1, y1)]
            for p in path:
                # print(p)
                self.drawer.setposition(p)
                self.screen.update()

            self.__point_list = []
        else:
            self.__point_list.append((x, y))

    def setup_pen(self) -> None:
        """Set up the pen when the pen button is clicked."""
        self.__point_list = []
        ls = self.__button_list[:]
        ls.remove(self.pen_button)
        for pen in ls:
            pen.config(relief=tk.SUNKEN)
        self.pen_button.config(relief=tk.RAISED)
        self.drawer.ondrag(self.do_nothing)
        self.screen.onclick(self.click_handler)
        self.screen.onkeyrelease(self.release_handler, '1')

    def setup_line(self) -> None:
        """Sets up the pen for line-drawing."""
        self.__point_list = []
        self.line_button.config(relief=tk.RAISED)
        ls = self.__button_list[:]
        ls.remove(self.line_button)
        for pen in ls:
            pen.config(relief=tk.SUNKEN)
        self.drawer.ondrag(self.do_nothing)
        self.screen.onclick(self.draw_line)
        self.screen.onkeyrelease(self.drawer.penup, '1')

    def setup_circle(self) -> None:
        """Sets up the pen for line-drawing."""
        self.__point_list = []
        self.circle_button.config(relief=tk.RAISED)
        ls = self.__button_list[:]
        ls.remove(self.circle_button)
        for pen in ls:
            pen.config(relief=tk.SUNKEN)
        self.screen.onclick(self.draw_circle)
        self.drawer.ondrag(self.do_nothing)

    def setup_rectangle(self) -> None:
        """Sets up the pen for line-drawing."""
        self.__point_list = []
        self.rectangle_button.config(relief=tk.RAISED)
        ls = self.__button_list[:]
        ls.remove(self.rectangle_button)
        for pen in ls:
            pen.config(relief=tk.SUNKEN)
        self.screen.onclick(self.draw_rectangle)
        self.drawer.ondrag(self.do_nothing)

    def do_nothing(self, *_) -> None:
        """Literally do nothing!"""
        pass
