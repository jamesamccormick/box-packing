from ..main import Box, Item, run

def test_normal():
    box = Box(
        width=300,
        depth=400,
        height=200
    )

    items = [
        Item('GHERKIN', height=200, depth=400, width=200),
        Item('POTATO', height=100, depth=100, width=100),
        Item('TOMATO', height=100, depth=100, width=100),
        Item('RASPBERRY', height=100, depth=100, width=100),
        Item('ORANGE', height=100, depth=100, width=100),
        Item('PLANK', height=100, depth=400, width=100)
    ]

    box = run(box, items)

    assert len(box.items) == 6

    for item in box.items:
        print(f'{item.name} starts at {item.position} in rotation type {item.rotation_type}')
