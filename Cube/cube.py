import random
from Cube.cell import Cell


class _rotator:
    def __init__(self):
        # first number in the tuple means which axis in the order:
        # {0:'x', 1:'y', 2:'z'}
        # second number in the tuple means what to multiply that axis by
        self.magical_rotator = [
            [  # Up
                [(2, 1), (1, 1), (0, -1)],
                [(2, -1), (1, 1), (0, 1)]
            ],
            [  # Left
                [(0, 1), (2, -1), (1, 1)],
                [(0, 1), (2, 1), (1, -1)]
            ],
            [  # Front
                [(1, -1), (0, 1), (2, 1)],
                [(1, 1), (0, -1), (2, 1)]
            ],
            [  # Right
                [(0, 1), (2, 1), (1, -1)],
                [(0, 1), (2, -1), (1, 1)]
            ],
            [  # Back
                [(1, 1), (0, -1), (2, 1)],
                [(1, -1), (0, 1), (2, 1)]
            ],
            [  # Down
                [(2, -1), (1, 1), (0, 1)],
                [(2, 1), (1, 1), (0, -1)]
            ]]

    def get_rotator(self, move, direction):
        moveInt = 0
        directions = {'r': 0, 'l': 1}
        moves = ['U', 'L', 'F', 'R', 'B', 'D']
        for m in moves:
            if m == move:
                moveInt = moves.index(m)
        return self.magical_rotator[moveInt][directions[direction]]

    def rotate(self, cords, move, direction):
        rotator = self.get_rotator(move, direction)
        res = []
        for operation in rotator:
            res.append(cords[operation[0]] * operation[1])
        return tuple(res)


def reshape(mat, dim):
    res = []
    if isinstance(mat[0], list):
        for y in range(len(mat)):
            for x in range(len(mat[y])):
                res.append(mat[y][x])
    else:
        for y in range(dim[0]):
            res.append([])
            for x in range(dim[1]):
                res[y].append(mat[y * (dim[0]) + x])
    return res


def mirror(mat, axis=1):
    if axis == 1:
        for y in range(len(mat)):
            temp = (mat[y][0])
            mat[y][0] = mat[y][-1]
            mat[y][-1] = temp
    if axis == 0:
        for x in range(len(mat[0])):
            temp = (mat[0][x])
            mat[0][x] = mat[-1][x]
            mat[-1][x] = temp


