import time
from selenium import webdriver
from mspaint import MsPaint
import random

CHROME_DRIVER_PATH = "C:/Drivers/chromedriver/chromedriver_win32/chromedriver.exe"
COLORHUNT_SITES = ["https://colorhunt.co/palettes/neon", "https://colorhunt.co/palettes/happy",
                   "https://colorhunt.co/palettes/kids", "https://colorhunt.co/palettes/rainbow",
                   "https://colorhunt.co/palettes/christmas"]
MAX_COLORS_IN_ROW = 10
NUMBER_OF_COLORS = 25


def main():
    color_list: list = list()
    tmp_color_list: list = list()
    try:
        with open("colors.txt") as file:
            color_list = [color.replace('\n', '') for color in file.readlines()]
    except FileNotFoundError:
        driver = webdriver.Chrome(CHROME_DRIVER_PATH)

        for site in COLORHUNT_SITES:
            driver.get(site)
            time.sleep(0.2)
            palettes = driver.find_elements_by_css_selector(".item .palette .place span")[1:]
            color_list.extend([palette.get_attribute("data-copy") for palette in palettes])

        driver.close()

        color_list = list(set(color_list))
        random.shuffle(color_list)
        print(color_list)
        with open("colors.txt", mode='a') as file:
            for color in color_list:
                file.write(f"{color}\n")

    random.shuffle(color_list)
    color_list = list(set(color_list))
    color_list = [random.choice(color_list[:random.randint(20, 30)]) for _ in range(NUMBER_OF_COLORS)]
    # print(color_list)
    painter = MsPaint(color_list, MAX_COLORS_IN_ROW)
    painter.setup()


if __name__ == "__main__":
    main()
