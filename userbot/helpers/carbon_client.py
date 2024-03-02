from carbon import Carbon


def carbon_client(
    shadow=True, font_size=14, padding=48, window_controls=False, theme="vscode"
):
    client = Carbon(
        downloads_dir="userbot/downloads/",  # Defaults to current directory
        colour="rgba(171, 184, 195, 1)",  # Hex or rgba color
        shadow=shadow,  # Turn on/off shadow
        shadow_blur_radius="68px",
        shadow_offset_y="20px",
        export_size="3x",  # resolution of exported image, e.g. 1x, 3x
        font_size=f"{font_size}px",
        font_family="JetBrains Mono",  # font family, e.g. JetBrains Mono, Fira Code.
        first_line_number=1,
        language="auto",  # programing language for properly highlighting
        line_numbers=True,  # turn on/off, line number
        horizontal_padding=f"{padding}px",
        vertical_padding=f"{padding}px",
        theme=theme,  # code theme
        watermark=False,  # turn on/off watermark
        width_adjustment=True,  # turn on/off width adjustment
        window_controls=window_controls,  # turn on/off window controls
        window_theme=None,
    )
    return client
