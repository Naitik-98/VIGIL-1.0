from __future__ import annotations

from dataclasses import dataclass
from tkinter import font


@dataclass(slots=True, frozen=True)
class ColorPalette:
    background: str = "#181818"
    sidebar: str = "#202020"
    card: str = "#2B2B2B"
    accent: str = "#00C896"
    warning: str = "#FFC107"
    danger: str = "#E53935"
    text: str = "white"
    text_secondary: str = "#B0B0B0"
    border: str = "#3A3A3A"
    healthy: str = "#4CAF50"
    due_soon: str = "#FFC107"
    overdue: str = "#E53935"


DARK_PALETTE = ColorPalette()


@dataclass(slots=True, frozen=True)
class FontScheme:
    title: tuple[str, int, str]
    heading: tuple[str, int, str]
    subheading: tuple[str, int, str]
    normal: tuple[str, int, str]
    small: tuple[str, int, str]
    mono: tuple[str, int, str]

    def get_title(self) -> font.Font:
        return font.Font(family=self.title[0], size=self.title[1], weight=self.title[2])

    def get_heading(self) -> font.Font:
        return font.Font(family=self.heading[0], size=self.heading[1], weight=self.heading[2])

    def get_subheading(self) -> font.Font:
        return font.Font(family=self.subheading[0], size=self.subheading[1], weight=self.subheading[2])

    def get_normal(self) -> font.Font:
        return font.Font(family=self.normal[0], size=self.normal[1], weight=self.normal[2])

    def get_small(self) -> font.Font:
        return font.Font(family=self.small[0], size=self.small[1], weight=self.small[2])

    def get_mono(self) -> font.Font:
        return font.Font(family=self.mono[0], size=self.mono[1], weight=self.mono[2])


FONT_SCHEME = FontScheme(
    title=("Segoe UI", 16, "bold"),
    heading=("Segoe UI", 13, "bold"),
    subheading=("Segoe UI", 11, "bold"),
    normal=("Segoe UI", 10, "normal"),
    small=("Segoe UI", 9, "normal"),
    mono=("Courier New", 9, "normal"),
)


PADDING_LARGE = 16
PADDING_MEDIUM = 12
PADDING_SMALL = 8
BORDER_WIDTH = 1
CORNER_RADIUS = 8
