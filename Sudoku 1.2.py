# Sudoku Version 2

import pygame
import random

# Set Up
pygame.init()

side_width = 70
border_width = 10
inner_line_width = 4
box_width = 60

screen_length = 2 * side_width + 4 * border_width + 6 * inner_line_width + 9 * box_width

wn = pygame.display.set_mode((screen_length, screen_length))
pygame.display.set_caption("Sudoku 1.2")
bg_colour = (255, 255, 255)

# Board
board = [0,  0,  0,  0,  0,  0,  0,  0,  0,
         0,  12, 0,  0,  0,  0,  10, 15, 0,
         0,  15, 16, 0,  12, 14, 0,  0,  13,
         15, 0,  17, 10, 11, 0,  18, 0,  0,
         0,  18, 0,  0,  17, 0,  0,  12, 0,
         0,  0,  11, 0,  16, 18, 17, 0,  15,
         17, 0,  0,  15, 18, 0,  12, 14, 0,
         0,  11, 15, 0,  0,  0,  0,  18, 0,
         0,  0,  0,  0,  0,  0,  0,  0,  0]

border_colour = (0, 0, 0)
inner_line_colour = (60, 60, 60)
line_length = screen_length - 2 * side_width
font = pygame.font.SysFont("Times New Roman", 57)
number_colour = (100, 100, 170)

auto_solving = False
testing = False
show = True


# Main Game

