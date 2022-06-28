from Cube.cube import Cube


def __solve_cross(cube):
    color_to_norm = {'g': (2, -1), 'o': (0, -1), 'b': (2, 1), 'r': (0, 1)}
    res = ''
    edges = __get_yellow_edges(cube)
    b = 0
    for edge in edges:
        edgeInPlace = False
        neighbor = __get_neighbors(cube, edge)[0]
        i = 0
        if edge.point[1] == 0:
            while True:
                if edge.norm[2] == -1:
                    if edge.point[0] == 1:
                        cube.sequence('R U R`')
                        res += 'R U R` '

                    elif edge.point[0] == -1:
                        cube.sequence('L` U` L')
                        res += 'L` U` L '
                    for a in range(i):
                        cube.move('r')
                        res += 'mR '

                    for a in range(i):
                        cube.turn('U', 'l')
                        res += 'U` '

                    break
                else:
                    cube.move('l')
                    res += 'mL '
                    i += 1

        elif edge.norm[1] == -1:
            while True:
                if edge.point[2] == -1:
                    break
                else:
                    cube.turn('U', 'r')
                    res += 'U '

        elif edge.point[1] == -1:
            while True:
                if edge.norm[2] == -1:
                    cube.sequence('F R U` R` F` U2')
                    res += 'F R U` R` F` U2 '
                    break
                else:
                    cube.turn('U', 'r')
                    res += 'U '

        elif edge.norm[1] == 1:
            axis = color_to_norm[neighbor.color][0]
            value = color_to_norm[neighbor.color][1]
            if neighbor.norm[axis] == value:
                edgeInPlace = True
            else:
                i = 0
                while True:
                    if edge.point[2] == -1:
                        cube.sequence('F2')
                        res += 'F2 '
                        for a in range(i):
                            cube.turn('D', 'l')
                            res += 'D` '
                        break
                    else:
                        cube.turn('D', 'r')
                        res += 'D '
                        i += 1

        elif edge.point[1] == 1:
            i = 0
            while True:
                if edge.norm[2] == -1:
                    cube.sequence('F` R U` R` F U2')
                    res += 'F` R U` R` F U2 '
                    for a in range(i):
                        cube.turn('D', 'l')
                        res += 'D` '
                    break
                else:
                    cube.turn('D', 'r')
                    res += 'D '
                    i += 1

        if not edgeInPlace:
            edgeColor = neighbor.color

            colors_to_turns = {'g': 'F', 'o': 'L', 'b': 'B', 'r': 'R'}

            for a in range(tuple(colors_to_turns).index(edgeColor)):
                cube.turn('U', 'r')
                res += 'U '
            for a in range(2):
                cube.turn(colors_to_turns[edgeColor], 'r')
                res += colors_to_turns[edgeColor] + ' '
            b += 1

    return res


