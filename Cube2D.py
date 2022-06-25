from cv2 import cuda_Event
import numpy as np
import cv2
from enum import Enum
import kociemba
from Cube.cube import Cube
import Function as Fc

class Cube2D():
    def __init__(self) -> None:
        self.mu = 1
        self.mf = 2
        self.mr = 3
        self.mb = 4
        self.ml = 5
        self.md = 6
        self.up_face = [0, 0, 0, 0, self.mu, 0, 0, 0, 0]
        self.front_face = [0, 0, 0, 0, self.mf, 0, 0, 0, 0]
        self.right_face = [0, 0, 0, 0, self.mr, 0, 0, 0, 0]
        self.back_face = [0, 0, 0, 0, self.mb, 0, 0, 0, 0]
        self.left_face = [0, 0, 0, 0, self.ml, 0, 0, 0, 0]
        self.down_face = [0, 0, 0, 0, self.md, 0, 0, 0, 0]
        self.cube_solved = [self.mu, self.mu, self.mu, self.mu, self.mu, self.mu, self.mu, self.mu,self.mu,
                           self.mr, self.mr, self.mr, self.mr, self.mr, self.mr, self.mr, self.mr, self.mr,
                           self.mf, self.mf, self.mf, self.mf, self.mf, self.mf, self.mf, self.mf, self.mf,
                           self.md, self.md, self.md, self.md, self.md, self.md, self.md, self.md, self.md,
                           self.ml, self.ml, self.ml, self.ml, self.ml, self.ml, self.ml, self.ml, self.ml,
                           self.mb, self.mb, self.mb, self.mb, self.mb, self.mb,self.mb, self.mb, self.mb]

    def DetectFace(self,detected_face,curDetect):
        if(curDetect == 1 and self.mu == detected_face[0][4]): 
            self.up_face = np.asarray(detected_face[0])
            print(self.up_face)
        elif(curDetect == 2 and self.mf == detected_face[0][4]): 
            self.front_face = np.asarray(detected_face[0])
            print(self.front_face)
        elif(curDetect == 3 and self.mr == detected_face[0][4]): 
            self.right_face = np.asarray(detected_face[0])
            print(self.right_face)
        elif(curDetect == 4 and self.mb == detected_face[0][4]): 
            self.back_face = np.asarray(detected_face[0])
            print(self.back_face)
        elif(curDetect == 5 and self.ml == detected_face[0][4]): 
            self.left_face = np.asarray(detected_face[0])
            print(self.left_face)
        elif(curDetect == 6 and self.md == detected_face[0][4]): 
            self.down_face = np.asarray(detected_face[0])
            print(self.down_face)

    def CalculateSolution(self):
        solution = Fc.concat(self.up_face, self.right_face, self.front_face, self.down_face, self.left_face, self.back_face)
        final_str = ''
        if (solution == self.cube_solved).all():
            print('魔方已经还原')
        else:
            for val in range(len(solution)):
                if solution[val] == self.mf:
                    final_str = final_str + 'F'
                elif solution[val] == self.mr:
                    final_str = final_str + 'R'
                elif solution[val] == self.mb:
                    final_str = final_str + 'B'
                elif solution[val] == self.ml:
                    final_str = final_str + 'L'
                elif solution[val] == self.mu:
                    final_str = final_str + 'U'
                elif solution[val] == self.md:
                    final_str = final_str + 'D'
            try:
                solved = kociemba.solve(final_str)
                # text = '还原步骤:' + solved
                # print(text)
                steps = solved.split()
                CalculateDone = True
                return solved,steps,CalculateDone
            except:
                # print('识别结果不构成标准魔方，无法还原')
                # text = '识别结果不构成标准魔方，无法还原'
                steps = [0]
                CalculateDone = False
                return steps,CalculateDone
    def copy(self):
        NewCube = Cube2D()
        NewCube.mu = np.copy(self.mu)
        NewCube.mf = np.copy(self.mf)
        NewCube.mr = np.copy(self.mr)
        NewCube.mb = np.copy(self.mb)
        NewCube.ml = np.copy(self.ml)
        NewCube.md = np.copy(self.md)
        NewCube.up_face = np.copy(self.up_face)
        NewCube.front_face = np.copy(self.front_face)
        NewCube.right_face = np.copy(self.right_face)
        NewCube.back_face = np.copy(self.back_face)
        NewCube.left_face = np.copy(self.left_face)
        NewCube.down_face = np.copy(self.down_face)
        return NewCube

    def check(self):
        solution  = Fc.concat(self.up_face, self.right_face, self.front_face, self.down_face, self.left_face, self.back_face)
        if (solution == self.cube_solved).all():
            return True
        else:
            return False
