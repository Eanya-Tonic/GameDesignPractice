from turtle import st
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from quat import *
from geometry import *
import Cube2D
import numpy as np


def Direction(Step, theta):
    if Step == "F" or Step == "R" or Step == "B'" or Step == "B`" or Step == "L'" or Step == "L`" or Step == "R" or Step == "U" or Step == "D'" or Step == "D`":
        sys.stdout.write(Step)
        theta *= -1
    elif Step == "F'" or Step == "F`" or Step == "B" or Step == "L" or Step == "R'" or Step == "R`" or Step == "U'" or Step == "U`" or Step == "D":
        sys.stdout.write(Step)
        theta *= 1
    elif Step == "F2" or Step == "B2" or Step == "L2" or Step == "R2" or Step == "U2" or Step == "D2":
        sys.stdout.write(Step)
        theta *= 2
    return theta


def draw_Step(Step, Move_Flag, theta):
    # print("rotating")
    if Step == "F" or Step == "F'" or Step == "F2" or Step == "F`":
        for i in range(8):
            center_pieces[1][i] = z_rot(center_pieces[1][i], theta)
        for axis in edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[2] < 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = z_rot(piece[i], theta)
        for piece in corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[2] < 0:
                    flag = False
                    break
            if flag:
                for i in range(8):
                    piece[i] = z_rot(piece[i], theta)

    if Step == "L" or Step == "L'" or Step == "L2" or Step == "L`":
        for i in range(8):
            center_pieces[4][i] = x_rot(center_pieces[4][i], theta)

        for axis in edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[0] > 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = x_rot(piece[i], theta)
        for piece in corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[0] > 0:
                    flag = False
                    break
            if flag:
                for i in range(8):
                    piece[i] = x_rot(piece[i], theta)

    if Step == "B" or Step == "B'" or Step == "B2" or Step == "B`":
        for i in range(8):
            center_pieces[3][i] = z_rot(center_pieces[3][i], theta)

        for axis in edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[2] > 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = z_rot(piece[i], theta)
        for piece in corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[2] > 0:
                    flag = False
                    break
            if flag:
                for i in range(8):
                    piece[i] = z_rot(piece[i], theta)

    if Step == "R" or Step == "R'" or Step == "R2" or Step == "R`":
        for i in range(8):
            center_pieces[2][i] = x_rot(center_pieces[2][i], theta)

        for axis in edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[0] < 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = x_rot(piece[i], theta)
        for piece in corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[0] < 0:
                    flag = False
                    break
            if flag:
                for i in range(8):
                    piece[i] = x_rot(piece[i], theta)

    if Step == "U" or Step == "U'" or Step == "U2" or Step == "U`":
        for i in range(8):
            center_pieces[0][i] = y_rot(center_pieces[0][i], theta)

        for axis in edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[1] < 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = y_rot(piece[i], theta)
        for piece in corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[1] < 0:
                    flag = False
                    break
            if flag:
                for i in range(8):
                    piece[i] = y_rot(piece[i], theta)

    if Step == "D" or Step == "D'" or Step == "D2" or Step == "D`":
        for i in range(8):
            center_pieces[5][i] = y_rot(center_pieces[5][i], theta)

        for axis in edge_pieces:
            for piece in axis:
                flag = True
                for vertex in piece:
                    if vertex[1] > 0:
                        flag = False
                        break
                if flag:
                    for i in range(8):
                        piece[i] = y_rot(piece[i], theta)
        for piece in corner_pieces:
            flag = True
            for vertex in piece:
                if vertex[1] > 0:
                    flag = False
                    break
            if flag:
                for i in range(8):
                    piece[i] = y_rot(piece[i], theta)
    Move_Flag = False
    return Move_Flag


def draw_cube(cube2D):
    glLineWidth(GLfloat(6.0))
    glBegin(GL_LINES)
    # glColor3fv((1.0, 1.0, 1.0))
    # glColor3fv((0.5, 0.5, 0.5))
    glColor3fv((0.0, 0.0, 0.0))

    for axis in edge_pieces:
        for piece in axis:
            for edge in cube_edges:
                for vertex in edge:
                    glVertex3fv(piece[vertex])
    for piece in center_pieces:
        for edge in cube_edges:
            for vertex in edge:
                glVertex3fv(piece[vertex])
    for piece in corner_pieces:
        for edge in cube_edges:
            for vertex in edge:
                glVertex3fv(piece[vertex])
    glEnd()
    draw_stickers(cube2D)