def __solve_corners(cube):
    res = ''
    color_to_norm = {'g': (2, -1),
                     'o': (0, -1),
                     'b': (2, 1),
                     'r': (0, 1)}

    norms = {'u': (0, -1, 0),
             'r': (1, 0, 0),
             'd': (0, 1, 0),
             'l': (-1, 0, 0),
             'b': (0, 0, 1),
             'f': (0, 0, -1)}
    corners = __get_yellow_corners(cube)
    solved = []
    for corner in corners:
        neighbors = __get_neighbors(cube, corner)
        if corner not in solved:
            if corner.norm == norms['d']:
                cornerSolved = True
                for i in range(2):
                    axis = color_to_norm[neighbors[i].color][0]
                    value = color_to_norm[neighbors[i].color][1]
                    if neighbors[i].norm[axis] != value:
                        cornerSolved = False
                if cornerSolved:
                    solved.append(corner)
                else:
                    i = 0
                    cornerSide = ''
                    on = True
                    while on:
                        if corner.point == (1, 1, -1):
                            on = False
                            cornerSide = 'r'
                        elif corner.point == (-1, 1, -1):
                            on = False
                            cornerSide = 'l'
                        else:
                            i += 1
                            cube.turn('D', 'r')
                            res += 'D '

                    if cornerSide == 'r':
                        cube.sequence('R U R`')
                        res += 'R U R` '
                    if cornerSide == 'l':
                        cube.sequence('L` U` L')
                        res += 'L` U` L '

                    for a in range(i):
                        cube.turn('D', 'l')
                        res += 'D` '

            if corner not in solved:
                if corner.norm == norms['u']:
                    cornerSide = ''
                    on = True
                    while on:
                        if corner.point == (1, -1, -1):
                            on = False
                            cornerSide = 'r'
                        elif corner.point == (-1, -1, -1):
                            on = False
                            cornerSide = 'l'
                        else:
                            cube.turn('U', 'r')
                            res += 'U '

                    howMuchToTurn = ['g', 'o', 'b', 'r']
                    neighbors = __get_neighbors(cube, corner)
                    sideNeighbor = None
                    for neighbor in neighbors:
                        if neighbor.norm == norms[cornerSide]:
                            sideNeighbor = neighbor

                    for i in range(howMuchToTurn.index(sideNeighbor.color)):
                        cube.turn('D', 'r')
                        res += 'D '
                    if cornerSide == 'r':
                        for i in range(3):
                            cube.sequence('U R U` R`')
                            res += 'U R U` R` '
                    elif cornerSide == 'l':
                        for i in range(3):
                            cube.sequence('U` L` U L')
                            res += 'U` L` U L '
                    for i in range(howMuchToTurn.index(sideNeighbor.color)):
                        cube.turn('D', 'l')
                        res += 'D` '
                    solved.append(corner)

                if corner not in solved:
                    if corner.point[1] == 1:
                        on = True
                        i = 0
                        while on:
                            if corner.norm == (0, 0, -1):
                                if corner.point == (1, 1, -1):
                                    on = False
                                    cube.sequence('F` U` F U')
                                    res += 'F` U` F U '
                                elif corner.point == (-1, 1, -1):
                                    on = False
                                    cube.sequence('F U F` U`')
                                    res += 'F U F` U` '
                            else:
                                cube.turn('D', 'r')
                                res += 'D '
                                i += 1
                        for a in range(i):
                            cube.turn('D', 'l')
                            res += 'D` '

                    cornerSide = ''
                    on = True
                    while on:
                        if corner.norm == (0, 0, -1):
                            if corner.point == (1, -1, -1):
                                on = False
                                cornerSide = 'r'
                            elif corner.point == (-1, -1, -1):
                                on = False
                                cornerSide = 'l'
                        else:
                            cube.turn('U', 'r')
                            res += 'U '

                    howMuchToTurn = ['g', 'o', 'b', 'r']
                    topNeighbor = None
                    for neighbor in neighbors:
                        if neighbor.norm == norms['u']:
                            topNeighbor = neighbor
                    for i in range(howMuchToTurn.index(topNeighbor.color)):
                        cube.turn('D', 'r')
                        res += 'D '
                    if cornerSide == 'r':
                        cube.sequence('U R U` R`')
                        res += 'U R U` R` '
                    elif cornerSide == 'l':
                        cube.sequence('U` L` U L')
                        res += 'U` L` U L '
                    for i in range(howMuchToTurn.index(topNeighbor.color)):
                        cube.turn('D', 'l')
                        res += 'D` '
                    solved.append(corner)

    return res


