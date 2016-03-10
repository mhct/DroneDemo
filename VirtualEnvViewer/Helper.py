from collections import namedtuple

Point = namedtuple("Point", "x y z")
Cell = namedtuple("Cell", "x y height")
Resolution = namedtuple("Resolution", "x y")
MapWidth = namedtuple("MapWidth", "x y")
MapParams = namedtuple("MapParams", "map_width resolution")
Mesh = namedtuple("Mesh", "virtual_objects drone")