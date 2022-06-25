from tkinter import W

from cv2 import split
from Cube.cube import Cube
# from Cube.Solver import kociemba
from Cube.Solver.beginners import solver
from Cube.Solver import beginners
import time
import math

def ChangeForm(cube2D):
    up = ''
    front =''
    right = ''
    back = ''
    left = ''
    down = ''
    for color in cube2D.up_face:
        if color == 1:
            up += 'w'
        elif color == 2:
            up += 'g'
        elif color == 3:
            up += 'r'
        elif color == 4:
            up += 'b'
        elif color == 5:
            up += 'o'
        elif color == 6:
            up += 'y'
    
    for color in cube2D.front_face:
        if color == 1:
            front += 'w'
        elif color == 2:
            front += 'g'
        elif color == 3:
            front += 'r'
        elif color == 4:
            front += 'b'
        elif color == 5:
            front += 'o'
        elif color == 6:
            front += 'y'

    for color in cube2D.right_face:
        if color == 1:
            right += 'w'
        elif color == 2:
            right += 'g'
        elif color == 3:
            right += 'r'
        elif color == 4:
            right += 'b'
        elif color == 5:
            right += 'o'
        elif color == 6:
            right += 'y'

    for color in cube2D.back_face:
        if color == 1:
            back += 'w'
        elif color == 2:
            back += 'g'
        elif color == 3:
            back += 'r'
        elif color == 4:
            back += 'b'
        elif color == 5:
            back += 'o'
        elif color == 6:
            back += 'y'

    for color in cube2D.left_face:
        if color == 1:
            left += 'w'
        elif color == 2:
            left += 'g'
        elif color == 3:
            left += 'r'
        elif color == 4:
            left += 'b'
        elif color == 5:
            left += 'o'
        elif color == 6:
            left += 'y'

    for color in cube2D.down_face:
        if color == 1:
            down += 'w'
        elif color == 2:
            down += 'g'
        elif color == 3:
            down += 'r'
        elif color == 4:
            down += 'b'
        elif color == 5:
            down += 'o'
        elif color == 6:
            down += 'y'
    
    CubeString = [up,left,front,right,back,down]
    BeginnerCube = Cube(''.join(CubeString))
    # print(cube)
    # solution = beginners.solve(cube)
    # cube.sequence(solution)
    # end = time.time()
    # print('Done!')
    # print(f'solution: {solution}')
    return BeginnerCube

def solveCube_BeginnerSolver(cube):
    BeginnerCube = ChangeForm(cube)
    solve_cross,solve_corners,solve_second_layer,oll_step_1,oll_step_2,pll_step_1,pll_step_2,res = solver.__solve_3x3(BeginnerCube)
    BeginnerCube.sequence(res)
    solve_cross = str.split(solve_cross)
    solve_corners = str.split(solve_corners)
    solve_second_layer = str.split(solve_second_layer)
    oll_step_1 = str.split(oll_step_1)
    oll_step_2 = str.split(oll_step_2)
    pll_step_1 = str.split(pll_step_1)
    pll_step_2 = str.split(pll_step_2)
    solution = str.split(res)
    return solve_cross,solve_corners,solve_second_layer,oll_step_1,oll_step_2,pll_step_1,pll_step_2,res,solution
    # print(f'solution: {res}')