def __solve_second_layer(cube):
    color_to_norm = {'g': (2, -1), 'o': (0, -1), 'b': (2, 1), 'r': (0, 1)}
    res = ''
    edges = __get_all_edges(cube)
    newEdges = []
    for edge in edges:
        currentEdgeColors = [edge.color, __get_neighbors(cube, edge)[0].color]
        goodEdge = True
        if 'w' in currentEdgeColors or 'y' in currentEdgeColors:
            goodEdge = False
        if goodEdge:
            newEdges.append(edge)
    edges = newEdges

    for edge in edges:
        already_solved = True
        edge_n_neighbor = __get_neighbors(cube, edge)
        edge_n_neighbor.append(edge)
        for piece in edge_n_neighbor:
            axis = color_to_norm[piece.color][0]
            value = color_to_norm[piece.color][1]
            if piece.norm[axis] != value:
                already_solved = False

        if not already_solved:
            if edge.point[1] == 0:
                i = 0
                while True:
                    if edge.norm[2] == -1:
                        if edge.point[0] == 1:
                            cube.sequence("U R U` R` U` F` U F")
                            res += 'U R U` R` U` F` U F '
                        elif edge.point[0] == -1:
                            cube.sequence("U` L` U L U F U` F`")
                            res += 'U` L` U L U F U` F` '
                        for a in range(i):
                            cube.turn('M', 'l')
                            res += 'M` '
                        break
                    else:
                        cube.turn('M', 'r')
                        res += 'M '
                        i += 1

            if edge.point[1] == -1:
                while True:
                    if edge.point[2] == -1:
                        break
                    else:
                        cube.turn('U', 'r')
                        res += 'U '
                color1 = edge.color
                color2 = __get_neighbors(cube, edge)[0].color
                if edge.norm[1] == -1:
                    color2 = color1
                    color1 = __get_neighbors(cube, edge)[0].color

                # the tuples in the dict show the color that is in the right
                # and the color that is in the left
                colors_to_turns = {'g': ('r', 'o'),
                                   'o': ('g', 'b'),
                                   'b': ('o', 'r'),
                                   'r': ('b', 'g')}

                for i in range(tuple(colors_to_turns).index(color1)):
                    cube.move('l')
                    res += 'mL '
                    cube.turn('U', 'r')
                    res += 'U '

                side_to_alg = ('U R U` R` U` F` U F', 'U` L` U L U F U` F`')
                side = colors_to_turns[color1].index(color2)
                cube.sequence(side_to_alg[side])
                res += side_to_alg[side] + ' '
                for i in range(tuple(colors_to_turns).index(color1)):
                    cube.move('r')
                    res += 'mR '

                edges.remove(__get_neighbors(cube, edge)[0])

    return res


def __oll_step_2(cube):
    res = ''
    side = __get_side_corners_map(cube, 'U', 'w')

    no_corners = '# # \n' \
                 '# # \n'

    one_corner = '# # \n' \
                 'w # \n'

    close_corners = '# w \n' \
                    '# w \n'

    diagonal_corners = 'w # \n' \
                       '# w \n'

    solved = 'w w \n' \
             'w w \n'

    cases = [no_corners, one_corner, close_corners, diagonal_corners]

    while True:
        if side in cases:
            cube.sequence('R U R` U R U2 R`')
            res += 'R U R` U R U2 R` '
            side = __get_side_corners_map(cube, 'U', 'w')

        elif side == solved:
            return res

        else:
            cube.turn('U', 'r')
            res += 'U '
            side = __get_side_corners_map(cube, 'U', 'w')


def __oll_step_1(cube):
    res = ''
    side = __get_side_edges_map(cube, 'U', 'w')

    case1 = '# w # \n' \
            'w w # \n' \
            '# # # \n'

    case2 = '# # # \n' \
            'w w w \n' \
            '# # # \n'

    case3 = '# # # \n' \
            '# w # \n' \
            '# # # \n'

    solved = '# w # \n' \
             'w w w \n' \
             '# w # \n'

    cases = (case1, case2, case3)

    while True:
        if side in cases:
            cube.sequence("F R U R` U` F`")
            res += 'F R U R` U` F` '
            side = __get_side_edges_map(cube, 'U', 'w')
        elif side == solved:
            return res
        else:
            cube.turn('U', 'r')
            res += 'U '
            side = __get_side_edges_map(cube, 'U', 'w')


