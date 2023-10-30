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

### Our First SVG File
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