def rotate_cw(face):
    final = np.copy(face)
    final[0] = face[6]
    final[1] = face[3]
    final[2] = face[0]
    final[3] = face[7]
    final[4] = face[4]
    final[5] = face[1]
    final[6] = face[8]
    final[7] = face[5]
    final[8] = face[2]
    return final

def rotate_ccw(face):
    final = np.copy(face)
    final[8] = face[6]
    final[7] = face[3]
    final[6] = face[0]
    final[5] = face[7]
    final[4] = face[4]
    final[3] = face[1]
    final[2] = face[8]
    final[1] = face[5]
    final[0] = face[2]
    return final

def right_cw(up_face,right_face,front_face,down_face,left_face,back_face):
    temp = np.copy(front_face)
    front_face[2] = down_face[2]
    front_face[5] = down_face[5]
    front_face[8] = down_face[8]
    down_face[2] = back_face[6]
    down_face[5] = back_face[3]
    down_face[8] = back_face[0]
    back_face[0] = up_face[8]
    back_face[3] = up_face[5]
    back_face[6] = up_face[2]
    up_face[2] = temp[2]
    up_face[5] = temp[5]
    up_face[8] = temp[8]
    right_face = rotate_cw(right_face)
    return up_face,right_face,front_face,down_face,left_face,back_face

def right_ccw(up_face,right_face,front_face,down_face,left_face,back_face):
    temp = np.copy(front_face)
    front_face[2] = up_face[2]
    front_face[5] = up_face[5]
    front_face[8] = up_face[8]
    up_face[2] = back_face[6]
    up_face[5] = back_face[3]
    up_face[8] = back_face[0]
    back_face[0] = down_face[8]
    back_face[3] = down_face[5]
    back_face[6] = down_face[2]
    down_face[2] = temp[2]
    down_face[5] = temp[5]
    down_face[8] = temp[8]
    right_face = rotate_ccw(right_face)
    return up_face,right_face,front_face,down_face,left_face,back_face

def left_cw(up_face,right_face,front_face,down_face,left_face,back_face):
    temp = np.copy(front_face)
    front_face[0] = up_face[0]
    front_face[3] = up_face[3]
    front_face[6] = up_face[6]
    up_face[0] = back_face[8]
    up_face[3] = back_face[5]
    up_face[6] = back_face[2]
    back_face[2] = down_face[6]
    back_face[5] = down_face[3]
    back_face[8] = down_face[0]
    down_face[0] = temp[0]
    down_face[3] = temp[3]
    down_face[6] = temp[6]
    left_face = rotate_cw(left_face)
    return up_face,right_face,front_face,down_face,left_face,back_face

def left_ccw(up_face,right_face,front_face,down_face,left_face,back_face):
    temp = np.copy(front_face)
    front_face[0] = down_face[0]
    front_face[3] = down_face[3]
    front_face[6] = down_face[6]
    down_face[0] = back_face[8]
    down_face[3] = back_face[5]
    down_face[6] = back_face[2]
    back_face[2] = up_face[6]
    back_face[5] = up_face[3]
    back_face[8] = up_face[0]
    up_face[0] = temp[0]
    up_face[3] = temp[3]
    up_face[6] = temp[6]
    left_face = rotate_ccw(left_face)
    return up_face,right_face,front_face,down_face,left_face,back_face

