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


output = svg()
print(output)