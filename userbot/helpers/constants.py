class First:
    ALIVE = "`I'm Alive, Master :3`"


class WWW:
    SpeedTest = (
        "Speedtest started at `{start}`\n\n"
        "Ping:\n{ping} ms\n\n"
        "Download:\n{downloads}\n\n"
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

