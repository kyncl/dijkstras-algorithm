import pygame
import sys
from tkinter import messagebox

import time
import tracemalloc

winWidth = 600
winHeight = 600
window = pygame.display.set_mode((winWidth, winHeight))

rows = 25
colums = 25

boxWidth = winWidth // rows
boxHeight = winHeight // colums

grid = []
queue = []
path = []

testNumber = 0

class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j

        self.start = False
        self.wall = False
        self.end = False
        self.selected = False

        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None

    def draw(self, win, color):
        pygame.draw.rect(
            win,
            color,
            (self.x * boxWidth, self.y * boxHeight, boxWidth - 2, boxHeight - 2),
        )

    def setNeighbours(self):
        # horizontal neighbours
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < colums - 1:
            self.neighbours.append(grid[self.x + 1][self.y])

        # vertical neighbours
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


def dijkstraAlgorithm(targetBox):
    srch = True
    # take the first box and remove it from arr
    currentBox = queue.pop(0)
    # to prevent to getting in queue arr
    currentBox.visited = True

    if currentBox == targetBox:
        while currentBox.prior != startBox:
            path.append(currentBox.prior)
            currentBox = currentBox.prior
        srch = False

    else:
        srch = True
        for neighbour in currentBox.neighbours:
            if neighbour.queued == False and neighbour.wall == False:
                neighbour.queued = True
                neighbour.prior = currentBox
                queue.append(neighbour)
    return srch


def placePoint(grid, isWall=True, specificBox=None):
    if specificBox == None:
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]

        if x > 0 and y > 0 and x < winWidth and y < winHeight:
            i = x // boxWidth
            j = y // boxHeight

            if isWall == True:
                if grid[i][j] != startBox and grid[i][j].end == False:
                    grid[i][j].wall = True
            else:
                if grid[i][j] != startBox and grid[i][j].wall == False:
                    grid[i][j].end = True
                    return grid[i][j]
    else:
        if isWall == True:
            if specificBox.start == False and specificBox.end == False:
                if specificBox.wall == True:
                    specificBox.wall = False
                else:
                    specificBox.wall = True
        else:
            if specificBox.start == False and specificBox.wall == False:
                if specificBox.end == True:
                    specificBox.end = False
                else:
                    specificBox.end = True
                    return specificBox