def draw_stickers(cube2D):
    Center_Color, EdgeColor, CornerColor = cube2Dt3D(cube2D)
    glBegin(GL_QUADS)

    # 绘制中心块
    i = 0
    for color, surface in zip(Center_Color, cube_surfaces):
        glColor3fv(Num2Color(color))
        for vertex in surface:
            glVertex3fv(center_pieces[i][vertex])
        i += 1

    # 中心块黑色内衬
    for color, surface in zip(cube_colors, cube_surfaces):
        j = 0
        for piece in center_pieces:
            glColor3fv((0, 0, 0))
            for vertex in surface:
                glVertex3fv(center_pieces[j][vertex])
            j += 1

    # 绘制棱块
    i = 0
    j = 0
    for surface, face in zip(cube_surfaces, edges):
        for piece in face:
            color = Num2Color(EdgeColor[i][j])
            glColor3fv(color)
            for vertex in surface:
                glVertex3fv(edge_pieces[piece[0]][piece[1]][vertex])
            j += 1
        j = 0
        i += 1

    # # 棱块黑色内衬
    edge_black_pat = [
        [0, 1, 2, 3, 4, 5],
        [0, 1, 2, 3, 4, 5],
        [0, 1, 2, 3, 4, 5]
    ]

    glColor3fv((0, 0, 0))

    for i in range(len(edge_black_pat)):
        for face in edge_black_pat[i]:
            for piece in edge_pieces[i]:
                for vertex in cube_surfaces[face]:
                    glVertex3fv(piece[vertex])

    # 绘制角块
    corner_color_pat = [
        [1, 4, 5],  # 0
        [0, 1, 4],  # 1
        [0, 1, 2],  # 2
        [1, 2, 5],  # 3
        [3, 4, 5],  # 4
        [0, 3, 4],  # 5
        [0, 2, 3],  # 6
        [2, 3, 5],  # 7
    ]

    i = 0
    j = 0
    for i in range(len(corner_color_pat)):
        for face in corner_color_pat[i]:
            color = Num2Color(CornerColor[i][j])
            glColor3fv(color)
            for vertex in cube_surfaces[face]:
                glVertex3fv(corner_pieces[i][vertex])
            j += 1
        j = 0

    # #角块黑色内衬
    corner_black_pat = [
        [0, 2, 3],  # 0
        [2, 3, 5],  # 1
        [3, 4, 5],  # 2
        [0, 3, 4],  # 3
        [0, 1, 2],  # 4
        [1, 2, 5],  # 5
        [1, 4, 5],  # 6
        [0, 1, 4],  # 7
    ]
    for i in range(len(corner_color_pat)):
        glColor3fv((0, 0, 0))
        for i in range(len(corner_black_pat)):
            for face in corner_black_pat[i]:
                for vertex in cube_surfaces[face]:
                    glVertex3fv(corner_pieces[i][vertex])
    glEnd()
    draw_axis()


def draw_axis():
    glLineWidth(GLfloat(1.0))
    glBegin(GL_LINES)

    for color, axis in zip(axis_colors, axes):
        glColor3fv(color)
        for point in axis:
            glVertex3fv(axis_verts[point])
    glEnd()


def cube2Dt3D(cube2D):
    # 中心块
    UP_Center = cube2D.mu
    FRONT_Center = cube2D.mf
    RIGHT_Center = cube2D.mr
    BACK_Center = cube2D.mb
    LEFT_Center = cube2D.ml
    DOWN_Center = cube2D.md

    Center_Colors = [UP_Center,
                     FRONT_Center,
                     RIGHT_Center,
                     BACK_Center,
                     LEFT_Center,
                     DOWN_Center
                     ]

    # 棱块
    UP_Edges = [cube2D.up_face[7],
                cube2D.up_face[1],
                cube2D.up_face[3],
                cube2D.up_face[5]]

    FRONT_Edges = [cube2D.front_face[7],
                   cube2D.front_face[1],
                   cube2D.front_face[3],
                   cube2D.front_face[5]]

    RIGHT_Edges = [cube2D.right_face[5],
                   cube2D.right_face[3],
                   cube2D.right_face[1],
                   cube2D.right_face[7]]

    BACK_Edges = [cube2D.back_face[1],
                  cube2D.back_face[7],
                  cube2D.back_face[5],
                  cube2D.back_face[3]]

    LEFT_Edges = [cube2D.left_face[5],
                  cube2D.left_face[3],
                  cube2D.left_face[7],
                  cube2D.left_face[1]]

    DOWN_Edges = [cube2D.down_face[1],
                  cube2D.down_face[7],
                  cube2D.down_face[3],
                  cube2D.down_face[5]]

    Edges_Colors = [UP_Edges,
                    FRONT_Edges,
                    RIGHT_Edges,
                    BACK_Edges,
                    LEFT_Edges,
                    DOWN_Edges
                    ]

    Corner_Colors_0 = [cube2D.front_face[6],
                       cube2D.left_face[8],
                       cube2D.down_face[0]
                       ]

    Corner_Colors_1 = [cube2D.up_face[6],
                       cube2D.front_face[0],
                       cube2D.left_face[2]
                       ]

    Corner_Colors_2 = [cube2D.up_face[8],
                       cube2D.front_face[2],
                       cube2D.right_face[0]]

    Corner_Colors_3 = [cube2D.front_face[8],
                       cube2D.right_face[6],
                       cube2D.down_face[2]]

    Corner_Colors_4 = [cube2D.back_face[8],
                       cube2D.left_face[6],
                       cube2D.down_face[6]]

    Corner_Colors_5 = [cube2D.up_face[0],
                       cube2D.back_face[2],
                       cube2D.left_face[0]]

    Corner_Colors_6 = [cube2D.up_face[2],
                       cube2D.right_face[2],
                       cube2D.back_face[0]]

    Corner_Colors_7 = [cube2D.right_face[8],
                       cube2D.back_face[6],
                       cube2D.down_face[8]
                       ]
    # print(Edges_Colors[1])

    Corner_Colors = [Corner_Colors_0,
                     Corner_Colors_1,
                     Corner_Colors_2,
                     Corner_Colors_3,
                     Corner_Colors_4,
                     Corner_Colors_5,
                     Corner_Colors_6,
                     Corner_Colors_7,
                     ]
    return Center_Colors, Edges_Colors, Corner_Colors


def Num2Color(Num):
    cube_colors = [
        (0.5, 0.5, 0.5),  # Gray
        (1.0, 0.85, 0.1),  # Yellow
        (0.0, 0.318, 0.729),  # Blue
        (0.8, 0.118, 0.118),  # Red
        (0.0, 0.7, 0.2),  # Green
        (1.0, 0.345, 0.0),  # Orange
        (1.0, 1.0, 1.0)  # White
    ]
    return cube_colors[Num]
