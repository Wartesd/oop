import json
import os
from enum import Enum
from typing import Tuple, Literal


class Color(Enum):
    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    RESET = "\033[0m"


FONT_FILE = "font.json"

if os.path.exists(FONT_FILE):
    with open(FONT_FILE, "r", encoding="utf-8") as file:
        FONT_DATA = json.load(file)
else:
    raise FileNotFoundError(FONT_FILE)

Size = Literal["small", "medium", "large"]


class Printer:
    def __init__(
            self,
            color: Color,
            position: Tuple[int, int] | None = None,
            symbol: str = "*",
            size: Size = "medium"
    ):
        self.color = color
        self.symbol = symbol
        self.original_position = (0, 0)
        self.position = position or self.original_position
        self.size = size
        self.font = FONT_DATA[size]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(Color.RESET.value, end="")

    @staticmethod
    def print(
            text: str,
            color: Color,
            position: Tuple[int, int] | None = None,
            symbol: str = "*",
            size: Size = "medium"
    ):
        Printer._render_text(text, color, position, symbol, size)

    def print_text(self, text: str):
        Printer._render_text(text, self.color, self.position, self.symbol, self.size)

    @staticmethod
    def _render_text(
            text: str,
            color: Color,
            position: Tuple[int, int],
            symbol: str = None,
            size: Size = "medium"
    ):
        position = position or (0, 0)
        coordinate_settings = f"\033[{position[1]};{position[0]}H"
        print(color.value, end="")

        font = FONT_DATA[size]
        lines = ["" for _ in range(font['height'])]

        for char in text.upper():
            if char in font["symbols"]:
                char_pattern = font["symbols"][char].split("\n")
                for i, line in enumerate(char_pattern):
                    if symbol:
                        line = line.replace("*", symbol)
                    lines[i] += line + "  "

        for line in lines:
            print(coordinate_settings, line)
        print(Color.RESET.value, end="")


if __name__ == "__main__":
    print("\n" * 30)

    # Статическое использование с разными размерами
    Printer.print("SMALL", Color.RED, (5, 5), "#", "small")
    Printer.print("MEDIUM", Color.GREEN, (5, 12), "$", "medium")
    Printer.print("LARGE", Color.BLUE, (5, 20), "@", "large")

    # Использование с контекстным менеджером и разными размерами
    with Printer(Color.CYAN, (40, 5), "₽", "small") as printer:
        printer.print_text("SMALL TEXT")

    with Printer(Color.MAGENTA, (40, 12), "€", "medium") as printer:
        printer.print_text("MEDIUM TEXT")

    with Printer(Color.YELLOW, (40, 20), "¥", "large") as printer:
        printer.print_text("LARGE TEXT")