def Main():
    global grid
    global queue
    global path
    global startBox

    global testNumber

    searching = True
    beginAlgo = False
    targetBoxSet = False
    targetBox = None

    posSelectedBox = [0, 0]
    previousSelectedBox = None

    again = False
    gameLoop = True

    start = 0

    while gameLoop == True:
        for event in pygame.event.get():
            # for quiting script
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # controls

            # mouse
            elif event.type == pygame.MOUSEMOTION and beginAlgo == False:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                i = x // boxWidth
                j = y // boxHeight
                if previousSelectedBox != None:
                    previousSelectedBox.selected = False
                    posSelectedBox[0] = i
                    posSelectedBox[1] = j
                grid[i][j].selected = True
                previousSelectedBox = grid[i][j]

                if x > 0 and y > 0 and x < winWidth and y < winHeight:
                    # event.buttons[0] = clicked on left mouse button
                    if event.buttons[0]:
                        placePoint(grid)

                    # event.buttons[2] = clicked on right mouse button
                    elif (
                            event.buttons[2]
                            and targetBoxSet == False
                            and grid[i][j].wall == False
                    ):
                        targetBox = placePoint(grid, False)
                        targetBoxSet = True

            # keyboard
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if previousSelectedBox != None:
                        placePoint(grid, True, previousSelectedBox)
                    else:
                        placePoint(grid)

                elif event.key == pygame.K_x and targetBoxSet == False:
                    if previousSelectedBox != None:
                        targetBox = placePoint(
                            grid, False, previousSelectedBox)
                        if targetBox != None:
                            targetBoxSet = True
                    elif targetBoxSet == False:
                        targetBox = placePoint(grid, False)
                        targetBoxSet = True

                elif event.key == pygame.K_SPACE and targetBoxSet == True:
                    beginAlgo = True

                if event.key == pygame.K_RIGHT or event.key == pygame.K_l:
                    if posSelectedBox[0] < colums - 1:
                        posSelectedBox[0] += 1
                    else:
                        posSelectedBox[0] = 0
                elif event.key == pygame.K_LEFT or event.key == pygame.K_h:
                    if posSelectedBox[0] <= (-1) * (colums - 1):
                        posSelectedBox[0] = 0
                    else:
                        posSelectedBox[0] -= 1

                if event.key == pygame.K_DOWN or event.key == pygame.K_j:
                    if posSelectedBox[1] < rows - 1:
                        posSelectedBox[1] += 1
                    else:
                        posSelectedBox[1] = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_k:
                    if posSelectedBox[1] <= (-1) * (rows - 1):
                        posSelectedBox[1] = 0
                    else:
                        posSelectedBox[1] -= 1

                if previousSelectedBox != None:
                    previousSelectedBox.selected = False
                grid[posSelectedBox[0]][posSelectedBox[1]].selected = True
                previousSelectedBox = grid[posSelectedBox[0]
                ][posSelectedBox[1]]
                break

        # the algorithm
        if beginAlgo == True:
            if len(queue) > 0 and searching == True:
                if start == 0:
                    start = time.time()
                    tracemalloc.start()
                    testNumber += 1
                searching = dijkstraAlgorithm(targetBox)

            elif searching == False:
                print(f"{testNumber}) Time: {time.time() - start}s RAM Used: {tracemalloc.get_traced_memory()}KiB")
                tracemalloc.stop()

                # The output is given in form of (current, peak),i.e, current memory is the memory the code is currently
                # using and peak memory is the maximum space the program used while executing.

                end = messagebox.askyesno(
                    "found target!",
                    "target was found!\ndo you want to continue or end the program?",
                )
                if end == True:
                    gameLoop = False
                    again = True
                else:
                    pygame.quit()
                    sys.exit()

            else:
                if searching == True:
                    searching = False
                    # Tk().wm_withdraw()
                    end = messagebox.askyesno(
                        "no solution",
                        "there is no way to point"
                        "\ndo you want to continue or end the program?",
                    )
                    if end == True:
                        gameLoop = False
                        again = True
                    else:
                        pygame.quit()
                        sys.exit()

        window.fill((0, 0, 0))

        # color of boxes
        for i in range(colums):
            for j in range(rows):
                grid[i][j].draw(window, (20, 20, 20))

                if grid[i][j].queued == True:
                    grid[i][j].draw(window, (200, 200, 0))
                if grid[i][j].visited == True:
                    grid[i][j].draw(window, (0, 200, 200))
                if grid[i][j].selected == True:
                    grid[i][j].draw(window, (255, 255, 255))

                if grid[i][j] in path:
                    grid[i][j].draw(window, (0, 0, 200))

                if grid[i][j].start == True:
                    grid[i][j].draw(window, (20, 240, 20))
                if grid[i][j].wall == True:
                    if grid[i][j].selected == True:
                        grid[i][j].draw(window, (150, 150, 150))
                    else:
                        grid[i][j].draw(window, (90, 90, 90))
                if grid[i][j].end == True:
                    if grid[i][j].selected == True:
                        grid[i][j].draw(window, (255, 30, 20))
                    else:
                        grid[i][j].draw(window, (240, 20, 20))
        pygame.display.flip()
    else:
        if again == True:
            grid = []
            queue = []
            path = []
            # create grid
            for i in range(colums):
                arr = []
                for j in range(rows):
                    arr.append(Box(i, j))
                grid.append(arr)

            # create neighbours
            for i in range(colums):
                for j in range(rows):
                    grid[i][j].setNeighbours()

            startBox = grid[0][0]
            startBox.start = True
            startBox.visited = True

            queue.append(startBox)

            Main()


if __name__ == "__main__":
    # create grid
    for i in range(colums):
        arr = []
        for j in range(rows):
            arr.append(Box(i, j))
        grid.append(arr)

    # create neighbours
    for i in range(colums):
        for j in range(rows):
            grid[i][j].setNeighbours()

    startBox = grid[0][0]

    startBox.start = True
    startBox.visited = True

    queue.append(startBox)

    messagebox.showinfo(
        "Controls",
        "moving with mouse or arrows or vim like movement\nleft mouse on box or z = create wall \nright mouse on box or x = create target position\nspacebar = start algorithm",
    )

    Main()