def front_cw(up_face,right_face,front_face,down_face,left_face,back_face):
    temp = np.copy(up_face)
    # print(front_face)
    front_face = rotate_cw(front_face)
    # print(front_face)
    up_face[8] = left_face[2]
    up_face[7] = left_face[5]
    up_face[6] = left_face[8]
    left_face[2] = down_face[0]
    left_face[5] = down_face[1]
    left_face[8] = down_face[2]
    down_face[2] = right_face[0]
    down_face[1] = right_face[3]
    down_face[0] = right_face[6]
    right_face[0] = temp[6]
    right_face[3] = temp[7]
    right_face[6] = temp[8]
    return up_face,right_face,front_face,down_face,left_face,back_face

def front_ccw(up_face,right_face,front_face,down_face,left_face,back_face):
    temp = np.copy(up_face)
    # print(front_face)
    front_face = rotate_ccw(front_face)
    # print(front_face)
    up_face[6] = right_face[0]
    up_face[7] = right_face[3]
    up_face[8] = right_face[6]
    right_face[0] = down_face[2]
    right_face[3] = down_face[1]
    right_face[6] = down_face[0]
    down_face[0] = left_face[2]
    down_face[1] = left_face[5]
    down_face[2] = left_face[8]
    left_face[8] = temp[6]
    left_face[5] = temp[7]
    left_face[2] = temp[8]
    return up_face,right_face,front_face,down_face,left_face,back_face

def back_cw(up_face,right_face,front_face,down_face,left_face,back_face):
    temp = np.copy(up_face)
    up_face[0] = right_face[2]
    up_face[1] = right_face[5]
    up_face[2] = right_face[8]
    right_face[8] = down_face[6]
    right_face[5] = down_face[7]
    right_face[2] = down_face[8]
    down_face[6] = left_face[0]
    down_face[7] = left_face[3]
    down_face[8] = left_face[6]
    left_face[0] = temp[2]
    left_face[3] = temp[1]
    left_face[6] = temp[0]
    back_face = rotate_cw(back_face)
    return up_face,right_face,front_face,down_face,left_face,back_face

def back_ccw(up_face,right_face,front_face,down_face,left_face,back_face):
    temp = np.copy(up_face)
    up_face[2] = left_face[0]
    up_face[1] = left_face[3]
    up_face[0] = left_face[6]
    left_face[0] = down_face[6]
    left_face[3] = down_face[7]
    left_face[6] = down_face[8]
    down_face[6] = right_face[8]
    down_face[7] = right_face[5]
    down_face[8] = right_face[2]
    right_face[2] = temp[0]
    right_face[5] = temp[1]
    right_face[8] = temp[2]
    back_face = rotate_ccw(back_face)
    return up_face,right_face,front_face,down_face,left_face,back_face

def up_cw(up_face,right_face,front_face,down_face,left_face,back_face):
    temp = np.copy(front_face)
    front_face[0] = right_face[0]
    front_face[1] = right_face[1]
    front_face[2] = right_face[2]
    right_face[0] = back_face[0]
    right_face[1] = back_face[1]
    right_face[2] = back_face[2]
    back_face[0] = left_face[0]
    back_face[1] = left_face[1]
    back_face[2] = left_face[2]
    left_face[0] = temp[0]
    left_face[1] = temp[1]
    left_face[2] = temp[2]
    up_face = rotate_cw(up_face)
    return up_face,right_face,front_face,down_face,left_face,back_face

def up_ccw(up_face,right_face,front_face,down_face,left_face,back_face):
    temp = np.copy(front_face)
    front_face[0] = left_face[0]
    front_face[1] = left_face[1]
    front_face[2] = left_face[2]
    left_face[0] = back_face[0]
    left_face[1] = back_face[1]
    left_face[2] = back_face[2]
    back_face[0] = right_face[0]
    back_face[1] = right_face[1]
    back_face[2] = right_face[2]
    right_face[0] = temp[0]
    right_face[1] = temp[1]
    right_face[2] = temp[2]
    up_face = rotate_ccw(up_face)
    return up_face,right_face,front_face,down_face,left_face,back_face

