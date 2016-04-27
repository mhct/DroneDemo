OBJECT_NAME = "Middle Wall"
FILE_NAME = "virtual_object_middle_wall.txt"
X_ORIGIN = 0
Y_ORIGIN = 40
X_WIDTH = 40
Y_WIDTH = 1
HEIGHT = 4000 # in millimeters


content = OBJECT_NAME + "\n"

for x in range(X_ORIGIN, X_ORIGIN + X_WIDTH):
    for y in range(Y_ORIGIN, Y_ORIGIN + Y_WIDTH):
        content += "%d %d %d \n" % (x, y, HEIGHT)

file = open(FILE_NAME, "w")
file.write(content)