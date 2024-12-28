import re

with open("./index.html") as f:
    lines = f.readlines()

fans_regex = re.compile(r'href="([^"]+)">@([^<]+)<')
fans_set = set()

start_ind = -1
last_ind = -1
for ind, line in enumerate(lines):
    if start_ind != -1:
        if "</p>" in line:
            last_ind = ind
            break
        match = fans_regex.search(line.strip())
        if match:
            fans_set.add((match.group(1), match.group(2)))
    if "Fans (in alphabetical order):" in line:
        start_ind = ind

if start_ind == -1:
    raise ValueError("'Fans (in alphabetical order):' text not found in the index.html")
if last_ind == -1:
    raise ValueError("Closing '</p>' tag for closing fans list not found.")

def sort_key(fan):
    """
    Sorting key for fans:
    1. Sort by the first letter of the nickname (case-insensitive).
    2. If the first letter is the same, sort by whether it’s uppercase.
    3. Finally, sort alphabetically by the full nickname.
    """
    _nickname = fan[1]
    return (
        _nickname[0].lower(),
        _nickname[0].isupper(),
        _nickname.lower(),
    )


fans_list = sorted(fans_set, key=sort_key)

output = [
    f'        <a href="{_url}">@{_nickname}</a>{"," if len(fans_list) - 1 != ind else "."}\n'
    for ind, (_url, _nickname) in enumerate(fans_list)
]

lines[start_ind + 1 : last_ind] = output

with open("./index.html", "w+") as f:
    f.writelines(lines)
