import numpy as np
import cv2
from enum import Enum
import Cube2D

class Operation_ToShow(Enum):
    N = 0
    R = 1
    r = 2
    L = 3
    l = 4
    U = 5
    u = 6
    D = 7
    d = 8
    T_F = 9
    T_R = 10
    Wrong_Center = 11
    Wrong_All = 12

def Condition(NeedTurn_Flag,Done_Flag,step,detected_face,temp_Cube,Ori_Cube):
    condition = Operation_ToShow.N
    Mid_up_face = np.copy(Ori_Cube.up_face)
    Mid_right_face = np.copy(Ori_Cube.right_face)
    Mid_front_face = np.copy(Ori_Cube.front_face)
    Mid_down_face = np.copy(Ori_Cube.down_face)
    Mid_left_face = np.copy(Ori_Cube.left_face)
    Mid_back_face = np.copy(Ori_Cube.back_face)
    if step == "R" or step == "R'" or step == "L" or step == "L'" or step == "U" or step == "U'" or step == "D" or step == "D'" or step == "R`"  or step == "L`" or step == "U`" or step == "D`":
        if(detected_face[4] == temp_Cube.front_face[4]):#展示了所需的面
            if np.array_equal(detected_face, temp_Cube.front_face):#和操作后的一致
                condition = Operation_ToShow.N
                Done_Flag = True#操作完毕
            elif np.array_equal(detected_face, Ori_Cube.front_face):#和操作前的一致
                if(step == "R"):
                    condition = Operation_ToShow.R#绘制操作指示
                elif(step == "R'" or step == "R`"):
                    condition = Operation_ToShow.r
                elif(step == "L"):
                    condition = Operation_ToShow.L
                elif(step == "L'" or step == "L`"):
                    condition = Operation_ToShow.l
                elif(step == "U"):
                    condition = Operation_ToShow.U
                elif(step == "U'" or step == "U`"):
                    condition = Operation_ToShow.u
                elif(step == "D"):
                    condition = Operation_ToShow.D
                elif(step == "D'" or step == "D`"):
                    condition = Operation_ToShow.d
            else:
                condition = Operation_ToShow.Wrong_All
        else:
            condition = Operation_ToShow.Wrong_Center
    
    elif step == "F" or step == "F'" or step == "F`":
        if detected_face[4] == temp_Cube.right_face[4] or detected_face[4] == temp_Cube.front_face[4]:
            if np.array_equal(detected_face ,Ori_Cube.front_face):
                condition = Operation_ToShow.T_R#转向右侧
            elif np.array_equal(detected_face ,Ori_Cube.right_face):
                if(step == "F"):
                    condition = Operation_ToShow.L
                elif(step == "F'" or step == "F`"):
                    condition = Operation_ToShow.l
            elif np.array_equal(detected_face,temp_Cube.right_face):
                condition = Operation_ToShow.T_F
            elif np.array_equal(detected_face,temp_Cube.front_face):
                condition = Operation_ToShow.N
                Done_Flag = True
            else:
                condition = Operation_ToShow.Wrong_All
        else:
            condition = Operation_ToShow.Wrong_Center

    elif step == "B" or step == "B'" or step == "B`":
        NeedTurn_Flag = True
        if(Done_Flag == False):
            if(detected_face[4] == temp_Cube.front_face[4]):
                condition = Operation_ToShow.T_R
            elif(detected_face[4] == temp_Cube.right_face[4]):
                if np.array_equal(detected_face,Ori_Cube.right_face):
                    if(step == "B"):
                        condition = Operation_ToShow.R
                    elif(step == "B'"or step == "B`"):
                        condition = Operation_ToShow.r
                elif np.array_equal(detected_face,temp_Cube.right_face):
                    condition = Operation_ToShow.N
                    Done_Flag = True
            else:
                condition = Operation_ToShow.Wrong_Center
        if(Done_Flag):
            if np.array_equal(detected_face,temp_Cube.front_face):
                condition = Operation_ToShow.N
                NeedTurn_Flag = False
            elif(detected_face[4] == temp_Cube.right_face[4]):
                condition = Operation_ToShow.T_F
            else:
                condition = Operation_ToShow.Wrong_All

    elif step == "R2" or step == "L2" or step == "U2" or step == "D2" :
        if(detected_face[4] == temp_Cube.front_face[4]):#展示了所需的面
            if np.array_equal(detected_face,temp_Cube.front_face):
                condition = Operation_ToShow.N
                Done_Flag = True
            else:
                if(step == "R2"):
                    Mid_up_face, Mid_right_face, Mid_front_face, Mid_down_face, Mid_left_face, Mid_back_face = Cube2D.right_cw(Mid_up_face, Mid_right_face, Mid_front_face, Mid_down_face, Mid_left_face, Mid_back_face)
                    if np.array_equal(detected_face,Ori_Cube.front_face) or np.array_equal(detected_face,Mid_front_face):
                        condition = Operation_ToShow.R
                elif(step == "L2"):
                    Mid_up_face, Mid_right_face, Mid_front_face, Mid_down_face, Mid_left_face, Mid_back_face = Cube2D.left_cw(Mid_up_face, Mid_right_face, Mid_front_face, Mid_down_face, Mid_left_face, Mid_back_face)
                    if np.array_equal(detected_face,Ori_Cube.front_face) or np.array_equal(detected_face,Mid_front_face):
                        condition = Operation_ToShow.L
                elif(step == "U2"):
                    Mid_up_face, Mid_right_face, Mid_front_face, Mid_down_face, Mid_left_face, Mid_back_face = Cube2D.up_cw(Mid_up_face, Mid_right_face, Mid_front_face, Mid_down_face, Mid_left_face, Mid_back_face)
                    if np.array_equal(detected_face ,Ori_Cube.front_face) or np.array_equal(detected_face,Mid_front_face):
                        condition = Operation_ToShow.U
                elif(step == "D2"):
                    Mid_up_face, Mid_right_face, Mid_front_face, Mid_down_face, Mid_left_face, Mid_back_face = Cube2D.down_cw(Mid_up_face, Mid_right_face, Mid_front_face, Mid_down_face, Mid_left_face, Mid_back_face)
                    if np.array_equal(detected_face,Ori_Cube.front_face) or np.array_equal(detected_face,Mid_front_face):
                        condition = Operation_ToShow.D
                else:
                    condition = Operation_ToShow.Wrong_All
        else:
            condition = Operation_ToShow.Wrong_Center

    elif step == "F2":
        NeedTurn_Flag = True
        if(Done_Flag == False):
            if(detected_face[4] == temp_Cube.front_face[4]):
                condition = Operation_ToShow.T_R
            elif(detected_face[4] == temp_Cube.right_face[4]):
                Mid_up_face, Mid_right_face, Mid_front_face, Mid_down_face, Mid_left_face, Mid_back_face = Cube2D.front_cw(Mid_up_face, Mid_right_face, Mid_front_face, Mid_down_face, Mid_left_face, Mid_back_face)
                if  np.array_equal(detected_face,Ori_Cube.right_face) or np.array_equal(detected_face , Mid_right_face):
                    condition = Operation_ToShow.L
                elif np.array_equal(detected_face,temp_Cube.right_face):
                    condition = Operation_ToShow.T_F
                    Done_Flag = True
            else:
                condition = Operation_ToShow.Wrong_Center
        if(Done_Flag):
            if(detected_face[4] == temp_Cube.front_face[4]):
                condition = Operation_ToShow.N
                NeedTurn_Flag = False
            elif(detected_face[4] == temp_Cube.right_face[4]):
                condition = Operation_ToShow.T_F
            else:
                condition = Operation_ToShow.Wrong_All

    
    elif step == "B2":
        NeedTurn_Flag = True
        if(Done_Flag == False):
            if detected_face[4] == temp_Cube.front_face[4]:#展示了所需的面
                condition = Operation_ToShow.T_R
            elif(detected_face[4] == temp_Cube.right_face[4]):
                Mid_up_face, Mid_right_face, Mid_front_face, Mid_down_face, Mid_left_face, Mid_back_face = Cube2D.back_cw(Mid_up_face, Mid_right_face, Mid_front_face, Mid_down_face, Mid_left_face, Mid_back_face)
                if  np.array_equal(detected_face,Ori_Cube.right_face) or np.array_equal(detected_face , Mid_right_face):
                    condition = Operation_ToShow.r
                elif np.array_equal(detected_face,temp_Cube.right_face):
                    condition = Operation_ToShow.T_F
                    Done_Flag = True
                else:
                    condition = Operation_ToShow.Wrong_All
            else:
                condition = Operation_ToShow.Wrong_Center
        if(Done_Flag):
            if(detected_face[4] == temp_Cube.front_face[4]):
                condition = Operation_ToShow.N
                NeedTurn_Flag = False
            elif(detected_face[4] == temp_Cube.right_face[4]):
                condition = Operation_ToShow.T_F
            else:
                condition = Operation_ToShow.Wrong_Center
    elif step == "mL":
        if np.array_equal(detected_face,temp_Cube.front_face):
            condition = Operation_ToShow.N
            Done_Flag = True
        elif np.array_equal(detected_face,Ori_Cube.front_face):
            condition = Operation_ToShow.T_F
        else:
            condition = Operation_ToShow.Wrong_Center
    elif step == "mR":
        if np.array_equal(detected_face,temp_Cube.front_face):
            condition = Operation_ToShow.N
            Done_Flag = True
        elif np.array_equal(detected_face,Ori_Cube.front_face):
            condition = Operation_ToShow.T_R
        else:
            condition = Operation_ToShow.Wrong_Center
    return Done_Flag,condition,NeedTurn_Flag
    

