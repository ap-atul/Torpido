from PyQt5.QtGui import QColor


class Color:
    BGR = "background"
    PRI = "primary"
    SEC = "secondary"
    TEX = "text"


class Type:
    RGB = "rgb"
    HEX = "hex"


THEME = {

    # default theme of the system
    "default": {
        Color.BGR: {
            Type.RGB: QColor(42, 42, 50),
            Type.HEX: "#2A2A32",
        },
        Color.PRI: {
            Type.RGB: QColor(72, 58, 78),
            Type.HEX: "#483A4E",
        },
        Color.SEC: {
            Type.RGB: QColor(119, 81, 87),
            Type.HEX: "#775157",
        },
        Color.TEX: {
            Type.RGB: QColor(179, 132, 103),
            Type.HEX: "#B38467",
        }
    },

    # M theme
    "XeTon": {
        Color.BGR: {
            Type.RGB: QColor(0, 53, 69),
            Type.HEX: "#003545",
        },
        Color.PRI: {
            Type.RGB: QColor(0, 69, 74),
            Type.HEX: "#00454a",
        },
        Color.SEC: {
            Type.RGB: QColor(60, 101, 98),
            Type.HEX: "#3c6562",
        },
        Color.TEX: {
            Type.RGB: QColor(237, 99, 99),
            Type.HEX: "#ed6363",
        }
    },

    # A theme
    "Crank": {
        Color.BGR: {
            Type.RGB: QColor(26, 26, 46),
            Type.HEX: "#1a1a2e",
        },
        Color.PRI: {
            Type.RGB: QColor(22, 40, 70),
            Type.HEX: "#172846",
        },
        Color.SEC: {
            Type.RGB: QColor(35, 64, 108),
            Type.HEX: "#23406C",
        },
        Color.TEX: {
            Type.RGB: QColor(233, 69, 96),
            Type.HEX: "#e94560",
        }
    },

    # As theme
    "Spider": {
        Color.BGR: {
            Type.RGB: QColor(57, 50, 50),
            Type.HEX: "#393232",
        },
        Color.PRI: {
            Type.RGB: QColor(77, 69, 69),
            Type.HEX: "#4d4545",
        },
        Color.SEC: {
            Type.RGB: QColor(141, 98, 98),
            Type.HEX: "#8d6262",
        },
        Color.TEX: {
            Type.RGB: QColor(237, 141, 141),
            Type.HEX: "#ed8d8d",
        }
    },

    # S theme
    "Surajstan": {
        Color.BGR: {
            Type.RGB: QColor(33, 33, 33),
            Type.HEX: "#212121",
        },
        Color.PRI: {
            Type.RGB: QColor(50, 50, 50),
            Type.HEX: "#323232",
        },
        Color.SEC: {
            Type.RGB: QColor(13, 115, 119),
            Type.HEX: "#0d7377",
        },
        Color.TEX: {
            Type.RGB: QColor(20, 255, 236),
            Type.HEX: "#14ffec",
        }
    },

    "Light": {
        Color.BGR: {
            Type.RGB: QColor(243, 242, 218),
            Type.HEX: "#f3f2da",
        },
        Color.PRI: {
            Type.RGB: QColor(78, 141, 124),
            Type.HEX: "#4e8d7c",
        },
        Color.SEC: {
            Type.RGB: QColor(4, 87, 98),
            Type.HEX: "#045762",
        },
        Color.TEX: {
            Type.RGB: QColor(253, 58, 105),
            Type.HEX: "#fd3a69",
        }
    },

    "Light_Shadow": {
        Color.BGR: {
            Type.RGB: QColor(244, 244, 242),
            Type.HEX: "#f4f4f2",
        },
        Color.PRI: {
            Type.RGB: QColor(232, 232, 232),
            Type.HEX: "#e8e8e8",
        },
        Color.SEC: {
            Type.RGB: QColor(187, 191, 202),
            Type.HEX: "#bbbfca",
        },
        Color.TEX: {
            Type.RGB: QColor(73, 84, 100),
            Type.HEX: "#495464",
        }
    }
}

STYLESHEET = {
    "default": "./ui/theme/default.qss",
    "XeTon": "./ui/theme/xeton.qss",
    "Crank": "./ui/theme/crank.qss",
    "Spider": "./ui/theme/spider.qss",
    "Surajstan": "./ui/theme/surajstan.qss",
    "Light": "./ui/theme/light.qss",
    "Light_Shadow": "./ui/theme/shadow.qss",
}


def get_theme(style: str):
    """ Returns the colors for the theme style """
    if style in THEME:
        return THEME[style]

    # if some how style not found
    return THEME["default"]


def get_all_themes():
    """ Returns the list of the themes """
    return sorted(list(THEME.keys()))


def get_style_sheet(style):
    """ Returns the path for the style sheet """
    if style in STYLESHEET:
        return STYLESHEET[style]

    # if some hot style not found
    return STYLESHEET["default"]
