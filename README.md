# Algorithmic Art With Python

## Overview
- We'll use Python to create a Domain-Specific Language for writing SVG files
- Mostly a few functions and some clever math.

### Preliminary Things That Are Helpful

A function for writing an SVG tag:
```python
def tag(name, children=[], **kwargs):
    # build attributes into a string
    attributes = ""
    for attr_name, attr_value in kwargs.items():
        attributes += f"{attr_name}='{attr_value}' "

    if len(children) == 0:
        return f"<{name} {attributes} />"

    middle = "\n".join(children)
    return f"<{name} {attributes}>{middle}</{name}>"
```
- Allows child elements to be passed as an array of strings
- Returns a string of XML/SVG (and potentially HTML?!)
- Allows any element attributes to be passed as a keyword arguments

A clone of `range()` but for floating points:
```python
def frange(a, b, step):
    x = a
    while x < b:
        yield x
        x += step
```

## Our First SVG File
Let's create our first svg file. First, a function for generating the main SVG tag:
```python
def svg(children=[], **kwargs):
    return tag(
        "svg",
        children=children,
        xmlns="http://www.w3.org/2000/svg",
        viewBox="-2 -2 4 4",
        **kwargs,
    )
```
- `xmlns` is the "XML Namespace" which tells browsers/image software the XML schema and how to parse it.
- `viewBox` is the "viewport" for the file, like an xy plot. For example, this viewBox states that the minimum x and minimum y are -2. The viewBox is 4 units wide and 4 units high. As a results xy points outside of the range -2 to 2 will not be shown.

Now, another function for drawing a circle:
```python
def circle(cx, cy, r, **kwargs):
    return tag("circle", cx=cx, cy=cy, r=r, **kwargs)
```

And some code to draw it:
```python
circles = []
for t in frange(0, 1, 0.1):
    circles.append(circle(t, t, 0.01))

print(svg(
    children=[circle(0, 0, 1.0, fill="blue")]
))
```

## Example 1.5
Many Circles!
```python
print(svg(
    children=[
        circle(t, t, 0.01)
        for t in frange(0, 1, 0.1)
    ]
))
```

## Example 2
Circular circles
```python
print(svg(
    children=[
        circle(
            x=math.cos(t * math.tau)
            y=math.sin(t * math.tau)
            r=t * 0.05
        )
        for t in frange(0, 1, 0.01)
    ]
))
```

## Example 3
Spiral, with color:
```python
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

print(svg(children=circles))
```

## Example 4
A line segment, using `<polyline />`. Note the funky dictionary stuff.
That's because SVG uses hyphenation for a few attributes, and Python doesn't support hyphenated named parameters (I don't think?)
```python3
def line(points, **kwargs):
    point_string = " ".join([f"{p[0]},{p[1]}" for p in points])
    return tag("polyline", points=point_string, **kwargs)

print(svg(
    children=[
        line(
            [(0, 0), (1, 1)],
            **{
                "stroke": "blue",
                "stroke-width": 0.05,
            },
        )
    ]
))
```

# Example 5
A Koch snowflake fractal. We'll need a couple of things, hang on tight!

First, linear interpolation:
```python
def lerp(p1, p2, t):
    x1, y1 = p1
    x2, y2 = p2
    return [x1 + (x2 - x1) * t, y1 + (y2 - y1) * t]
```
- Given two points, finds a point on the line between them.
- If `t=0` returns p1
- If `t=1` returns p2
- If t is in-between returns a point on the line between `p1` and  `p2`.

The Koch line segment splitting algorithm:
```python
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
```

A function for applying the line-segment splitting algorithm to a set of line segments:
```python
def subdivide_all(items):
    # loop over each pair subdividing
    subdivided_items = []
    for left_index in range(len(items) - 1):
        left = items[left_index]
        right = items[left_index + 1]
        subdivided_items += subdivide(left, right)
    return subdivided_items
```

Now, start with an equilateral triangle:
```python
points = [
    (1.7, 0),
    (0, 1),
    (0, -1),
    (1.7, 0),
]
```

And subdivide a couple of times and print
```python
for k in range(3):
    points = subdivide_all(points)

print(svg(
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
))
```