def down_cw(up_face,right_face,front_face,down_face,left_face,back_face):
    temp = np.copy(front_face)
    front_face[6] = left_face[6]
    front_face[7] = left_face[7]
    front_face[8] = left_face[8]
    left_face[6] = back_face[6]
    left_face[7] = back_face[7]
    left_face[8] = back_face[8]
    back_face[6] = right_face[6]
    back_face[7] = right_face[7]
    back_face[8] = right_face[8]
    right_face[6] = temp[6]
    right_face[7] = temp[7]
    right_face[8] = temp[8]
    down_face = rotate_cw(down_face)
    return up_face,right_face,front_face,down_face,left_face,back_face

def down_ccw(up_face,right_face,front_face,down_face,left_face,back_face):
    temp = np.copy(front_face)
    front_face[6] = right_face[6]
    front_face[7] = right_face[7]
    front_face[8] = right_face[8]
    right_face[6] = back_face[6]
    right_face[7] = back_face[7]
    right_face[8] = back_face[8]
    back_face[6] = left_face[6]
    back_face[7] = left_face[7]
    back_face[8] = left_face[8]
    left_face[6] = temp[6]
    left_face[7] = temp[7]
    left_face[8] = temp[8]
    down_face = rotate_ccw(down_face)
    return up_face,right_face,front_face,down_face,left_face,back_face

def turn_to_right(up_face,right_face,front_face,down_face,left_face,back_face):
    temp = np.copy(front_face)
    front_face = np.copy(right_face)
    right_face = np.copy(back_face)
    back_face = np.copy(left_face)
    left_face = np.copy(temp)
    new_up_face = rotate_cw(up_face)
    new_down_face = rotate_ccw(down_face)
    return new_up_face,right_face,front_face,new_down_face,left_face,back_face

def turn_to_left(up_face,right_face,front_face,down_face,left_face,back_face):
    temp = np.copy(front_face)
    front_face = np.copy(left_face)
    left_face = np.copy(back_face)
    back_face = np.copy(right_face)
    right_face = np.copy(temp)
    new_up_face = rotate_ccw(up_face)
    new_down_face = rotate_cw(down_face)
    return new_up_face,right_face,front_face,new_down_face,left_face,back_face

