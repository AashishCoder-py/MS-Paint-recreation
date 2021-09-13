import time
from mspaint import MsPaint
import random

MAX_COLORS_IN_ROW = 10
NUMBER_OF_COLORS = 25


def main():
    """The Grand Main Method."""
    color_list: list = list()
    tmp_color_list: list = list()
    with open("colors.txt") as file:
        color_list = [color.replace('\n', '') for color in file.readlines()]  # remove the \n in every line

        color_list = list(set(color_list))
        random.shuffle(color_list)

    color_list = list(set(color_list))  # remove the common colours if any is present
    color_list = [random.choice(color_list[:random.randint(20, 30)]) for _ in range(NUMBER_OF_COLORS)]
    # print(color_list)
    
    painter = MsPaint(color_list, MAX_COLORS_IN_ROW)
    painter.setup()


if __name__ == "__main__":
    main()