def DrawInstructionText(curStep):
    if(curStep == "R"):
        text = "顺时针旋转R面90°（中心块为红色的面）"
    elif(curStep == "R'" or curStep == "R`"):
        text = "逆时针旋转R面90°（中心块为红色的面）"
    elif(curStep == "R2"):
        text = "旋转R面90°2次（中心块为红色的面）"
    elif(curStep == "L"):
        text = "顺时针旋转L面90°（中心块为橙色的面）"
    elif(curStep == "L'" or curStep == "L`"):
        text = "逆时针旋转L面90°（中心块为橙色的面）"
    elif(curStep == "L2"):
        text = "旋转L面90°2次（中心块为橙色的面）"
    elif(curStep == "U"):
        text = "顺时针旋转U面90°（中心块为黄色的面）"
    elif(curStep == "U'" or curStep == "U`"):
        text = "逆时针旋转U面90°（中心块为黄色的面）"
    elif(curStep == "U2"):
        text = "旋转R面90°2次（中心块为红色的面）"
    elif(curStep == "D"):
        text = "顺时针旋转D面90°（中心块为白色的面）"
    elif(curStep == "D'" or curStep == "D`"):
        text = "逆时针旋转D面90°（中心块为白色的面）"
    elif(curStep == "D2"):
        text = "旋转D面90°2次（中心块为红色的面）"
    elif(curStep == "F"):
        text = "顺时针旋转F面90°（中心块为蓝色的面）"
    elif(curStep == "F'" or curStep == "F`"):
        text = "顺时针旋转F面90°（中心块为蓝色的面）"
    elif(curStep == "F2"):
        text = "旋转F面90°2次（中心块为蓝色的面）"
    elif(curStep == "B"):
        text = "顺时针旋转B面90°（中心块为绿色的面）"
    elif(curStep == "B'" or curStep == "B`"):
        text = "逆时针旋转B面90°（中心块为绿色的面）"
    elif(curStep == "B2"):
        text = "旋转B面90°2次（中心块为绿色的面）"
    else:
        text = ""
    return text