class Cube:
    def __init__(self, scramble=None):
        self.rotator = _rotator()
        self.cells = []
        self.dim = (3, 3)
        self.positionNums = []
        self.__build_cube(scramble)
        self.colorToNorm = {'U': (0, -1, 0),
                            'L': (-1, 0, 0),
                            'F': (0, 0, -1),
                            'R': (1, 0, 0),
                            'B': (0, 0, 1),
                            'D': (0, 1, 0)}

    def __build_cube(self, scramble=None):
        if scramble == None:
            scramble = self.__get_solved_scramble()
        sideSize = self.dim[0] * self.dim[1]
        scramble = list(scramble)

        self.positionsNums = []

        if sideSize % 2 == 0:
            nums = range(int(self.dim[0] / 2))
            for i in nums:
                self.positionsNums.append(-i - 1)
            self.positionsNums.reverse()

            for i in nums:
                self.positionsNums.append(i + 1)
        else:
            nums = range(int((self.dim[0] - 1) / 2))
            for i in nums:
                self.positionsNums.append(-i - 1)
            self.positionsNums.reverse()
            self.positionsNums.append(0)
            for i in nums:
                self.positionsNums.append(i + 1)

        i = 0
        # top
        for z in self.positionsNums:
            z = z*-1
            for x in self.positionsNums:
                self.cells.append(
                    Cell(
                        point=(x, -1, z),
                        norm=(0, -1, 0),
                        color=scramble[i]))
                i += 1
        # left
        for y in self.positionsNums:
            for z in self.positionsNums:
                z = z*-1
                self.cells.append(
                    Cell(point=(-1, y, z),
                         norm=(-1, 0, 0),
                         color=scramble[i]))
                i += 1
        # front
        for y in self.positionsNums:
            for x in self.positionsNums:
                self.cells.append(
                    Cell(point=(x, y, -1),
                         norm=(0, 0, -1),
                         color=scramble[i]))
                i += 1
        # right
        for y in self.positionsNums:
            for z in self.positionsNums:
                self.cells.append(
                    Cell(point=(1, y, z),
                         norm=(1, 0, 0),
                         color=scramble[i]))
                i += 1
        # back
        for y in self.positionsNums:
            for x in self.positionsNums:
                x = x*-1
                self.cells.append(
                    Cell(point=(x, y, 1),
                         norm=(0, 0, 1),
                         color=scramble[i]))
                i += 1

        # bottom
        for z in self.positionsNums:
            for x in self.positionsNums:
                self.cells.append(
                    Cell(point=(x, 1, z),
                         norm=(0, 1, 0),
                         color=scramble[i]))
                i += 1

    def load_cube(self, colors):
        self.cells = []
        self.positionsNums = []
        self.__build_cube(colors)

    def __get_side(self, side):
        res = []
        temp = []
        for cell in self.cells:
            if cell.norm == self.colorToNorm[side]:
                temp.append(cell)

        for a in self.positionsNums:
            for b in self.positionsNums:
                point = []
                for i in range(3):
                    if self.colorToNorm[side][i] == 0:
                        if i == 0:
                            point.append(b)
                        elif i == 1:
                            point.append(a)
                        elif i == 2:
                            if self.colorToNorm[side][0] == 0:
                                point.append(a)
                            else:
                                point.append(b)
                    else:
                        point.append(self.colorToNorm[side][i])
                for cell in temp:
                    if cell.point == tuple(point):
                        res.append(cell)
        return res

    def load_scramble(self, scramble):
        scramble = list(scramble)
        sides = ['U', 'L', 'F', 'R', 'B', 'D']
        for side in sides:
            finished_sides = 0
            side_size = self.dim[0] * self.dim[1]
            # get the current side
            start = side_size * finished_sides
            end = side_size * finished_sides + side_size
            current_side_in_scramble = scramble[start:end]
            cells = self.__get_side(side)
            if side in ('B', 'U', 'L'):
                i = 1
                if side == 'U':
                    i = 0
                cells = reshape(cells, (self.dim[0], self.dim[1]))
                mirror(cells, i)
                cells = reshape(cells, (1, self.dim[0] * self.dim[1]))

            i = 0
            for cell in cells:
                cell.color = current_side_in_scramble[i]
                i += 1

    def get_side_in_matrix(self, side):
        res = []
        cells = self.__get_side(side)
        if side in ('B', 'U', 'L'):
            i = 1
            if side == 'U':
                i = 0
            cells = reshape(cells, (self.dim[0], self.dim[1]))
            mirror(cells, i)
            cells = reshape(cells, (1, self.dim[0] * self.dim[1]))
        colors = []
        for cell in cells:
            colors.append(cell.color)
        res = colors
        res = reshape(res, (self.dim[0], self.dim[1]))

        return res

    def get_cube_colors(self):
        res = ''
        sides = ['U', 'L', 'F', 'R', 'B', 'D']
        for side in sides:
            cells = self.__get_side(side)
            if side in ('B', 'U', 'L'):
                i = 1
                if side == 'U':
                    i = 0
                cells = reshape(cells, (self.dim[0], self.dim[1]))
                mirror(cells, i)
                cells = reshape(cells, (1, self.dim[0] * self.dim[1]))
            colors = []
            for cell in cells:
                colors.append(cell.color)
            i = 0
            for a in range(self.dim[0]):
                for b in range(self.dim[1]):
                    res += colors[i]
                    i += 1
        return res

    def __get_solved_scramble(self):
        res = ''
        sides = ['w', 'o', 'g', 'r', 'b', 'y']
        sideSize = self.dim[0] * self.dim[1]
        for side in sides:
            for i in range(sideSize):
                res += side
        return res

    def move(self, direction):
        opposite = {'r': 'l', 'l': 'r'}
        self.turn('U', direction)
        self.turn('M', direction)
        self.turn('D', opposite[direction])

    def turn(self, side, direction):
        cells = []
        # smallest coordinates possible
        negative = self.positionsNums[0]
        # biggest coordinates possible
        positive = self.positionsNums[-1]
        mid = 0
        # the first number in the tuple means
        # which axis on the coordinates are we going to compare
        sidesPoint = {'U': (1, negative),
                      'L': (0, negative),
                      'F': (2, negative),
                      'R': (0, positive),
                      'B': (2, positive),
                      'D': (1, positive),
                      'M': (1, mid)}

        for cell in self.cells:
            if cell.point[sidesPoint[side][0]] == sidesPoint[side][1]:
                cells.append(cell)

        sideCells = []
        if side != 'M':
            sideCells = self.__get_side(side)
        beltCells = []
        for cell in cells:
            if cell not in sideCells:
                beltCells.append(cell)

        if side == 'M':
            if self.dim != (3, 3):
                return
            for cell in cells:
                if cell in beltCells:
                    point = cell.point
                    norm = cell.norm
                    cell.point = self.rotator.rotate(point, side, direction)
                    cell.norm = self.rotator.rotate(norm, side, direction)
            return

        for cell in cells:
            cell.point = self.rotator.rotate(cell.point, side, direction)
            if cell in beltCells:
                cell.norm = self.rotator.rotate(cell.norm, side, direction)

    def sequence(self, sequence):
        """
        run a sequence of moves on the cube
        :param sequence:
        :return: void
        """
        moved = False
        sequence = sequence.split()
        for move in sequence:
            move = list(move)
            direction = 'r'
            if "`" in move:
                direction = 'l'

            elif "2" in move:
                for i in range(2):
                    if "W" in move:
                        pass
                        # W moves are not fully done yet
                    else:
                        self.turn(move[0], direction)
                        moved = True

            elif "W" in move:
                pass
                # W moves are not fully done yet

            if not moved:
                if move[0] == 'm':
                    self.move(move[1].lower())
                else:
                    self.turn(move[0], direction)
            else:
                moved = False

    def scramble(self, size=20):
        sides = ['U', 'L', 'F', 'R', 'B', 'D']
        lastAddedMove = ''
        scramble = ''
        for i in range(size):
            while True:
                addedMove = random.choice(sides)
                if addedMove != lastAddedMove:
                    break
            lastAddedMove = addedMove
            rand = random.randint(1, 5)
            if rand in (1, 2):
                pass
            elif rand in (3, 4):
                addedMove += '`'
            else:
                addedMove += '2'
            scramble += addedMove + ' '
        self.sequence(scramble)
        return scramble

    def __str__(self):
        res = ''
        sides = ['U', 'L', 'F', 'R', 'B', 'D']
        for side in sides:
            cells = self.__get_side(side)
            if side in ('B', 'U', 'L'):
                i = 1
                if side == 'U':
                    i = 0
                cells = reshape(cells, (self.dim[0], self.dim[1]))
                mirror(cells, i)
                cells = reshape(cells, (1, self.dim[0] * self.dim[1]))
            colors = []
            for cell in cells:
                colors.append(cell.color)
            i = 0
            for a in range(self.dim[0]):
                for b in range(self.dim[1]):
                    res += colors[i]
                    res += " "
                    i += 1
                res += '\n'
            res += '\n'
        return res
