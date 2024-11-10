"""Out printing utilities."""


def bordered(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ["┌" + "─" * width + "┐"]
    for s in lines:
        res.append("│" + (s + " " * width)[:width] + "│")
    res.append("└" + "─" * width + "┘")
    return "\n".join(res)