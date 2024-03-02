"""
Carbon client factory function with customizable options
"""

from carbon import Carbon


def carbon_client(
    shadow=True, font_size=14, padding=48, window_controls=False, theme="vscode"
):
    """
    The `carbon_client` function
    allows users to create instances of the Carbon class with customizable options such as
    shadow, font size, padding, theme, etc. This provides flexibility for users to tailor Carbon
    instances according to their preferences when used elsewhere in the codebase.
    """

    client = Carbon(
        downloads_dir="userbot/downloads/",
        colour="rgba(171, 184, 195, 1)",
        shadow=shadow,
        shadow_blur_radius="68px",
        shadow_offset_y="20px",
        export_size="3x",
        font_size=f"{font_size}px",
        font_family="JetBrains Mono",
        first_line_number=1,
        language="auto",
        line_numbers=True,
        horizontal_padding=f"{padding}px",
        vertical_padding=f"{padding}px",
        theme=theme,
        watermark=False,
        width_adjustment=True,
        window_controls=window_controls,
        window_theme=None,
    )
    return client
