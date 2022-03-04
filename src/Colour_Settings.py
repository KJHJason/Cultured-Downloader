def colour(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

class TerminalColours:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = '\033[4m'
    RED = colour(255, 0, 0)
    GREEN = colour(0, 255, 0)
    BLUE = colour(0, 0, 255)
    WHITE = colour(255, 255, 255)
    BLACK = colour(0, 0, 0)
    YELLOW = colour(255, 255, 0)
    PURPLE = colour(255, 0, 255)
    CYAN = colour(0, 255, 255)
    ORANGE = colour(255, 165, 0)
    BROWN = colour(165, 42, 42)
    LIGHT_BLUE = colour(0, 191, 255)
    LIGHT_GREEN = colour(144, 238, 144)
    LIGHT_RED = colour(255, 182, 193)
    LIGHT_PURPLE = colour(255, 20, 147)
    LIGHT_CYAN = colour(0, 255, 255)
    LIGHT_ORANGE = colour(255, 140, 0)
    LIGHT_BROWN = colour(210, 180, 140)
    DARK_BLUE = colour(0, 0, 139)
    DARK_GREEN = colour(0, 100, 0)
    DARK_RED = colour(139, 0, 0)
    DARK_PURPLE = colour(128, 0, 128)
    DARK_CYAN = colour(0, 139, 139)
    DARK_ORANGE = colour(255, 140, 0)
    DARK_BROWN = colour(165, 42, 42)
    LIGHT_GRAY = colour(211, 211, 211)
    DARK_GRAY = colour(169, 169, 169)