def hex_to_rgb_string(hex_color):
    if not hex_color:
        return "99 102 241"

    hex_color = hex_color.strip().lstrip("#")

    if len(hex_color) != 6:
        return "99 102 241"

    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"{r} {g} {b}"
    except ValueError:
        return "99 102 241"
