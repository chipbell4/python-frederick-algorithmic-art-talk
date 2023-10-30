import math


def frange(a, b, step):
    x = a
    while x < b:
        yield x
        x += step


def tag(name, children=[], **kwargs):
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
        **kwargs,
    )


def circle(cx, cy, r, **kwargs):
    return tag("circle", cx=cx, cy=cy, r=r, **kwargs)


def line(points, **kwargs):
    point_string = " ".join([f"{p[0]},{p[1]}" for p in points])
    return tag("polyline", points=point_string, **kwargs)


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

# EXAMPLE FOUR
points = [(0, 0), (1, 1)]

output = svg(
    children=[
        line(
            points,
            **{
                "stroke": "blue",
                "stroke-width": 0.05,
            },
        )
    ]
)


# EXAMPLE FIVE
def lerp(p1, p2, t):
    x1, y1 = p1
    x2, y2 = p2
    return [x1 + (x2 - x1) * t, y1 + (y2 - y1) * t]


def subdivide(p1, p2):
    # The 1/3, 1/2 and 2/3 marks
    p33 = lerp(p1, p2, 0.333)
    p66 = lerp(p1, p2, 0.666)
    pM = lerp(p1, p2, 0.5)

    # perturb the middle point PERPENDICULAR to the original line segment
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    pM[0] += dy * 0.2
    pM[1] += -dx * 0.2

    # Return all of the newly created points
    return [
        p1,
        p33,
        pM,
        p66,
        p2,
    ] 


def subdivide_all(items):
    # loop over each pair subdividing
    subdivided_items = []
    for left_index in range(len(items) - 1):
        left = items[left_index]
        right = items[left_index + 1]
        subdivided_items += subdivide(left, right)
    return subdivided_items


# start with a triangle
points = [
    (1.7, 0),
    (0, 1),
    (0, -1),
    (1.7, 0),
]

for k in range(3):
    points = subdivide_all(points)

output = svg(
    children=[
        line(
            points,
            **{
                "fill": "#444",
                "stroke": "#444",
                "stroke-width": 0.01,
            },
        )
    ]
)

print(output)