def PreOperation(step,Cube2D):
    up_face = Cube2D.up_face
    right_face = Cube2D.right_face
    front_face = Cube2D.front_face
    down_face = Cube2D.down_face 
    left_face = Cube2D.left_face
    back_face = Cube2D.back_face
    if step == "R":
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = right_cw(up_face, right_face, front_face, down_face, left_face, back_face)
                #print(concat(up_face, right_face, front_face, down_face, left_face, back_face))
    elif step == "R'" or step == "R`":
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = right_ccw(up_face, right_face, front_face, down_face, left_face, back_face)
                #print(concat(up_face, right_face, front_face, down_face, left_face, back_face))
    elif step == "R2":
        new_up_face_1, new_right_face_1, new_front_face_1, new_down_face_1, new_left_face_1, new_back_face_1 = right_cw(up_face, right_face, front_face, down_face, left_face, back_face)
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = right_cw(new_up_face_1, new_right_face_1, new_front_face_1, new_down_face_1, new_left_face_1, new_back_face_1)
                #print(concat(up_face, right_face, front_face, down_face, left_face, back_face))
    elif step == "L":
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = left_cw(up_face, right_face, front_face, down_face, left_face, back_face)
                #print(concat(up_face, right_face, front_face, down_face, left_face, back_face))
    elif step == "L'" or step == "L`":
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = left_ccw(up_face, right_face, front_face, down_face, left_face, back_face)
                #print(concat(up_face, right_face, front_face, down_face, left_face, back_face))
    elif step == "L2":
        new_up_face_1, new_right_face_1, new_front_face_1, new_down_face_1, new_left_face_1, new_back_face_1 = left_cw(up_face, right_face, front_face, down_face, left_face, back_face)
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = left_cw(new_up_face_1, new_right_face_1, new_front_face_1, new_down_face_1, new_left_face_1, new_back_face_1)
                #print(concat(up_face, right_face, front_face, down_face, left_face, back_face))
    elif step == "F":
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = front_cw(up_face, right_face, front_face, down_face, left_face, back_face)
                #print(concat(up_face, right_face, front_face, down_face, left_face, back_face))
    elif step == "F'" or step == "F`":
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = front_ccw(up_face, right_face, front_face, down_face, left_face, back_face)
                #print(concat(up_face, right_face, front_face, down_face, left_face, back_face))
    elif step == "F2":
        new_up_face_1, new_right_face_1, new_front_face_1, new_down_face_1, new_left_face_1, new_back_face_1 = front_cw(up_face, right_face, front_face, down_face, left_face, back_face)
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = front_cw(new_up_face_1, new_right_face_1, new_front_face_1, new_down_face_1, new_left_face_1, new_back_face_1)
                #print(concat(up_face, right_face, front_face, down_face, left_face, back_face))
    elif step == "B":
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = back_cw(up_face, right_face, front_face, down_face, left_face, back_face)
                #print(concat(up_face, right_face, front_face, down_face, left_face, back_face))
    elif step == "B'" or step == "B`":
                #print(up_face, right_face, front_face, down_face, left_face, back_face)
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = back_ccw(up_face, right_face, front_face, down_face, left_face, back_face)
    elif step == "B2":
        new_up_face_1, new_right_face_1, new_front_face_1, new_down_face_1, new_left_face_1, new_back_face_1 = back_cw(up_face, right_face, front_face, down_face, left_face, back_face)
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = back_cw(new_up_face_1, new_right_face_1, new_front_face_1, new_down_face_1, new_left_face_1, new_back_face_1)
                #print(concat(up_face, right_face, front_face, down_face, left_face, back_face))
    elif step == "U":
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = up_cw(up_face, right_face, front_face, down_face, left_face, back_face)
                #print(concat(up_face, right_face, front_face, down_face, left_face, back_face))
    elif step == "U'" or step == "U`":
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = up_ccw(up_face, right_face, front_face, down_face, left_face, back_face)
                #print(concat(up_face, right_face, front_face, down_face, left_face, back_face))
    elif step == "U2":
        new_up_face_1, new_right_face_1, new_front_face_1, new_down_face_1, new_left_face_1, new_back_face_1 = up_cw(up_face, right_face, front_face, down_face, left_face, back_face)
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = up_cw(new_up_face_1, new_right_face_1, new_front_face_1, new_down_face_1, new_left_face_1, new_back_face_1)
                #print(concat(up_face, right_face, front_face, down_face, left_face, back_face))
    elif step == "D":
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = down_cw(up_face, right_face, front_face, down_face, left_face, back_face)
                #print(concat(up_face, right_face, front_face, down_face, left_face, back_face))
    elif step == "D'" or step == "D`":
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = down_ccw(up_face, right_face, front_face, down_face, left_face, back_face)
                #print(concat(up_face, right_face, front_face, down_face, left_face, back_face))
    elif step == "D2":
        new_up_face_1, new_right_face_1, new_front_face_1, new_down_face_1, new_left_face_1, new_back_face_1 = down_cw(up_face, right_face, front_face, down_face, left_face, back_face)
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = down_cw(new_up_face_1, new_right_face_1, new_front_face_1, new_down_face_1, new_left_face_1, new_back_face_1)
                #print(concat(up_face, right_face, front_face, down_face, left_face, back_face))
    elif step == "mL":
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = turn_to_left(up_face, right_face, front_face, down_face, left_face, back_face)
        temp = Cube2D.mf
        Cube2D.mf = Cube2D.ml
        Cube2D.ml = Cube2D.mb
        Cube2D.mb = Cube2D.mr
        Cube2D.mr = temp
    elif step == "mR":
        new_up_face, new_right_face, new_front_face, new_down_face, new_left_face, new_back_face = turn_to_right(up_face, right_face, front_face, down_face, left_face, back_face)
        temp = Cube2D.mf
        Cube2D.mf = Cube2D.mr
        Cube2D.mr = Cube2D.mb
        Cube2D.mb = Cube2D.ml
        Cube2D.ml = temp

    Cube2D.up_face = new_up_face
    Cube2D.right_face = new_right_face
    Cube2D.front_face  = new_front_face
    Cube2D.down_face  = new_down_face
    Cube2D.left_face = new_left_face
    Cube2D.back_face = new_back_face
    return Cube2D