def __pll_step_1(cube):
    res = ''
    solvedCube = Cube()
    side = __get_side_corners(cube, 'L')
    didTPerm = False

    sides = ['U', 'L', 'F', 'R', 'B', 'D']
    for i in range(4):
        done = True
        for currentSide in sides:
            cubeSide = __get_side_corners(cube, currentSide)
            solvedSide = __get_side_corners(solvedCube, currentSide)
            if cubeSide != solvedSide:
                done = False
        if done:
            return res
        else:
            cube.turn('U', 'r')
            res += 'U '

    for a in range(4):
        isTperm = True
        i = 0
        for color in side:
            if i == 2:
                break
            if color != '\n' and color != ' ':
                i += 1
                if color != side[0]:
                    isTperm = False
                    break

        if isTperm:
            cube.sequence('R U R` U` R` F R2 U` R` U` R U R` F`')
            res += 'R U R` U` R` F R2 U` R` U` R U R` F` '
            didTPerm = True
            break
        else:
            cube.turn('U', 'r')
            res += 'U '
            side = __get_side_corners(cube, 'L')

    if not didTPerm:
        cube.sequence('F R U` R` U` R U R` F` R U R` U` R` F R F`')
        res += 'F R U` R` U` R U R` F` R U R` U` R` F R F` '

    while True:
        done = True
        for side in sides:
            cubeSide = __get_side_corners(cube, side)
            solvedSide = __get_side_corners(solvedCube, side)
            if cubeSide != solvedSide:
                done = False
        if done:
            return res
        else:
            cube.turn('U', 'r')
            res += 'U '


def __pll_step_2(cube):
    res = ''
    side = cube.get_side_in_matrix('B')
    solvedCube = Cube()

    for i in range(4):
        if str(cube) == str(solvedCube):
            return res
        else:
            cube.turn('U', 'r')
            res += 'U '

    while True:
        side = cube.get_side_in_matrix('B')
        for i in range(4):
            isOkToDoAlg = True
            for a in range(3):
                if side[0][a] != side[0][0]:
                    isOkToDoAlg = False
            if isOkToDoAlg:
                break
            else:
                cube.turn('U', 'r')
                res += 'U '
                side = cube.get_side_in_matrix('B')
        cube.sequence('R2 U R U R` U` R` U` R` U R`')
        res += 'R2 U R U R` U` R` U` R` U R` '
        for i in range(4):
            if str(cube) == str(solvedCube):
                return res
            else:
                cube.turn('U', 'r')
                res += 'U '


def __get_yellow_edges(cube):
    edges = []
    for cell in cube.cells:
        if cell.color == 'y':
            i = 0
            for point in cell.point:
                if point == 0:
                    i += 1
            if i == 1:
                edges.append(cell)

    return edges


def __get_all_edges(cube):
    edges = []
    for cell in cube.cells:
        i = 0
        for point in cell.point:
            if point == 0:
                i += 1
        if i == 1:
            edges.append(cell)

    return edges


def __get_all_corners(cube):
    corners = []
    for cell in cube.cells:
        if 0 not in cell.point:
            corners.append(cell)
    return corners


def __get_yellow_corners(cube):
    corners = []
    for cell in cube.cells:
        if cell.color == 'y':
            if 0 not in cell.point:
                corners.append(cell)
    return corners


def __get_neighbors(cube, cell):
    res = []
    for item in cube.cells:
        if item.point == cell.point and item != cell:
            res.append(item)
    return res


def __get_side_corners(cube, side):
    res = ''
    mat = cube.get_side_in_matrix(side)
    cords = [0, -1]
    for y in cords:
        for x in cords:
            res += mat[y][x]
            res += ' '
        res += '\n'
    return res


def __get_side_edges(cube, side):
    res = ''
    mat = cube.get_side_in_matrix(side)
    for y in range(3):
        for x in range(3):
            if x-1 == 0 or y-1 == 0:
                res += mat[y][x]
                res += ' '
            else:
                res += '#'
                res += ' '
        res += '\n'
    return res


