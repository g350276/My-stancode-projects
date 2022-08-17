"""
File: babygraphics.py
Name: Marinda
--------------------------------
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950,
         1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index where the current year is in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                            with the current year.
    """
    distance = (width - GRAPH_MARGIN_SIZE * 2) // len(YEARS)
    return GRAPH_MARGIN_SIZE + distance * year_index


def draw_fixed_lines(canvas):
    """
    Draws the fixed background lines on the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # ----- Write your code below this line ----- #

    # Create top and bottom horizontal lines
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE,
                       width=LINE_WIDTH)
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE,
                       CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, width=LINE_WIDTH)

    # Create vertical lines
    for i in range(len(YEARS)):
        x = get_x_coordinate(CANVAS_WIDTH, i)
        canvas.create_line(x, 0, x, CANVAS_HEIGHT, width=LINE_WIDTH)
        canvas.create_text(x, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, text=YEARS[i], anchor=tkinter.NW)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # ----- Write your code below this line ----- #

    color_index = 0
    for name in lookup_names:

        # Setting color
        color = COLORS[color_index % len(COLORS)]
        color_index += 1

        # Dict of years and ranks info of the name
        year_ranking = name_data[name]
        sorted_year_ranking = {}

        # Fill missing year as '*' and sorted the dict by years
        for year in YEARS:
            if str(year) not in year_ranking:
                sorted_year_ranking[year] = '*'
            else:
                sorted_year_ranking[year] = year_ranking[str(year)]

        # Add lines and texts for each years
        for year_index in range(len(sorted_year_ranking)-1):

            # Find x and y coordinates of the current year
            x1 = get_x_coordinate(CANVAS_WIDTH, year_index)
            if sorted_year_ranking[YEARS[year_index]] == '*':
                rank1 = '*'
                y1 = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE
            else:
                rank1 = int(sorted_year_ranking[YEARS[year_index]])
                if rank1 > MAX_RANK:
                    rank1 = '*'
                    y1 = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                else:
                    y1 = ((CANVAS_HEIGHT - GRAPH_MARGIN_SIZE * 2) / MAX_RANK) * rank1 + GRAPH_MARGIN_SIZE

            # Find x and y coordinates of the next year
            x2 = get_x_coordinate(CANVAS_WIDTH, year_index+1)
            if sorted_year_ranking[YEARS[year_index+1]] == '*':
                rank2 = '*'
                y2 = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE
            else:
                rank2 = int(sorted_year_ranking[YEARS[year_index+1]])
                if rank2 > MAX_RANK:
                    rank2 = '*'
                    y2 = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                else:
                    y2 = ((CANVAS_HEIGHT - GRAPH_MARGIN_SIZE * 2) / MAX_RANK) * rank2 + GRAPH_MARGIN_SIZE

            # Add text and draw line
            text = str(name) + " " + str(rank1)
            canvas.create_line(x1, y1, x2, y2, width=LINE_WIDTH, fill=color)
            canvas.create_text(x1 + TEXT_DX, y1, text=text, anchor=tkinter.SW, fill=color)

            # Add text of the last year in the last loop
            if year_index == len(sorted_year_ranking)-2:
                text = str(name) + " " + str(rank2)
                canvas.create_text(x2 + TEXT_DX, y2, text=text, anchor=tkinter.SW, fill=color)


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
