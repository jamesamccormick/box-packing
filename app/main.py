# WIDTH, DEPTH, HEIGHT
START_POSITION = [0, 0, 0]

class RotationType:
    RT_WDH = 0
    RT_DWH = 1

    ALL = [RT_WDH, RT_DWH]


class Axis:
    WIDTH = 0
    HEIGHT = 1
    DEPTH = 2

    ALL = [WIDTH, HEIGHT, DEPTH]


def rect_intersect(item1, item2, x, y):
    d1 = item1.get_dimension()
    d2 = item2.get_dimension()

    cx1 = item1.position[x] + d1[x]/2
    cy1 = item1.position[y] + d1[y]/2
    cx2 = item2.position[x] + d2[x]/2
    cy2 = item2.position[y] + d2[y]/2

    ix = max(cx1, cx2) - min(cx1, cx2)
    iy = max(cy1, cy2) - min(cy1, cy2)

    return ix < (d1[x]+d2[x])/2 and iy < (d1[y]+d2[y])/2


def intersect(item1, item2):
    return (
        rect_intersect(item1, item2, Axis.WIDTH, Axis.HEIGHT) and
        rect_intersect(item1, item2, Axis.HEIGHT, Axis.DEPTH) and
        rect_intersect(item1, item2, Axis.WIDTH, Axis.DEPTH)
    )


class Item():
    def __init__(self, name, height, depth, width):
        self.name = name
        self.height = height
        self.depth = depth
        self.width = width
        self.rotation_type = 0
        self.position = START_POSITION

    def get_volume(self):
        return self.height * self.depth * self.width

    def get_dimension(self):
        if self.rotation_type == RotationType.RT_WDH:
            return [self.width, self.depth, self.height]
        elif self.rotation_type == RotationType.RT_DWH:
            return [self.depth, self.width, self.height]
        
        raise SystemError


class Box():
    def __init__(self, height, depth, width):
        self.height = height
        self.depth = depth
        self.width = width
        self.items = []
        self.items_not_fitted = []

    def add_item(self, item, pivot):
        fit = False
        valid_item_position = item.position
        item.position = pivot # indicates the axis which we will rotate our item around to try and fit it in

        for i in range(0, len(RotationType.ALL)):
            item.rotation_type = i
            dimension = item.get_dimension()
            if (
                self.width < pivot[0] + dimension[0] or
                self.depth < pivot[1] + dimension[1] or
                self.height < pivot[2] + dimension[2]
            ):
                continue

            fit = True

            for current_item_in_bin in self.items:
                if intersect(current_item_in_bin, item):
                    fit = False
                    break

            if fit:
                self.items.append(item)
                return fit

        if not fit:
            item.position = valid_item_position

        return fit

def run(box, items):

    items.sort(
        key=lambda item: item.get_volume(), reverse=True
    )

    for item in items:
        print(f'Packing {item.name}')

        fitted = False

        if not box.items:
            response = box.add_item(item, START_POSITION)

            if not response:
                box.items_not_fitted.append(item)

            continue # we've done first item, lets continue onto next item

        for axis in range(0, 3):
            items_in_box = box.items

            for ib in items_in_box:
                pivot = [0, 0, 0]
                w, h, d = ib.get_dimension()
                if axis == Axis.WIDTH:
                    pivot = [
                        ib.position[0] + w,
                        ib.position[1],
                        ib.position[2]
                    ]
                elif axis == Axis.HEIGHT:
                    pivot = [
                        ib.position[0],
                        ib.position[1] + h,
                        ib.position[2]
                    ]
                elif axis == Axis.DEPTH:
                    pivot = [
                        ib.position[0],
                        ib.position[1],
                        ib.position[2] + d
                    ]

                if box.add_item(item, pivot):
                    fitted = True
                    break
            if fitted:
                break

        if not fitted:
            box.items_not_fitted.append(item)

    return box


# box = Box(
#     height=400,
#     depth=400,
#     width=400
# )

# items = [
#     Item('CAULI_1', height=200, depth=200, width=50),
#     Item('PASSION_2', height=200, depth=50, width=200),
#     Item('MANGO_1', height=200, depth=200, width=20),
#     Item('MANGO_2', height=500, depth=200, width=20),
# ]

# run(box, items)