def play():
    global show
    selected = [0, 0]
    while True:
        pygame.display.update()
        wn.fill(bg_colour)

        draw_board(border_colour, inner_line_colour)

        title("Sudoku")

        draw_numbers()

        check_mouse()

        selection(selected)

        update_numbers()

        check_rows()
        check_columns()
        check_box()

        win()

        pygame.draw.rect(wn, (50, 50, 150), (55, 15, 40, 40))
        pygame.draw.rect(wn, (200, 10, 10), (105, 15, 40, 40))
        if show:
            pygame.draw.rect(wn, (100, 250, 100), (600, 15, 40, 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                confirm(selected)
                selected = select()

                pos = pygame.mouse.get_pos()
                if 55 <= pos[0] <= 95 and 15 <= pos[1] <= 55:
                    auto_solve_1()

                elif 105 <= pos[0] <= 145 and 15 <= pos[1] <= 55:
                    create_new()

                elif 600 <= pos[0] <= 640 and 15 <= pos[1] <= 55:
                    if show:
                        show = False


def title(phrase):
    title_font = pygame.font.SysFont("Times New Roman", 65)
    title = title_font.render(phrase, 1, (0, 0, 0))
    wn.blit(title, (screen_length//2 - title.get_width()//2, 0))


def draw_board(border_colour, inner_line_colour):

    # Vertical Inner Lines
    pygame.draw.rect(wn, inner_line_colour, (side_width + border_width + box_width, side_width,
                                             inner_line_width, line_length))
    pygame.draw.rect(wn, inner_line_colour, (side_width + border_width + 2 * box_width + inner_line_width, side_width,
                                             inner_line_width, line_length))
    pygame.draw.rect(wn, inner_line_colour,
                     (side_width + 2 * border_width + 4 * box_width + 2 * inner_line_width, side_width,
                      inner_line_width, line_length))
    pygame.draw.rect(wn, inner_line_colour,
                     (side_width + 2 * border_width + 5 * box_width + 3 * inner_line_width, side_width,
                      inner_line_width, line_length))
    pygame.draw.rect(wn, inner_line_colour,
                     (side_width + 3 * border_width + 7 * box_width + 4 * inner_line_width, side_width,
                      inner_line_width, line_length))
    pygame.draw.rect(wn, inner_line_colour,
                     (side_width + 3 * border_width + 8 * box_width + 5 * inner_line_width, side_width,
                      inner_line_width, line_length))

    # Horizontal Inner Lines
    pygame.draw.rect(wn, inner_line_colour, (side_width, side_width + border_width + box_width,
                                             line_length, inner_line_width))
    pygame.draw.rect(wn, inner_line_colour, (side_width, side_width + border_width + 2 * box_width + inner_line_width,
                                             line_length, inner_line_width))
    pygame.draw.rect(wn, inner_line_colour,
                     (side_width, side_width + 2 * border_width + 4 * box_width + 2 * inner_line_width,
                      line_length, inner_line_width))
    pygame.draw.rect(wn, inner_line_colour,
                     (side_width, side_width + 2 * border_width + 5 * box_width + 3 * inner_line_width,
                      line_length, inner_line_width))
    pygame.draw.rect(wn, inner_line_colour,
                     (side_width, side_width + 3 * border_width + 7 * box_width + 4 * inner_line_width,
                      line_length, inner_line_width))
    pygame.draw.rect(wn, inner_line_colour,
                     (side_width, side_width + 3 * border_width + 8 * box_width + 5 * inner_line_width,
                      line_length, inner_line_width))

    # Vertical Border Lines
    pygame.draw.rect(wn, border_colour, (side_width, side_width, border_width, line_length))
    pygame.draw.rect(wn, border_colour, (side_width + 2 * inner_line_width + border_width + 3 * box_width, side_width,
                                         border_width, line_length))
    pygame.draw.rect(wn, border_colour,
                     (side_width + 4 * inner_line_width + 2 * border_width + 6 * box_width, side_width,
                      border_width, line_length))
    pygame.draw.rect(wn, border_colour,
                     (side_width + 6 * inner_line_width + 3 * border_width + 9 * box_width, side_width,
                      border_width, line_length))

    # Horizontal Border Lines
    pygame.draw.rect(wn, border_colour, (side_width, side_width, line_length, border_width))
    pygame.draw.rect(wn, border_colour, (side_width, side_width + border_width + 2 * inner_line_width + 3 * box_width,
                                         line_length, border_width))
    pygame.draw.rect(wn, border_colour,
                     (side_width, side_width + 2 * border_width + 4 * inner_line_width + 6 * box_width,
                      line_length, border_width))
    pygame.draw.rect(wn, border_colour,
                     (side_width, side_width + 3 * border_width + 6 * inner_line_width + 9 * box_width,
                      line_length, border_width))


def update_numbers(index=None):
    pos = 1
    if auto_solving and show:
        pygame.display.update()
        wn.fill(bg_colour)
        draw_board(border_colour, inner_line_colour)
        title("Sudoku")
        draw_numbers()
        check_mouse()
        highlighted(index)

    if auto_solving and not show:
        pygame.draw.rect(wn, (255, 255, 255), (200, 0, 400, side_width))
        title("Please Wait")
        pygame.display.update()

    else:
        for number in board:
            if number != 0:
                if number > 9:
                    number -= 9
                    display = font.render(str(number), 1, number_colour)
                else:
                    display = font.render(str(number), 1, (0, 0, 0))
                row = pos // 9
                if pos % 9 == 0:
                    row -= 1
                column = pos % 9 - 1
                if column == -1:
                    column = 8

                h_bords = row // 3
                v_bords = column // 3

                h_line = row - h_bords
                v_line = column - v_bords

                y = side_width + row * box_width + (h_bords + 1) * border_width + h_line * inner_line_width
                x = side_width + column * box_width + (v_bords + 1) * border_width + v_line * inner_line_width + 15
                wn.blit(display, (x, y))
            pos += 1


def check_mouse():
    pos = pygame.mouse.get_pos()
    highlight = (255, 255, 130)
    xpos = pos[0]
    ypos = pos[1]

    # Find Column
    col = 1
    xpos -= (side_width + border_width)
    while xpos > box_width:
        if col % 3 != 0:
            xpos -= (box_width + inner_line_width)
        else:
            xpos -= (box_width + border_width)
        col += 1
    if xpos < 0:
        col = 0

    # Find Row
    row = 1
    ypos -= (side_width + border_width)
    while ypos > box_width:
        if row % 3 != 0:
            ypos -= (box_width + inner_line_width)
        else:
            ypos -= (box_width + border_width)
        row += 1
    if ypos < 0:
        row = 0

    if (row != 0 and col != 0) and (row <= 9 and col <= 9):
        v_bords = (col - 1) // 3 + 1
        h_bords = (row - 1) // 3 + 1
        v_lines = col - v_bords
        h_lines = row - h_bords

        x = side_width + v_bords * border_width + v_lines * inner_line_width + (col - 1) * box_width
        y = side_width + h_bords * border_width + h_lines * inner_line_width + (row - 1) * box_width
        pygame.draw.rect(wn, highlight, (x, y, box_width, box_width))


def select():
    pos = pygame.mouse.get_pos()
    xpos = pos[0]
    ypos = pos[1]

    # Find Column
    col = 1
    xpos -= (side_width + border_width)
    while xpos > box_width:
        if col % 3 != 0:
            xpos -= (box_width + inner_line_width)
        else:
            xpos -= (box_width + border_width)
        col += 1
    if xpos < 0:
        col = 0

    # Find Row
    row = 1
    ypos -= (side_width + border_width)
    while ypos > box_width:
        if row % 3 != 0:
            ypos -= (box_width + inner_line_width)
        else:
            ypos -= (box_width + border_width)
        row += 1
    if ypos < 0:
        row = 0

    return [col, row]


def selection(selected):
    highlight = (255, 160, 160)
    row = selected[1]
    col = selected[0]

    if (row != 0 and col != 0) and (row <= 9 and col <= 9):
        v_bords = (col - 1) // 3 + 1
        h_bords = (row - 1) // 3 + 1
        v_lines = col - v_bords
        h_lines = row - h_bords

        x = side_width + v_bords * border_width + v_lines * inner_line_width + (col - 1) * box_width
        y = side_width + h_bords * border_width + h_lines * inner_line_width + (row - 1) * box_width
        pygame.draw.rect(wn, highlight, (x, y, box_width, box_width))


def draw_numbers():
    button_colour = (20, 20, 20)
    button_shade = (200, 200, 200)
    button_highlight = (255, 255, 130)
    button_side = 35
    button_gap = 25

    title_colour = (10, 10, 10)
    button_font = pygame.font.SysFont("Times New Roman", 35)

    pos = pygame.mouse.get_pos()

    for i in range(1, 10):

        pygame.draw.rect(wn, button_shade, (70 + i * (button_side + button_gap),
                                            screen_length - side_width // 2 - button_side // 2,
                                            button_side, button_side))

        if screen_length - side_width // 2 - button_side // 2 < pos[1] < screen_length - side_width//2 + button_side//2:
            if 70 + i * (button_side + button_gap) < pos[0] < 70 + i * (button_side + button_gap) + button_side:
                pygame.draw.rect(wn, button_highlight, (70 + i * (button_side + button_gap),
                                                    screen_length - side_width // 2 - button_side // 2,
                                                    button_side, button_side))

        pygame.draw.rect(wn, button_colour, (70 + i * (button_side + button_gap),
                                             screen_length - side_width // 2 - button_side // 2,
                                             button_side, button_side), 3)

        number = button_font.render(str(i), 1, title_colour)
        wn.blit(number, (78 + i * (button_side + button_gap), screen_length - side_width // 2 - button_side // 2 - 3))


def confirm(selected):
    pos = pygame.mouse.get_pos()
    number = (pos[0] - 70) // 60
    button_side = 35

    col = selected[0]
    row = selected[1]
    index = 9 * (row - 1) + col - 1

    if (row != 0 and col != 0) and (row <= 9 and col <= 9):
        if screen_length - side_width // 2 - button_side // 2 < pos[1] < screen_length - side_width//2 + button_side//2:
            if board[index] == 0:
                board[index] = number


def check_rows():
    for i in range(0, 9):
        row = []
        for j in range(0, 9):
            index = 9 * i + j
            number = board[index]
            if number > 9:
                number -= 9
            if number != 0:
                row.append(number)

        if len(row) != len(set(row)):
            if not auto_solving:
                end_game("row", i)
            else:
                return False

    return True


def check_columns():
    for i in range(0, 9):
        column = []
        for j in range(0, 9):
            index = 9 * j + i
            number = board[index]
            if number > 9:
                number -= 9
            if number != 0:
                column.append(number)

        if len(column) != len(set(column)):
            if not auto_solving:
                end_game("column", i)
            else:
                return False

    return True


def check_box():
    boxes = [[], [], [],
             [], [], [],
             [], [], []]

    for index in range(len(board)):
        number = board[index]
        if number > 9:
            number -= 9
        if number != 0:
            i = (index % 9) // 3
            j = index // 27
            box_num = (j * 3) + i
            if box_num > 8:
                break
            boxes[box_num].append(number)

    for box in boxes:
        if len(box) != len(set(box)):
            index = boxes.index(box)
            if not auto_solving:
                end_game("box", index)
            else:
                return False

    return True


def end_game(type, index):
    select_colour = (255, 200, 200)
    end_border_colour = (240, 10, 10)
    end_line_colour = (240, 30, 30)

    counter = 0
    speed = 300
    while True:
        pygame.display.update()
        wn.fill(bg_colour)
        counter += 1

        if counter > speed * 10:
            counter = 0

        # Box Failure
        if type == "box":
            i = index % 3
            j = index // 3
            big_box_width = 3 * box_width + 2 * inner_line_width
            pygame.draw.rect(wn, select_colour, (side_width + border_width + i * (big_box_width + border_width),
                                                 side_width + border_width + j * (big_box_width + border_width),
                                                 big_box_width, big_box_width))

        # Column Failure
        elif type == "column":
            v_bords = index // 3
            v_lines = index - v_bords
            pygame.draw.rect(wn, select_colour, (side_width + border_width * (v_bords + 1) + v_lines * inner_line_width
                                                 + index * box_width, side_width + border_width,
                                                 box_width, line_length - border_width))

        # Row Failure
        elif type == "row":
            h_bords = index // 3
            h_lines = index - h_bords
            pygame.draw.rect(wn, select_colour, (side_width + border_width, side_width + border_width * (h_bords + 1)
                                                 + h_lines * inner_line_width + index * box_width,
                                                line_length - border_width, box_width))

        switch = counter // speed
        if switch % 2 == 1:
            draw_board(end_border_colour, end_line_colour)
            title("You Failed")
        elif switch % 2 == 0:
            draw_board(border_colour, inner_line_colour)
            title("Sudoku")

        draw_numbers()
        update_numbers()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


def win():
    completed_section = []
    for number in board:
        if number != 0:
            completed_section.append(number)

    if len(completed_section) == len(board):
        win_border_colour = (10, 240, 10)
        win_line_colour = (30, 240, 30)

        counter = 0
        speed = 350
        while True:
            pygame.display.update()
            wn.fill(bg_colour)
            counter += 1

            if counter > speed * 10:
                counter = 0

            switch = counter // speed
            if switch % 2 == 1:
                draw_board(win_border_colour, win_line_colour)
                title("You Win")
            elif switch % 2 == 0:
                draw_board(border_colour, inner_line_colour)
                title("Sudoku")

            draw_numbers()
            update_numbers()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()


def auto_solve_1():
    global auto_solving, show
    index = 0
    auto_solving = True
    while index < len(board):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Solving

        if board[index] == 0:
            board[index] += 1
            update_numbers(index)

        if board[index] <= 9:
            rows = check_rows()
            columns = check_columns()
            box = check_box()

            if rows and columns and box:
                index += 1
            else:
                while not rows or not columns or not box:
                    if board[index] != 9:
                        board[index] += 1
                        update_numbers(index)
                        rows = check_rows()
                        columns = check_columns()
                        box = check_box()
                    else:
                        board[index] = 0
                        update_numbers(index)
                        index -= 1
                        while board[index] == 9:
                            board[index] = 0
                            update_numbers(index)
                            index -= 1
                        while board[index] > 9:
                            index -= 1

            # Unsolvable
            if index < 0:
                return False

        else:
            index += 1

    counter = 0
    speed = 350
    auto_solving = False
    solved_border_colour = (10, 10, 100)
    solved_line_colour = (15, 15, 120)
    if not testing:
        show = True
        while True:
            pygame.display.update()
            wn.fill(bg_colour)
            counter += 1

            if counter > speed * 10:
                counter = 0

            switch = counter // speed
            if switch % 2 == 1:
                draw_board(solved_border_colour, solved_line_colour)
                title("Solved")
            elif switch % 2 == 0:
                draw_board(border_colour, inner_line_colour)
                title("Sudoku")

            draw_numbers()
            update_numbers()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

    elif testing:
        return True


def highlighted(index):
    colour = (255, 255, 130)
    row = index // 9
    column = index % 9

    v_bords = column // 3 + 1
    v_lines = column - v_bords + 1
    h_bords = row // 3 + 1
    h_lines = row - h_bords + 1
    pygame.draw.rect(wn, colour, (side_width + v_bords * border_width + v_lines * inner_line_width + column * box_width,
                                  side_width + h_bords * border_width + h_lines * inner_line_width + row * box_width,
                                  box_width, box_width))


def create_new():
    global auto_solving, testing
    auto_solving = True
    solvable = False
    while not solvable:
        for index in range(len(board)):
            board[index] = 0

        difficulty = random.randint(5, 20)
        while difficulty > 0:
            slot = random.randint(0, len(board))
            if slot > len(board):
                slot -= 1
            while board[slot] != 0:
                slot = random.randint(0, len(board))
            board[slot] = random.randint(1, 9)
            grace = 10
            while not check_rows() or not check_columns() or not check_box():
                board[slot] = random.randint(1, 9)
                grace -= 1
                if grace == 0:
                    slot = random.randint(0, len(board))
                    while board[slot] != 0:
                        slot = random.randint(0, len(board))

            difficulty -= 1
        for number in board:
            if number != 0:
                index = board.index(number)
                number += 9
                board[index] = number
        testing = True
        solvable = auto_solve_1()

    for number in board:
        if number <= 9:
            index = board.index(number)
            board[index] = 0

    testing = False
    auto_solving = False


play()