def __get_side_corners_map(cube, side, color):
    res = ''
    mat = cube.get_side_in_matrix(side)
    cords = [0, -1]
    for y in cords:
        for x in cords:
            current = mat[y][x]
            if current != '\n' and current != ' ' and current != color:
                res += '# '
            else:
                res += mat[y][x]
                res += ' '
        res += '\n'
    return res


def __get_side_edges_map(cube, side, color):
    res = ''
    mat = cube.get_side_in_matrix(side)
    for y in range(3):
        for x in range(3):
            if (x - 1 == 0 or y - 1 == 0) and mat[y][x] == color:
                res += mat[y][x]
                res += ' '
            else:
                res += '#'
                res += ' '
        res += '\n'
    return res


def __optimize_sequence(sequence):
    res = ''
    sequence = sequence.split()
    i = 0
    while i <= len(sequence) - 1:
        repeat = 0
        iterator = 0
        isMove = False
        while True:
            if i + iterator <= len(sequence) - 1:
                if list(sequence[i])[0] == list(sequence[i + iterator])[0]:
                    if list(sequence[i])[0] == 'm':
                        isMove = True
                        break
                    if len(list(sequence[i + iterator])) == 2:
                        if list(sequence[i + iterator])[1] == '`':
                            repeat -= 1
                        elif list(sequence[i + iterator])[1] == '2':
                            repeat += 2
                    else:
                        repeat += 1
                    iterator += 1
                else:
                    break
            else:
                break
        if not isMove:
            if repeat >= 0:
                repeat = repeat % 4
            else:
                repeat = repeat % -4

            if repeat == 0:
                pass
            elif repeat == 1 or repeat == -3:
                res += list(sequence[i])[0] + ' '
            elif abs(repeat) == 2:
                res += list(sequence[i])[0] + '2 '
            elif repeat == 3 or repeat == -1:
                res += list(sequence[i])[0] + '` '

            i += iterator
        else:
            res += sequence[i] + ' '
            i += 1

    return res


def __solve_3x3(cube):
    colors = cube.get_cube_colors()
    res = ''
    solve_cross = __solve_cross(cube)
    solve_corners = __solve_corners(cube)
    solve_second_layer = __solve_second_layer(cube)
    oll_step_1 = __oll_step_1(cube)
    oll_step_2 = __oll_step_2(cube)
    pll_step_1 = __pll_step_1(cube)
    pll_step_2 = __pll_step_2(cube)
    # res += __solve_cross(cube)
    # res += __solve_corners(cube)
    # res += __solve_second_layer(cube)
    # res += __oll_step_1(cube)
    # res += __oll_step_2(cube)
    # res += __pll_step_1(cube)
    # res += __pll_step_2(cube)
    res = solve_cross + solve_corners + solve_second_layer + oll_step_1+ oll_step_2 + pll_step_1 + pll_step_2
    solve_cross = __optimize_sequence(solve_cross)
    solve_corners = __optimize_sequence(solve_corners)
    solve_second_layer = __optimize_sequence(solve_second_layer)
    oll_step_1= __optimize_sequence(oll_step_1)
    oll_step_2 = __optimize_sequence(oll_step_2)
    pll_step_1 = __optimize_sequence(pll_step_1)
    pll_step_2 = __optimize_sequence(pll_step_2)
    res = __optimize_sequence(res)
    cube.load_cube(colors)
    return solve_cross,solve_corners,solve_second_layer,oll_step_1,oll_step_2,pll_step_1,pll_step_2,res


def __solve_2x2(cube):
    colors = cube.get_cube_colors()
    res = ''
    res += __solve_corners(cube)
    res += __oll_step_2(cube)
    res += __pll_step_1(cube)
    cube.load_cube(colors)
    return __optimize_sequence(res)