def DrawInstructionText_2(curStep):
    if(curStep == "R"):
        text = "顺时针旋转R面90°"
    elif(curStep == "R'" or curStep == "R`"):
        text = "逆时针旋转R面90°"
    elif(curStep == "R2"):
        text = "旋转R面90°2次"
    elif(curStep == "L"):
        text = "顺时针旋转L面90°"
    elif(curStep == "L'" or curStep == "L`"):
        text = "逆时针旋转L面90°"
    elif(curStep == "L2"):
        text = "旋转L面90°2次"
    elif(curStep == "U"):
        text = "顺时针旋转U面90°"
    elif(curStep == "U'" or curStep == "U`"):
        text = "逆时针旋转U面90°"
    elif(curStep == "U2"):
        text = "旋转U面90°2次"
    elif(curStep == "D"):
        text = "顺时针旋转D面90°"
    elif(curStep == "D'" or curStep == "D`"):
        text = "逆时针旋转D面90°"
    elif(curStep == "D2"):
        text = "旋转D面90°2次"
    elif(curStep == "F"):
        text = "顺时针旋转F面90°"
    elif(curStep == "F'" or curStep == "F`"):
        text = "顺时针旋转F面90°"
    elif(curStep == "F2"):
        text = "旋转F面90°2次"
    elif(curStep == "B"):
        text = "顺时针旋转B面90°"
    elif(curStep == "B'" or curStep == "B`"):
        text = "逆时针旋转B面90°"
    elif(curStep == "B2"):
        text = "旋转B面90°2次"
    elif(curStep == "mL"):
        text = "整体转向L面"
    elif(curStep == "mR"):
        text = "整体转向R面"
    else:
        text = ""
    return text