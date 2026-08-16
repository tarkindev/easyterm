"""Theme definitions. Uses Textual's native Theme system, so switching
themes automatically restyles every built-in widget (Header, Footer,
Input, scrollbars) plus any of our own CSS that references theme
variables ($primary, $accent, etc) instead of hardcoded colors.
"""

from textual.theme import Theme

THEMES: dict[str, Theme] = {
    "matrix": Theme(
        name="matrix",
        primary="#39ff9d",
        secondary="#7ee787",
        accent="#39ff9d",
        foreground="#c9d1d9",
        background="#0a0e14",
        surface="#0d1117",
        panel="#0d1117",
        success="#7ee787",
        warning="#ffb454",
        error="#ff5f56",
        dark=True,
    ),
    "synthwave": Theme(
        name="synthwave",
        primary="#ff71ce",
        secondary="#01cdfe",
        accent="#ff71ce",
        foreground="#f4eeff",
        background="#170524",
        surface="#241734",
        panel="#241734",
        success="#05ffa1",
        warning="#fffb96",
        error="#ff5f56",
        dark=True,
    ),
    "amber": Theme(
        name="amber",
        primary="#ffb000",
        secondary="#ff8800",
        accent="#ffb000",
        foreground="#ffd580",
        background="#120b00",
        surface="#1a1200",
        panel="#1a1200",
        success="#a8ff60",
        warning="#ffb000",
        error="#ff5f56",
        dark=True,
    ),
    "ocean": Theme(
        name="ocean",
        primary="#39c5ff",
        secondary="#7ee7ff",
        accent="#39c5ff",
        foreground="#cdeeff",
        background="#061019",
        surface="#0b1b28",
        panel="#0b1b28",
        success="#4fe0a8",
        warning="#ffcc66",
        error="#ff5f56",
        dark=True,
    ),
}

DEFAULT_THEME = "matrix"