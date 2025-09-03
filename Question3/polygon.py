import turtle  # using the built-in turtle module


# Koch-like step, mirrored to point inward
def draw_edge(length, depth):
    if depth == 0:
        turtle.forward(length)  # move pen forward
    else:
        part = length / 3

        # first segment
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


# quick visual check
draw_edge(200, 1)


turtle.done()  # keep window open
