# Group Members:
# - Ashish Bhusal Student ID: s395452
# - Nabin Pandey Student ID: s394815
# - Bashudev Adhikari Student ID: s394439

import turtle  # using the built-in turtle module


def draw_edge(length, depth):
    """
    Recursive edge function.
    Each edge gets split into 4 smaller edges with an inward dent.
    """
    if depth == 0:
        # base case, no recursion, draw straight line
        turtle.forward(length)  # move pen forward
    else:
        part = length / 3  # divide edge into 3 parts

        # first straight path
        draw_edge(part, depth - 1)

        # turn right to push the triangle inward relative to the edge
        turtle.right(60)
        draw_edge(part, depth - 1)

        # opposite turn to complete the triangle dent
        turtle.left(120)
        draw_edge(part, depth - 1)

        # return heading to original direction
        turtle.right(60)
        draw_edge(part, depth - 1)


# now try to make a polygon out of these recursive edges
def draw_polygon(sides, length, depth):
    """
    Draws a polygon with given number of sides.
    Each side is replaced by a recursive edge.
    """
    angle = 360 / sides  # turning angle at each corner
    for _ in range(sides):
        draw_edge(length, depth)  # draw one fractal edge
        turtle.right(angle)  # rotate to start next side


def main():
    # instead of hardcoding, ask the user
    sides = int(input("Enter the number of sides:"))
    length = int(input("Enter the side length:"))
    depth = int(input("Enter the recursion depth:"))

    # turtle setup for better visuals
    turtle.speed(0)  # fastest drawing
    turtle.hideturtle()  # hide the arrow
    turtle.bgcolor("white")
    turtle.color("black")

    # move turtle so drawing appears more centered on screen without this, part of the shape can go off the canvas
    turtle.penup()
    turtle.goto(-length / 2, length / 3)
    turtle.pendown()

    # now pass user values into the polygon function
    draw_polygon(sides, length, depth)

    turtle.done()  # keep window open until closed by user


if __name__ == "__main__":
    main()
