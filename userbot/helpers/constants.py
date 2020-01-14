class First:
    ALIVE = "`Baka! Anata wa watashi ga shinu to omotta?`"


class Eval:
    RUNNING = "**Expression:**\n```{}```\n\n**Running...**"
    ERROR = "**Expression:**\n```{}```\n\n**Error:**\n```{}```"
    SUCCESS = "**Expression:**\n```{}```\n\n**Success** | `None`"
    RESULT = "**Expression:**\n```{}```\n\n**Result:**\n```{}```"
    RESULT_FILE = "**Expression:**\n```{}```\n\n**Result:**\nView `output.txt` below ⤵"

    ERROR_LOG = (
        "**Evaluation Query**\n"
        "```{}```\n"
        "erred in chat \"[{}](t.me/c/{}/{})\" with error\n"
        "```{}```"
    )

    SUCCESS_LOG = (
        "Evaluation Query\n"
        "```{}```\n"
        "succeeded in \"[{}](t.me/c/{}/{})\""
    )

    RESULT_LOG = (
        "Evaluation Query\n"
        "```{}```\n"
        "executed in chat \"[{}](t.me/c/{}/{})\"."
    )


class WWW:
    SpeedTest = (
        "Speedtest started at `{start}`\n\n"
        "Ping:\n{ping} ms\n\n"
        "Download:\n{download}\n\n"
        "Upload:\n{upload}\n\n"
        "ISP:\n__{isp}__"
    )

    NearestDC = (
        "Country: `{}`\n"
        "Nearest Datacenter: `{}`\n"
        "This Datacenter: `{}`"
    )


