import math

def frange(a, b, step):
    x = a
    while x < b:
        yield x
        x += step

def tag(name, children = [], **kwargs):
    # build attributes into a string
    attributes = ""
    for attr_name, attr_value in kwargs.items():
        attributes += f"{attr_name}='{attr_value}' "

    if len(children) == 0:
        return f"<{name} {attributes} />"

    middle = "\n".join(children)
    return f"<{name} {attributes}>{middle}</{name}>"

def svg(children=[], **kwargs):
    return tag(
        "svg",
        children=children,
        xmlns="http://www.w3.org/2000/svg",
        viewBox="-2 -2 4 4",
        **kwargs
    )

def circle(cx, cy, r, **kwargs):
    return tag("circle", cx=cx, cy=cy, r=r, **kwargs)

# EXAMPLE ONE
circles = []
for t in frange(0, 1, 0.1):
    circles.append(circle(t, t, 0.01))

# EXAMPLE TWO
circles = []
for t in frange(0, 1, 0.01):
    x = math.cos(t * math.tau)
    y = math.sin(t * math.tau)
    r = t * 0.05

    circles.append(circle(x, y, r))

# EXAMPLE THREE
circles = []
for t in frange(0, 5, 0.01):
    theta = t * math.tau
    spiral_radius = theta * 0.05

    x = spiral_radius * math.cos(theta)
    y = spiral_radius * math.sin(theta)
    radius = t * 0.01

    red = 0
    green = 255 * abs(math.cos(theta))
    blue = 255 * abs(math.sin(theta))
    fill = f"rgb({red}, {green}, {blue})"

    circles.append(circle(x, y, radius, fill=fill))


output = svg(children=circles)
print(output)