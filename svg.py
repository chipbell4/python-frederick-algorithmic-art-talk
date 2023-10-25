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
        viewBox="0 0 1 1",
        **kwargs
    )

def circle(cx, cy, r, **kwargs):
    return tag("circle", cx=cx, cy=cy, r=r, **kwargs)

circles = []
for x in frange(0, 1, 0.1):
    circles.append(circle(x, x, 0.01))

output = svg(children=circles)
print(output)