class MEMES:
    REVERSE = (
        "⠐⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠂\n"
        "⠄⠄⣰⣾⣿⣿⣿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣆⠄⠄\n"
        "⠄⠄⣿⣿⣿⡿⠋⠄⡀⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠋⣉⣉⣉⡉⠙⠻⣿⣿⠄⠄\n"
        "⠄⠄⣿⣿⣿⣇⠔⠈⣿⣿⣿⣿⣿⡿⠛⢉⣤⣶⣾⣿⣿⣿⣿⣿⣿⣦⡀⠹⠄⠄\n"
        "⠄⠄⣿⣿⠃⠄⢠⣾⣿⣿⣿⠟⢁⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠄⠄\n"
        "⠄⠄⣿⣿⣿⣿⣿⣿⣿⠟⢁⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄⠄\n"
        "⠄⠄⣿⣿⣿⣿⣿⡟⠁⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⠄\n"
        "⠄⠄⣿⣿⣿⣿⠋⢠⣾⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⠄⠄\n"
        "⠄⠄⣿⣿⡿⠁⣰⣿⣿⣿⣿⣿⣿⣿⣿⠗⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⡟⠄⠄\n"
        "⠄⠄⣿⡿⠁⣼⣿⣿⣿⣿⣿⣿⡿⠋⠄⠄⠄⣠⣄⢰⣿⣿⣿⣿⣿⣿⣿⠃⠄⠄\n"
        "⠄⠄⡿⠁⣼⣿⣿⣿⣿⣿⣿⣿⡇⠄⢀⡴⠚⢿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢠⠄⠄\n"
        "⠄⠄⠃⢰⣿⣿⣿⣿⣿⣿⡿⣿⣿⠴⠋⠄⠄⢸⣿⣿⣿⣿⣿⣿⣿⡟⢀⣾⠄⠄\n"
        "⠄⠄⢀⣿⣿⣿⣿⣿⣿⣿⠃⠈⠁⠄⠄⢀⣴⣿⣿⣿⣿⣿⣿⣿⡟⢀⣾⣿⠄⠄\n"
        "⠄⠄⢸⣿⣿⣿⣿⣿⣿⣿⠄⠄⠄⠄⢶⣿⣿⣿⣿⣿⣿⣿⣿⠏⢀⣾⣿⣿⠄⠄\n"
        "⠄⠄⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⠋⣠⣿⣿⣿⣿⠄⠄\n"
        "⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢁⣼⣿⣿⣿⣿⣿⠄⠄\n"
        "⠄⠄⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢁⣴⣿⣿⣿⣿⣿⣿⣿⠄⠄\n"
        "⠄⠄⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⢁⣴⣿⣿⣿⣿⠗⠄⠄⣿⣿⠄⠄\n"
        "⠄⠄⣆⠈⠻⢿⣿⣿⣿⣿⣿⣿⠿⠛⣉⣤⣾⣿⣿⣿⣿⣿⣇⠠⠺⣷⣿⣿⠄⠄\n"
        "⠄⠄⣿⣿⣦⣄⣈⣉⣉⣉⣡⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⠉⠁⣀⣼⣿⣿⣿⠄⠄\n"
        "⠄⠄⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣾⣿⣿⡿⠟⠄⠄\n"
        "⠠⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
    )

    SLAP_TEMPLATES = [
        "{hits} {victim} with a {item}.",
        "{hits} {victim} in the face with a {item}.",
        "{hits} {victim} around a bit with a {item}.",
        "{throws} a {item} at {victim}.",
        "grabs a {item} and {throws} it at {victim}'s face.",
        "{hits} a {item} at {victim}.", "{throws} a few {item} at {victim}.",
        "grabs a {item} and {throws} it in {victim}'s face.",
        "launches a {item} in {victim}'s general direction.",
        "sits on {victim}'s face while slamming a {item} {where}.",
        "starts slapping {victim} silly with a {item}.",
        "pins {victim} down and repeatedly {hits} them with a {item}.",
        "grabs up a {item} and {hits} {victim} with it.",
        "starts slapping {victim} silly with a {item}.",
        "holds {victim} down and repeatedly {hits} them with a {item}.",
        "prods {victim} with a {item}.",
        "picks up a {item} and {hits} {victim} with it.",
        "ties {victim} to a chair and {throws} a {item} at them.",
        "{hits} {victim} {where} with a {item}.",
        "ties {victim} to a pole and whips them {where} with a {item}."
        "gave a friendly push to help {victim} learn to swim in lava.",
        "sent {victim} to /dev/null.", "sent {victim} down the memory hole.",
        "beheaded {victim}.", "threw {victim} off a building.",
        "replaced all of {victim}'s music with Nickelback.",
        "spammed {victim}'s email.", "made {victim} a knuckle sandwich.",
        "slapped {victim} with pure nothing.",
        "hit {victim} with a small, interstellar spaceship.",
        "quickscoped {victim}.", "put {victim} in check-mate.",
        "RSA-encrypted {victim} and deleted the private key.",
        "put {victim} in the friendzone.",
        "slaps {victim} with a DMCA takedown request!"
    ]

    ITEMS = [
        "cast iron skillet",
        "large trout",
        "baseball bat",
        "cricket bat",
        "wooden cane",
        "nail",
        "printer",
        "shovel",
        "pair of trousers",
        "CRT monitor",
        "diamond sword",
        "baguette",
        "physics textbook",
        "toaster",
        "portrait of Richard Stallman",
        "television",
        "mau5head",
        "five ton truck",
        "roll of duct tape",
        "book",
        "laptop",
        "old television",
        "sack of rocks",
        "rainbow trout",
        "cobblestone block",
        "lava bucket",
        "rubber chicken",
        "spiked bat",
        "gold block",
        "fire extinguisher",
        "heavy rock",
        "chunk of dirt",
        "beehive",
        "piece of rotten meat",
        "bear",
        "ton of bricks",
    ]

    THROW = [
        "throws",
        "flings",
        "chucks",
        "hurls",
    ]

    HIT = [
        "hits",
        "whacks",
        "slaps",
        "smacks",
        "bashes",
    ]

    WHERE = ["in the chest", "on the head", "on the butt", "on the crotch"]

    REPLACEMENT_MAP = {
        "a": "ɐ",
        "b": "q",
        "c": "ɔ",
        "d": "p",
        "e": "ǝ",
        "f": "ɟ",
        "g": "ƃ",
        "h": "ɥ",
        "i": "ᴉ",
        "j": "ɾ",
        "k": "ʞ",
        "l": "l",
        "m": "ɯ",
        "n": "u",
        "o": "o",
        "p": "d",
        "q": "b",
        "r": "ɹ",
        "s": "s",
        "t": "ʇ",
        "u": "n",
        "v": "ʌ",
        "w": "ʍ",
        "x": "x",
        "y": "ʎ",
        "z": "z",
        "A": "∀",
        "B": "B",
        "C": "Ɔ",
        "D": "D",
        "E": "Ǝ",
        "F": "Ⅎ",
        "G": "פ",
        "H": "H",
        "I": "I",
        "J": "ſ",
        "K": "K",
        "L": "˥",
        "M": "W",
        "N": "N",
        "O": "O",
        "P": "Ԁ",
        "Q": "Q",
        "R": "R",
        "S": "S",
        "T": "┴",
        "U": "∩",
        "V": "Λ",
        "W": "M",
        "X": "X",
        "Y": "⅄",
        "Z": "Z",
        "0": "0",
        "1": "Ɩ",
        "2": "ᄅ",
        "3": "Ɛ",
        "4": "ㄣ",
        "5": "ϛ",
        "6": "9",
        "7": "ㄥ",
        "8": "8",
        "9": "6",
        ",": "'",
        ".": "˙",
        "?": "¿",
        "!": "¡",
        '"': ",,",
        "'": ",",
        "(": ")",
        ")": "(",
        "[": "]",
        "]": "[",
        "{": "}",
        "}": "{",
        "<": ">",
        ">": "<",
        "&": "⅋",
        "_": "‾",
    }
