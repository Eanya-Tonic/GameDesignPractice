# -*- coding: utf-8 -*-
import sys
from typing import List
import cv2
import math
import numpy as np
from PySide2 import QtGui,QtCore,QtWidgets
from PySide2.QtWidgets import QApplication, QWidget,QMainWindow,QLabel
from PySide2.QtCore import QTimer,QDateTime,QRect,Slot,QObject,SIGNAL,Signal
from PySide2 import QtOpenGL
from PySide2.QtGui import QMouseEvent
from MainWindowUI import Ui_MainWindow
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from enum import Enum
from datetime import date, datetime
import random
from sklearn.neighbors import KNeighborsClassifier  # 引入KNN分类器

import DrawCube3D
import Function as Fc
import ImgInput
import Cube2D
import Operation as Op
from quat import *
from geometry import *
import BeginnerSolver

def create_referrence_color(image,color_string):
    #"yellow", "green", "red", "white", "blue", "orange"
    string = [(255,255,255) for rect in range(9)]
    for n in range(len(color_string)):
        if (color_string[n] == "yellow"):
            string[n] = (0,255,200)
        elif (color_string[n] == "green"):
            string[n] = (0,255,0)
        elif (color_string[n] == "red"):
            string[n] = (0,0,255)
        elif (color_string[n] == "white"):
            string[n] = (255,255,255)
        elif (color_string[n] == "blue"):
            string[n] = (255,0,0)
        elif (color_string[n] == "orange"):
            string[n] = (10,100,255)
        else:
            string[n] = (100,100,100)
    #print (string)
    for row in range(3):
        y = 10 + row * 30
        for col in range(3):
            x = 450 + col *30
            cv2.rectangle(image,(x,y),(x+20,y+20),string[row*3+col],-1)

def color(bgrtuple):
    """
    Takes a tuple input that has (b,g,r) and return the color of that pixel
    """
    bgrtuple = list(bgrtuple)
    
    b = bgrtuple[0]
    g = bgrtuple[1]
    r = bgrtuple[2]
    #if (r >100 and  r*1.3> g > r*0.9 and r*0.9>b>r*0.7):
    if (-60 < r-g < 60 and 55<r-b<105):
        return "yellow"
    if (r>180 and g<r*0.8 and b< r*0.8):
        return "orange"
    if (r-g>30 and r-b>30):
        return "red"
    if (g-b>30 and g-r>30):
    #if (g>120 and r <120 and b <120):
        return "green"
    if (b-r >30 and b - g >30):
        return "blue"
    if (g*1.2>r>g*0.8 and g*1.2>b>g*0.8):
        return "white"
    else:
        return "grey"

def get_color_string(bgrlist):
    result_string = ["hi" for face in range(9)]
    
    running = 0
    while (running < 9):
        bgrstring = bgrlist[running]
        result_string[running] = color(tuple(bgrstring))
        running = running+1
    return result_string

def ev(img,x,y,layer): #Evaluates the average value inside a rectangle of one color channel
    #(x,y) is the coordinate of the center of the rectangle
    #w and l are the width and lendth of the rectangle
    w = 10
    h = 10
    a = list(range(x-w, x+w))
    b = list(range(y-h, y+h))
    t = 0
    tot = 0
    for c in a:
        for d in b:
            tot = tot + img[d,c,layer]
            t = t +1
            
    return int(tot/t)


def process(image):
    #Process an bgr image to binary 
    #kernel = np.ones((3,3),np.uint8) this is an alternative way to create kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #Corresponding grayscale image to the input
    binary = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,11,5) 
    binary_blurred = cv2.medianBlur(binary,5)
    binary_dilated = cv2.dilate(binary_blurred,kernel,iterations = 5)
    binary_inv = 255 - binary_dilated
    
    return binary_inv

def approx_is_square(approx, SIDE_VS_SIDE_THRESHOLD=0.70, ANGLE_THRESHOLD=20, ROTATE_THRESHOLD=30):
    """
    Rules
    - there must be four corners
    - all four lines must be roughly the same length
    - all four corners must be roughly 90 degrees
    - AB and CD must be horizontal lines
    - AC and BC must be vertical lines
    SIDE_VS_SIDE_THRESHOLD
        If this is 1 then all 4 sides must be the exact same length.  If it is
        less than one that all sides must be within the percentage length of
        the longest side.
        A ---- B
        |      |
        |      |
        C ---- D
    """

    assert SIDE_VS_SIDE_THRESHOLD >= 0 and SIDE_VS_SIDE_THRESHOLD <= 1, "SIDE_VS_SIDE_THRESHOLD must be between 0 and 1"
    assert ANGLE_THRESHOLD >= 0 and ANGLE_THRESHOLD <= 90, "ANGLE_THRESHOLD must be between 0 and 90"

    # There must be four corners
    if len(approx) != 4:
        return False
    
    # Find the four corners
    (A, B, C, D) = sort_corners(tuple(approx[0][0]),
                                tuple(approx[1][0]),
                                tuple(approx[2][0]),
                                tuple(approx[3][0]))

    # Find the lengths of all four sides
    AB = pixel_distance(A, B)
    AC = pixel_distance(A, C)
    DB = pixel_distance(D, B)
    DC = pixel_distance(D, C)
    distances = (AB, AC, DB, DC)
    max_distance = max(distances)
    cutoff = int(max_distance * SIDE_VS_SIDE_THRESHOLD)

    # If any side is much smaller than the longest side, return False
    for distance in distances:
        if distance < cutoff:
            return False

    return True

def sort_corners(corner1, corner2, corner3, corner4):
    """
    Sort the corners such that
    - A is top left
    - B is top right
    - C is bottom left
    - D is bottom right
    Return an (A, B, C, D) tuple
    """
    results = []
    corners = (corner1, corner2, corner3, corner4)

    min_x = None
    max_x = None
    min_y = None
    max_y = None

    for (x, y) in corners:
        if min_x is None or x < min_x:
            min_x = x

        if max_x is None or x > max_x:
            max_x = x

        if min_y is None or y < min_y:
            min_y = y

        if max_y is None or y > max_y:
            max_y = y

    # top left
    top_left = None
    top_left_distance = None
    for (x, y) in corners:
        distance = pixel_distance((min_x, min_y), (x, y))
        if top_left_distance is None or distance < top_left_distance:
            top_left = (x, y)
            top_left_distance = distance

    results.append(top_left)

    # top right
    top_right = None
    top_right_distance = None

    for (x, y) in corners:
        if (x, y) in results:
            continue

        distance = pixel_distance((max_x, min_y), (x, y))
        if top_right_distance is None or distance < top_right_distance:
            top_right = (x, y)
            top_right_distance = distance
    results.append(top_right)

    # bottom left
    bottom_left = None
    bottom_left_distance = None

    for (x, y) in corners:
        if (x, y) in results:
            continue

        distance = pixel_distance((min_x, max_y), (x, y))

        if bottom_left_distance is None or distance < bottom_left_distance:
            bottom_left = (x, y)
            bottom_left_distance = distance
    results.append(bottom_left)

    # bottom right
    bottom_right = None
    bottom_right_distance = None

    for (x, y) in corners:
        if (x, y) in results:
            continue

        distance = pixel_distance((max_x, max_y), (x, y))

        if bottom_right_distance is None or distance < bottom_right_distance:
            bottom_right = (x, y)
            bottom_right_distance = distance
    results.append(bottom_right)

    return results

def pixel_distance(A, B):
    """
    Pythagrian therom to find the distance between two pixels
    """
    A = (1,1)
    B = (1,1)
    (col_A, row_A) = A
    (col_B, row_B) = B

    return (math.sqrt(math.pow(col_B - col_A, 2) + math.pow(row_B - row_A, 2))+0)

def draw_aim(image,x1,y1,x2,y2,w,b,g,r):
    #Draws a box aim on an image to tell the user where to put the rubik's cube
    cv2.line(image,(x1,y1),(x1,y1+w),(b,g,r),2)
    cv2.line(image,(x1,y1),(x1+w,y1),(b,g,r),2)

    cv2.line(image,(x2,y1),(x2,y1+w),(b,g,r),2)
    cv2.line(image,(x2,y1),(x2-w,y1),(b,g,r),2)
        
    cv2.line(image,(x1,y2),(x1,y2-w),(b,g,r),2)
    cv2.line(image,(x1,y2),(x1+w,y2),(b,g,r),2)

    cv2.line(image,(x2,y2),(x2,y2-w),(b,g,r),2)
    cv2.line(image,(x2,y2),(x2-w,y2),(b,g,r),2)

def get_string(c_list):
    """
    Takes a list of (x,y) coordinates and arrange them in order from top left corner to bottom right
    """
    
    x = [0 for num in range(9)]
    y = [0 for num in range(9)]
    #cords = [[0 for col in range(2)] for row in range(9)]
    for a in range(len(c_list)):
        x[a] = c_list[a][0]
        y[a] = c_list[a][1]
    xmin = min(x)
    xmax = max(x)
    
    ymin = min(y)
    ymax = max(y)

    xavg = int((xmin+xmax)/2)
    yavg = int((ymin+ymax)/2)
    
    #cv2.rectangle(img,(xmin,ymin),(xmax,ymax),(100,100,100), 5)
    string = [[xmin,ymin],[xavg,ymin],[xmax,ymin],[xmin,yavg],[xavg,yavg],[xmax,yavg],[xmin,ymax],[xavg,ymax],[xmax,ymax]]
    #string = [[xmin,ymin],[xmax,ymax]]

    return string

def get_average_color(image,image_coordinates):
    result_string = [[0 for col in range(5)] for face in range(9)]
    running = 0
    while (running < 9):
        x = image_coordinates[running][0]
        y = image_coordinates[running][1]
        result_string[running][0]= ev(image,x,y,0)
        result_string[running][1]= ev(image,x,y,1)
        result_string[running][2]= ev(image,x,y,2)
        result_string[running][3]= x
        result_string[running][4]= y
        running = running +1
    return result_string

class CurState(Enum):
    Pause = 0
    OriginalColor_Detect = 1
    OriginalColor_Confirm = 2
    OriginalColor_Done = 3
    ProgressColor_Start = 4
    ProgressColor_Detect = 5
    ProgressColor_Done = 6
    Count_Down = 7
    Start = 8
    CalibrateColors = 9
    CalibrateColors_Confirm = 10

class CurLayer(Enum):
    Cross = 1
    Corner = 2
    Second_layer = 3
    oll_step_1 = 4
    oll_step_2 = 5
    pll_step_1 = 6
    pll_step_2 = 7
    Done = 8

class Solvemethod(Enum):
    UnChoose = 0
    K_method = 1
    Beginner_method = 2

labelSig = 0
clickFlag = False

class LabelDrawSticker(QLabel):  ##重写自己的QLabel
    global labelSig,clickFlag
    def __int__(self, parent=None):
        QLabel.__init__(self,parent)
    def mousePressEvent(self, QMouseEvent):  ##单击事件
        global labelSig,clickFlag
        if QMouseEvent.buttons() == QtCore.Qt.LeftButton:   ##判断是否鼠标左键点击
            clickFlag = False
            pos = QMouseEvent.pos()
            x,y = pos.x(), pos.y()
            if(x in range(0,66)):
                if(y in range(0,66)):
                    labelSig = 1
                    clickFlag = True
                elif(y in range(67,132)):
                    labelSig = 4
                    clickFlag = True
                elif(y in range(133,200)):
                    labelSig = 7
                    clickFlag = True
            elif(x in range(67,132)):
                if(y in range(0,66)):
                    labelSig = 2
                    clickFlag = True
                elif(y in range(67,132)):
                    labelSig = 5
                    clickFlag = True
                elif(y in range(133,200)):
                    labelSig = 8
                    clickFlag = True
            elif(x in range(133,200)):
                if(y in range(0,66)):
                    labelSig = 3
                    clickFlag = True
                elif(y in range(67,132)):
                    labelSig = 6
                    clickFlag = True
                elif(y in range(133,200)):
                    labelSig = 9
                    clickFlag = True
            if(clickFlag == False):
                labelSig = 0
        print(clickFlag)

class MyWidget(QMainWindow,Ui_MainWindow):
    sendCube2D = Signal(object)
    sendStep = Signal(object)
    def restart_program(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        os.system("Demo.py")
    def __init__(self,parent = None):
        super(MyWidget,self).__init__(parent = parent)

        self.timer_camera = QTimer()
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Label_DrawSticker = LabelDrawSticker(self.ui.Label_DrawSticker)
        self.openGLWidget = MyGLWidget(self.ui.centralwidget)
        self.timer_opengl = QTimer()
        self.ui.Text2_3DModel.raise_()
        self.ui.Text12_NamePair.raise_()
        self.ui.Text0_Welcome.raise_()
        self.ui.Text15_Chosemethod.raise_()
        self.ui.Button_Beginner.raise_()
        self.ui.Button_Kociemba.raise_()
        self.MyInit()
        self.slot_init()
        self.MySetStyles()
        self.addSolidColors()

        # self.loadGLTextures()
        self.openGLWidget.setObjectName(u"openGLWidget")
        self.openGLWidget.setGeometry(QRect(40, 140, 900, 675))
        self.openGLWidget.initializeGL()
        QObject.connect(self.ui.Button_Check,SIGNAL('clicked()'),self.Button_Check_Clicked)
        QObject.connect(self.ui.Button_Retry,SIGNAL('clicked()'),self.Button_Retry_Clicked)
        QObject.connect(self.ui.Button_Restart,SIGNAL('clicked()'),self.Button_Restart_Clicked)
        QObject.connect(self.ui.Button_Beginner,SIGNAL('clicked()'),self.Button_Beginner_Clicked)
        QObject.connect(self.ui.Button_Kociemba,SIGNAL('clicked()'),self.Button_Kociemba_Clicked)

    def MyInit(self):
        self.curState = CurState.Start
        self.curDetect = 1
        self.steps = []
        self.curStep = 0
        self.start_time = datetime.now()
        self.CountDown_Flag = False
        self.ReDetect_Flag = False
        self.DetecteDone_Flag = False
        self.OriginalDetectDone_Flag = False
        self.OriginalCorrect = False
        self.CenterCorret_Flag = False
        self.ProcessReady_Flag = False
        self.NextMove_Flag = False
        self.NeedTurn_Flag = False
        self.SendStep_Flag = True
        self.faces = []
        self.detectedface = [0,0,0,0,0,0,0,0,0]
        self.Stickers = [0,0,0,0,0,0,0,0,0]
        self.curDetect = 1
        self.Cube2D = Cube2D.Cube2D()
        self.Cube2D_temp = Cube2D.Cube2D()
        self.sendCube2D.emit(self.Cube2D)
        self.Condition = Op.Operation_ToShow.N
        self.BackDone_Flag = False
        self.MoveDone_Flag = False
        self.DrawStickersArea = np.zeros((191, 191, 3), np.uint8)
        self.DrawStickersArea[:] = (0, 0, 0)

        self.DrawCube2DArea = np.zeros((220, 292, 3), np.uint8)
        self.DrawCube2DArea[:] = (125, 125, 125)
        self.Solvemethod = Solvemethod.UnChoose
        self.curLayer = 0
        self.BeginnerState = [CurLayer.Cross,CurLayer.Corner,CurLayer.Second_layer,CurLayer.oll_step_1,CurLayer.oll_step_2,CurLayer.pll_step_1,CurLayer.pll_step_2,CurLayer.Done]
        self.solve_cross = []
        self.solve_corners = []
        self.solve_second_layer= []
        self.oll_step_1 = []
        self.oll_step_2 = []
        self.pll_step_1 = []
        self.pll_step_2 = []
        self.color_s=[[0 for col in range(5)] for face in range(9)]
        self.noCircle=False
        self.CalibrateEnd=False
        self.colorX = [[0 for col in range(3)] for face in range(282)]
        self.colorY = np.zeros(282,dtype=np.uint8)
        self.index = 0
        self.knn = KNeighborsClassifier()  # 调用KNN分类器

        ####DEBUG

    def MySetStyles(self):
        self.ui.Text0_Welcome.setStyleSheet('''font-family:DengXian;font-size = 24pt;background:solid rgba(255, 255, 255, 0.7); ''')
        self.ui.Text1_Detected.setStyleSheet('''font-family:DengXian;font-size = 24pt;''')
        self.ui.Text2_3DModel.setStyleSheet('''font-family:DengXian;background:solid rgb(255, 255, 255)''')
        self.ui.Text2_Video.setStyleSheet('''font-family:DengXian;color:white;''')
        self.ui.Text3_Instruction.setStyleSheet('''font-family:DengXian;color: red;background:solid rgb(255, 255, 255);''')
        self.ui.Text4_CountDown.setStyleSheet('''font-family:DengXian;color:white;''')
        self.ui.Text5_Resolution.setStyleSheet('''font-family:DengXian;font-size = 14pt;background:solid rgb(200, 200, 200);''')
        self.ui.Text6_CurStep.setStyleSheet('''font-family:DengXian;background:solid rgb(200, 200, 200);''')
        self.ui.Text7_NextStep.setStyleSheet('''font-family:DengXian;background:solid rgb(200, 200, 200);''')
        self.ui.Text9_Judge.setStyleSheet('''font-family:DengXian;font-size = 24pt;background:solid rgba(255, 255, 255, 0.7); ''')
        self.ui.Text9_Judge.setText("操作结果")
        self.ui.Text10_Notification.setText("说明：\n\n    1.请在明亮的自然环境光下识别魔方\n    2.请确保摄像机连接正确，并将摄像机平放在桌面上，镜头朝向正前方\n    3.请注意阅读画面上方的提示\n    4.如果还原过程中发现自己转错了请点击“重新开始”按钮")
        self.ui.Text10_Notification.setStyleSheet('''font-family:DengXian;font-size = 16pt;background:solid rgb(200, 200, 200); ''')
        self.ui.Text15_Chosemethod.setStyleSheet('''font-family:DengXian;color:red;background:solid rgb(255, 255, 255); ''')
        self.ui.Label_DrawBackGround.setStyleSheet('''background:solid rgb(200, 200, 200);''')
        self.ui.Text12_NamePair.setStyleSheet('''background:solid rgb(255, 255, 255)''')
        text = self.setNamepair(self.Cube2D_temp)
        self.ui.Text12_NamePair.setText(text)

    def Button_Check_Clicked(self):
        print('click')
        self.MySetStyles()
        if(self.curState == CurState.Start):
            # self.ui.Text0_Welcome.setEnabled(False)
            self.ui.Text0_Welcome.close()
            self.ui.Text10_Notification.show()
            self.ui.Text5_Resolution.show()
            self.ui.Text12_NamePair.show()
            self.curState = CurState.CalibrateColors
            self.CountDown_Flag = True
            self.start_time = datetime.now()
        if((self.CountDown_Flag == False or self.CalibrateEnd == True) and self.curState == CurState.CalibrateColors_Confirm):
            if(self.CalibrateEnd==False):
                self.curState = CurState.CalibrateColors
                self.CountDown_Flag = True
                self.start_time = datetime.now()
            else:
                self.CountDown_Flag = False
                self.curState = CurState.OriginalColor_Detect
                self.ui.Text3_Instruction.setText("颜色校准完成")
        if(self.CountDown_Flag == False and self.curState == CurState.OriginalColor_Confirm and self.CenterCorret_Flag == True):
            if(self.curDetect <= 5):
                self.curState = CurState.OriginalColor_Detect
                self.CountDown_Flag = True
                self.start_time = datetime.now()
                if(self.DetecteDone_Flag):
                    self.curDetect += 1
                    self.Stickers = [0,0,0,0,0,0,0,0,0]
            elif(self.curDetect == 6):
                self.OriginalDetectDone_Flag = True
                self.curState = CurState.OriginalColor_Done
                self.ui.Text3_Instruction.setText("识别完毕")
                self.ui.Text15_Chosemethod.show()
                self.ui.Button_Beginner.show()
                self.ui.Button_Kociemba.show()
                print("识别完毕")
            else:
                pass
        # if(self.CountDown_Flag == False and self.curState == CurState.OriginalColor_Done and self.OriginalCorrect):
        #     self.curState = CurState.ProgressColor_Start
            
        if(self.curState == CurState.ProgressColor_Start and self.ProcessReady_Flag):
            self.curState = CurState.ProgressColor_Detect
            self.ui.Text6_CurStep.show()
            self.ui.Text7_NextStep.show()
        if(self.curState == CurState.ProgressColor_Detect):
            pass

    def Button_Retry_Clicked(self):
        # print('click')
        if(self.CountDown_Flag == False and self.curState == CurState.OriginalColor_Confirm and self.OriginalDetectDone_Flag == False):
            self.curState = CurState.OriginalColor_Detect
            self.CountDown_Flag = True
            self.start_time = datetime.now()
    
    def Button_Restart_Clicked(self):
        # print('click')
        # self.ui.Text0_Welcome.show()
        # self.ui.Text3_Instruction.setText("提示信息")
        # self.ui.Text5_Resolution.setText("")
        # self.sendCube2D.emit(self.Cube2D)
        # self.MyInit()
        self.restart_program()

    def Button_Beginner_Clicked(self):
        if(self.curState == CurState.OriginalColor_Done):
            self.Solvemethod = Solvemethod.Beginner_method
            self.ui.Button_Beginner.close()
            self.ui.Button_Kociemba.close()
            self.ui.Text15_Chosemethod.close()
            
    def Button_Kociemba_Clicked(self):
        if(self.curState == CurState.OriginalColor_Done):
            self.Solvemethod = Solvemethod.K_method
            self.ui.Button_Beginner.close()
            self.ui.Button_Kociemba.close()
            self.ui.Text15_Chosemethod.close()
            
    def updateWindow(self):
       self.openGLWidget.updateGL()

    def slot_init(self):
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_camera.isActive()
        self.cap.open(0)
        self.show_camera()
        self.updateWindow()

        self.timer_opengl.timeout.connect(self.openGLWidget.MyUpdateGL)
        self.timer_opengl.isActive()
        self.timer_opengl.start(30)


        self.sendCube2D.connect(self.openGLWidget.receiveCube)
        self.sendStep.connect(self.openGLWidget.receiveStep)
        
    def addSolidColors(self):
        random.seed()
        HSVRange_Yellow = [26, 37, 43, 256, 46, 256]
        HSVRange_Red = [-1, 8, 43, 256, 46, 256]
        HSVRange_Red2 = [156, 180, 43, 256, 46, 256]
        HSVRange_Green = [55, 80, 43, 256, 46, 256]
        HSVRange_Orange = [8, 25, 43, 256, 46, 256]
        HSVRange_Blue = [90, 124, 43, 256, 46, 256]
        HSVRange_White = [0, 180, 0, 60, 150, 256]
        for i in range(1,7):
            for j in range(16):
                if(i == 1):
                    h=random.randint(HSVRange_Yellow[0], HSVRange_Yellow[1])
                    s=random.randint(HSVRange_Yellow[2], HSVRange_Yellow[3])
                    v=random.randint(HSVRange_Yellow[4], HSVRange_Yellow[5])
                    t=186 + (i-1)*15 + j
                    self.colorX[t] = [h,s,v]
                    self.colorY[t] = i
                if(i == 2):
                    h=random.randint(HSVRange_Blue[0], HSVRange_Blue[1])
                    s=random.randint(HSVRange_Blue[2], HSVRange_Blue[3])
                    v=random.randint(HSVRange_Blue[4], HSVRange_Blue[5])
                    t=186 + (i-1)*15 + j
                    self.colorX[t] = [h,s,v]
                    self.colorY[t] = i
                if(i == 3):
                    if(j<8):
                        h=random.randint(HSVRange_Red[0], HSVRange_Red[1])
                        s=random.randint(HSVRange_Red[2], HSVRange_Red[3])
                        v=random.randint(HSVRange_Red[4], HSVRange_Red[5])
                    else:
                        h=random.randint(HSVRange_Red2[0], HSVRange_Red2[1])
                        s=random.randint(HSVRange_Red2[2], HSVRange_Red2[3])
                        v=random.randint(HSVRange_Red2[4], HSVRange_Red2[5])
                    t=186 + (i-1)*15 + j
                    self.colorX[t] = [h,s,v]
                    self.colorY[t] = i
                if(i == 4):
                    h=random.randint(HSVRange_Green[0], HSVRange_Green[1])
                    s=random.randint(HSVRange_Green[2], HSVRange_Green[3])
                    v=random.randint(HSVRange_Green[4], HSVRange_Green[5])
                    t=186 + (i-1)*15 + j
                    self.colorX[t] = [h,s,v]
                    self.colorY[t] = i
                if(i == 5):
                    h=random.randint(HSVRange_Orange[0], HSVRange_Orange[1])
                    s=random.randint(HSVRange_Orange[2], HSVRange_Orange[3])
                    v=random.randint(HSVRange_Orange[4], HSVRange_Orange[5])
                    t=186 + (i-1)*15 + j
                    self.colorX[t] = [h,s,v]
                    self.colorY[t] = i
                if(i == 6):
                    h=random.randint(HSVRange_White[0], HSVRange_White[1])
                    s=random.randint(HSVRange_White[2], HSVRange_White[3])
                    v=random.randint(HSVRange_White[4], HSVRange_White[5])
                    t=186 + (i-1)*15 + j
                    self.colorX[t] = [h,s,v]
                    self.colorY[t] = i

    def show_camera(self):
        is_ok, bgr_image_input = self.cap.read()
        bgr_image_input=np.fliplr(bgr_image_input.copy())
        ret,image = self.cap.read()
        image = image
        x,y = image.shape[0:2]
        image = cv2.resize(image, (int(y/2),int(x/2)))
        b,g,r = cv2.split(image)
        recnum = 0
        cords = [[0 for col in range(2)] for row in range(9)]
        dilation = process(image)
        
        contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.12*cv2.arcLength(cnt,True),True)
            x = approx.ravel()[0]
            y = approx.ravel()[1]

            if (len(approx) == 4 and 90<x<210 and 60<y<180):
                #Approx has 4 (x,y) coordinates, where the first is the top left,and
                #the third is the bottom right. Findind the mid point of these two coordinates
                #will give me the center of the rectangle
                recnum = recnum + 1
                
                x1=approx[0,0,0]
                y1=approx[0,0,1]
                x2=approx[(approx.shape[0]-2),0,0] #X coordinate of the bottom right corner
                y2=approx[(approx.shape[0]-2),0,1] 
                
                xavg = int((x1+x2)/2)
                yavg = int((y1+y2)/2)

                if (recnum > 9):
                    break
                cords = list(cords)
                cords[recnum-1] = [xavg,yavg]
                
                if (approx_is_square(approx) == True and self.noCircle == False):
                    
                    cv2.circle(image,(xavg,yavg),15,(255,255,255),5)
                    #cv2.putText(image,str(b[yavg,xavg])+str(g[yavg,xavg])+str(r[yavg,xavg]),(100,recnum*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))
                    #cv2.drawContours(image, [approx],0,(0,0,255),2)
                if (recnum == 9 and approx_is_square(approx) == True):
                    string = get_string(cords)
                    color_string = get_average_color(image,string)
                    self.color_s = color_string
                    thecolor = get_color_string(color_string)
                    
                    create_referrence_color(image,thecolor)
        draw_aim(image,90,60,210,180,20,20,20,20)
        image_output = image.copy()
        #开始部分
        if(self.curState == CurState.Start):
            text = "欢迎使用魔方教学系统！\n\n\n1.请在明亮的自然环境光下识别魔方\n2.请确保摄像机连接正确，并将摄像机平放在桌面上，镜头朝向正前方\n3.请注意阅读画面上方的提示\n4.如果还原过程中发现自己转错了请点击“重新开始”按钮\n\n点击“确认”按钮开始识别！"
            self.ui.Text0_Welcome.setText(text)
            self.ui.Text5_Resolution.close()
            self.ui.Text6_CurStep.close()
            self.ui.Text7_NextStep.close()
            self.ui.Text9_Judge.close()
            self.ui.Text10_Notification.close()
            self.ui.Text12_NamePair.close()
            self.ui.Text13_CurLayer.close()
            self.ui.Text14_CurFormula.close()
            self.ui.Button_Beginner.close()
            self.ui.Button_Kociemba.close()
            self.ui.Text15_Chosemethod.close()
        #倒计时
        if(self.CountDown_Flag):
            self.ui.Text4_CountDown.show()
            if (datetime.now() - self.start_time).total_seconds() < 1:
                self.ui.Text4_CountDown.setText('3')
            elif 1 < (datetime.now() - self.start_time).total_seconds() < 2:
                self.ui.Text4_CountDown.setText('2')
            elif 2 < (datetime.now() - self.start_time).total_seconds() < 3:
                self.ui.Text4_CountDown.setText('1')
            elif (datetime.now() - self.start_time).total_seconds()>3:
                self.ui.Text4_CountDown.setText('')
                self.CountDown_Flag = False
        else:
            self.ui.Text4_CountDown.close()
            
        #校准颜色
        if(self.CountDown_Flag == False and self.curState == CurState.CalibrateColors):
            if(self.curDetect>=7):
                self.knn.fit(self.colorX, self.colorY)  # 训练KNN分类器
                self.curDetect = 1
                self.CalibrateEnd = True
                self.curState = CurState.OriginalColor_Detect
            if (recnum != 9):
                pass      
            elif(self.curDetect<7):
                if(self.index<=30):
                    h,s,v=Fc.getCenterHSV(self.color_s)
                    print([h[0][0],s[0][0],v[0][0]])
                    t = (self.curDetect-1) * 30 + self.index
                    self.colorX[t] = [h[0][0],s[0][0],v[0][0]]
                    self.colorY[t] = self.curDetect
                    self.index += 1
                    print(self.index)
                    print(self.colorX[t])

                if(self.index>30):
                    self.curState = CurState.CalibrateColors_Confirm
                    self.curDetect += 1
        #确认校准
        if(self.CountDown_Flag == False and self.curState == CurState.CalibrateColors_Confirm):
            self.ui.Text3_Instruction.setText("校准完毕，点击确认进行下一面的颜色校准")
            self.ui.Text3_Instruction.setStyleSheet('''font-family:DengXian;color: red;font-size = 24pt;''')
            self.color_s =[[0 for col in range(5)] for face in range(9)]
            self.index=0
            
        #初始识别
        if(self.CountDown_Flag == False and self.curState == CurState.OriginalColor_Detect):
            image_output1,contours = ImgInput.DrawContours(image_output)
            facesList,blob_colors,self.DetecteDone_Flag,self.CenterCorret_Flag,self.detected_face = ImgInput.DetectFace(self.faces,bgr_image_input,contours,self.curDetect,self.color_s,self.knn)
            self.color_s =[[0 for col in range(5)] for face in range(9)]
            self.faces = facesList
            if(self.DetecteDone_Flag):
                # print(self.Cube2D.up_face)
                self.faces = []
                self.Cube2D.DetectFace(self.detected_face,self.curDetect)
                if(self.curDetect<7):
                    self.curState = CurState.OriginalColor_Confirm
        
            if(len(self.detected_face)!= 0):
                for i in range(len(self.Stickers)):
                    if(self.Stickers[i] != self.detected_face[0][i]):
                        self.Stickers[i] = self.detected_face[0][i]
                    else:
                        pass
            self.sendCube2D.emit(self.Cube2D)
        #初始确认
        if(self.CountDown_Flag == False and self.curState == CurState.OriginalColor_Confirm):
            image_output1,contours = ImgInput.DrawContours(bgr_image_input)
            self.color_s =[[0 for col in range(5)] for face in range(9)]
            self.detected_face[0]=self.receiveChange(self.detected_face[0])
            if(self.curDetect <=6):
                if(self.CenterCorret_Flag == True):
                    self.ui.Text3_Instruction.setText("请确认识别结果")
                    self.ui.Text3_Instruction.setStyleSheet('''font-family:DengXian;color: red;font-size = 24pt;''')
                else:
                    self.ui.Text3_Instruction.setText("中心块颜色错误！请点击 “重试” 再次识别")
                    self.ui.Text3_Instruction.setStyleSheet('''font-family:DengXian;color: red;font-size = 50pt;''')
            else:
                self.ui.Text3_Instruction.setText("识别完毕")
        #初始完成
        if(self.curState == CurState.OriginalColor_Done):
            if(self.Solvemethod == Solvemethod.UnChoose):
                solved,self.steps,CalculateDone_Flag = self.Cube2D.CalculateSolution()
                if(CalculateDone_Flag):
                    self.ui.Text3_Instruction.setText("初始魔方已识别完毕，还原步骤计算成功！")
                    self.OriginalCorrect = True
                else:
                    self.ui.Text3_Instruction.setText("识别结果不构成标准魔方！请检查并重新开始！")
            elif(self.Solvemethod == Solvemethod.Beginner_method):
                self.solve_cross,self.solve_corners,self.solve_second_layer,self.oll_step_1,self.oll_step_2,self.pll_step_1,self.pll_step_2,res,solution = BeginnerSolver.solveCube_BeginnerSolver(self.Cube2D)
                self.steps = solution
                text = "层先法还原步骤：\n" + res
                self.ui.Text5_Resolution.setText(text)
                self.ui.Text5_Resolution.show()
                self.curState = CurState.ProgressColor_Start
            elif(self.Solvemethod == Solvemethod.K_method):
                solved,self.steps,CalculateDone_Flag = self.Cube2D.CalculateSolution()
                text = "快速还原步骤：\n" + solved
                self.ui.Text5_Resolution.setText(text)
                self.ui.Text5_Resolution.show()
                self.curState = CurState.ProgressColor_Start

        #还原准备
        if(self.curState == CurState.ProgressColor_Start):
            self.ui.Text3_Instruction.setText("请保持黄色中心块向上，展示蓝色F面后点击确定开始")
            self.ProcessReady_Flag = True
            self.NextMove_Flag = True
            self.noCircle=True

        if(self.CountDown_Flag == False and self.curState == CurState.ProgressColor_Detect):
            self.ui.Text9_Judge.close()
            ###########################Kociemba算法还原##############################
            if(self.Solvemethod == Solvemethod.K_method):
                try:
                    step = self.steps[self.curStep]
                    if(self.SendStep_Flag):
                        self.sendStep.emit(step)
                        self.SendStep_Flag = False
                except:
                    pass
                self.ui.Text6_CurStep.setText("当前步骤：" + step)
                self.ui.Text3_Instruction.setText(Op.DrawInstructionText(step))
                NextStep = self.curStep + 1
                try:
                    self.ui.Text7_NextStep.setText("下一步骤：" + self.steps[NextStep])
                except:
                    self.ui.Text7_NextStep.setText("没有下一步了，完成")
                if(self.NextMove_Flag):
                    self.Cube2D_temp = self.Cube2D.copy()
                    self.Cube2D_temp= Cube2D.PreOperation(step,self.Cube2D_temp)
                    self.NextMove_Flag = False
                image_output1,contours = ImgInput.DrawContours(bgr_image_input)
                # is_ok, bgr_image_input = self.cap.read()
                facesList,blob_colors,self.DetecteDone_Flag,self.CenterCorret_Flag,self.detected_face = ImgInput.DetectFace(self.faces,bgr_image_input,contours,self.curDetect,self.color_s,self.knn)
                self.color_s =[[0 for col in range(5)] for face in range(9)]
                self.faces = facesList
                if(self.DetecteDone_Flag):
                    if(len(self.detected_face)!= 0):
                        for i in range(len(self.Stickers)):
                            if(self.Stickers[i] != self.detected_face[0][i]):
                                self.Stickers[i] = self.detected_face[0][i]
                            else:
                                pass
                    # print(self.Cube2D.up_face)
                    self.faces = []
                    self.MoveDone_Flag,self.Condition,self.NeedTurn_Flag = Op.Condition(self.NeedTurn_Flag,self.MoveDone_Flag,step,self.detected_face[0],self.Cube2D_temp,self.Cube2D)
                    if(self.MoveDone_Flag == True and self.NeedTurn_Flag == False):
                        if(self.Cube2D_temp.check()):
                            self.Cube2D = self.Cube2D_temp.copy()
                            self.curState = CurState.ProgressColor_Done
                        else:
                            self.curStep += 1
                            try:
                                step = self.steps[self.curStep]
                            except:
                                pass
                            self.ui.Text6_CurStep.setText("当前步骤：" + step)
                            self.ui.Text3_Instruction.setText(Op.DrawInstructionText(step))
                            NextStep = self.curStep + 1
                            try:
                                self.ui.Text7_NextStep.setText("下一步骤：" + self.steps[NextStep])
                            except:
                                self.ui.Text7_NextStep.setText("没有下一步了，完成")
                            self.Cube2D = self.Cube2D_temp.copy()
                            self.NextMove_Flag = True
                            self.MoveDone_Flag = False
                            self.ui.Text9_Judge.setText("成功！")
                            self.ui.Text9_Judge.show()
                            self.CountDown_Flag = True
                            self.start_time = datetime.now()
                            self.SendStep_Flag = True
                    elif self.MoveDone_Flag == False or self.NeedTurn_Flag:
                        image_output = Fc.DrawInstruction(image_output,blob_colors,self.Condition)

            ###########################Kociemba算法还原##############################
            if(self.Solvemethod == Solvemethod.Beginner_method):
                self.ui.Text13_CurLayer.show()
                self.ui.Text14_CurFormula.show()
                if(self.BeginnerState[self.curLayer] == CurLayer.Cross):
                    self.steps = self.solve_cross
                    self.ui.Text13_CurLayer.setText("当前正在进行：底层十字还原")
                    self.ui.Text14_CurFormula.setText("该阶段没有固定公式")
                elif(self.BeginnerState[self.curLayer] == CurLayer.Corner):
                    self.steps = self.solve_corners
                    self.ui.Text13_CurLayer.setText("当前正在进行：底层角块还原")
                    self.ui.Text14_CurFormula.setText("该阶段的公式：F` U` F 或 R U R` 或 R U U R` U` + R U R`")
                elif(self.BeginnerState[self.curLayer] == CurLayer.Second_layer):
                    self.steps = self.solve_second_layer
                    self.ui.Text13_CurLayer.setText("当前正在进行：二层还原")
                    self.ui.Text14_CurFormula.setText("该阶段的公式：U R U` R` U` F` U F 或 U` L` U L U F U` F`")
                elif(self.BeginnerState[self.curLayer] == CurLayer.oll_step_1):
                    self.steps = self.oll_step_1
                    self.ui.Text13_CurLayer.setText("当前正在进行：获得顶层黄色十字")
                    self.ui.Text14_CurFormula.setText("该阶段的公式：F R U R` U` F`")
                elif(self.BeginnerState[self.curLayer] == CurLayer.oll_step_2):
                    self.steps = self.oll_step_2
                    self.ui.Text13_CurLayer.setText("当前正在进行：获得全部顶层黄色")
                    self.ui.Text14_CurFormula.setText("该阶段的公式：R U R` U R U2 R`")
                elif(self.BeginnerState[self.curLayer] == CurLayer.pll_step_1):
                    self.steps = self.pll_step_1
                    self.ui.Text13_CurLayer.setText("当前正在进行：顶层角块还原")
                    self.ui.Text14_CurFormula.setText("该阶段的公式：'R U R` U` R` F R2 U` R` U` R U R` F`")
                elif(self.BeginnerState[self.curLayer] == CurLayer.pll_step_2):
                    self.steps = self.pll_step_2
                    self.ui.Text13_CurLayer.setText("当前正在进行：顶层棱块还原")
                    self.ui.Text14_CurFormula.setText("该阶段的公式：R2 U R U R` U` R` U` R` U R`")                                 
                try:
                    step = self.steps[self.curStep]
                    if(self.SendStep_Flag):
                        self.sendStep.emit(step)
                        self.SendStep_Flag = False
                except:
                    self.curLayer += 1
                    self.curStep = 0
                    step = ''
                if(step != ''):    
                    self.ui.Text6_CurStep.setText("当前步骤：" + step)
                    self.ui.Text3_Instruction.setText(Op.DrawInstructionText_2(step))
                    NextStep = self.curStep + 1
                    try:
                        self.ui.Text7_NextStep.setText("下一步骤：" + self.steps[NextStep])
                    except:
                        self.ui.Text7_NextStep.setText("没有下一步了，完成")
                    if(self.NextMove_Flag):
                        self.Cube2D_temp = self.Cube2D.copy()
                        self.Cube2D_temp= Cube2D.PreOperation(step,self.Cube2D_temp)
                        if(step == 'mL' or step == 'mR'):
                            self.sendCube2D.emit(self.Cube2D_temp)
                            text = self.setNamepair(self.Cube2D_temp)
                            self.ui.Text12_NamePair.setText(text)
                        self.NextMove_Flag = False
                    image_output1,contours = ImgInput.DrawContours(bgr_image_input)
                    image_output = image.copy()
                    # is_ok, bgr_image_input = self.cap.read()
                    facesList,blob_colors,self.DetecteDone_Flag,self.CenterCorret_Flag,self.detected_face = ImgInput.DetectFace(self.faces,bgr_image_input,contours,self.curDetect,self.color_s)
                    self.faces = facesList
                    if(self.DetecteDone_Flag):
                        if(len(self.detected_face)!= 0):
                            for i in range(len(self.Stickers)):
                                if(self.Stickers[i] != self.detected_face[0][i]):
                                    self.Stickers[i] = self.detected_face[0][i]
                                else:
                                    pass
                        # print(self.Cube2D.up_face)
                        self.faces = []
                        self.MoveDone_Flag,self.Condition,self.NeedTurn_Flag = Op.Condition(self.NeedTurn_Flag,self.MoveDone_Flag,step,self.detected_face[0],self.Cube2D_temp,self.Cube2D)
                        if(self.MoveDone_Flag == True and self.NeedTurn_Flag == False):
                            if(self.Cube2D_temp.check()):
                                self.Cube2D = self.Cube2D_temp.copy()
                                self.curState = CurState.ProgressColor_Done
                            else:
                                self.curStep += 1
                                try:
                                    step = self.steps[self.curStep]
                                except:
                                    pass
                                self.ui.Text6_CurStep.setText("当前步骤：" + step)
                                self.ui.Text3_Instruction.setText(Op.DrawInstructionText_2(step))
                                NextStep = self.curStep + 1
                                try:
                                    self.ui.Text7_NextStep.setText("下一步骤：" + self.steps[NextStep])
                                except:
                                    self.ui.Text7_NextStep.setText("没有下一步了，完成")
                                self.Cube2D = self.Cube2D_temp.copy()
                                self.NextMove_Flag = True
                                self.MoveDone_Flag = False
                                self.ui.Text9_Judge.setText("成功！")
                                self.ui.Text9_Judge.show()
                                self.CountDown_Flag = True
                                self.start_time = datetime.now()
                                self.SendStep_Flag = True
                        elif self.MoveDone_Flag == False or self.NeedTurn_Flag:
                            image_output = Fc.DrawInstruction(image_output,blob_colors,self.Condition)                
        if(self.curState == CurState.ProgressColor_Done):
            self.ui.Text3_Instruction.setText("还原结束。点击重新开始识别新的魔方！")
        
        self.DrawSticker(self.DrawStickersArea,self.Stickers)
        self.DrawCube2D(self.DrawCube2DArea)
        self.DrawInstructionText(self.curDetect)
        self.timer_camera.start(30)
        
        if(is_ok):
            show = cv2.resize(image_output,(1280,960))
            show = cv2.cvtColor(show,cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(show.data,show.shape[1],show.shape[0],QtGui.QImage.Format_RGB888)
            self.ui.Label_ImgInput.setPixmap(QtGui.QPixmap.fromImage(showImage))
            self.ui.Label_ImgInput.setScaledContents(True)

    def receiveChange(self,detected_face):
        global labelSig,clickFlag
        print(labelSig)
        if(clickFlag):
            c = labelSig - 1
            if(c in range(0,9)):
                detected_face[c] += 1
                if(detected_face[c] == 7):
                    detected_face[c] = 1
            clickFlag = False
            print(c)
            self.Cube2D.DetectFace([detected_face],self.curDetect)
            for i in range(len(self.Stickers)):
                if(self.Stickers[i] != detected_face[i]):
                    self.Stickers[i] = detected_face[i]
                else:
                    pass
            self.sendCube2D.emit(self.Cube2D)
        return detected_face
            
    def DrawSticker(self,DrawStickersArea,detected_face):
        Sticker = Fc.draw_stickers(DrawStickersArea,detected_face,0,0)
        Sticker = cv2.cvtColor(Sticker,cv2.COLOR_BGR2RGB)
        showSticker = QtGui.QImage(Sticker.data,Sticker.shape[1],Sticker.shape[0],Sticker.shape[1] * 3,QtGui.QImage.Format_RGB888)
        self.ui.Label_DrawSticker.setPixmap(QtGui.QPixmap.fromImage(showSticker))
    
    def DrawCube2D(self,DrawCube2DArea):
        Cube2D= Fc.concat(self.Cube2D.up_face, self.Cube2D.right_face, self.Cube2D.front_face, self.Cube2D.down_face, self.Cube2D.left_face, self.Cube2D.back_face)
        Sticker = Fc.draw_2d_cube_state(DrawCube2DArea,Cube2D)
        Sticker = cv2.cvtColor(Sticker,cv2.COLOR_BGR2RGB)
        showSticker = QtGui.QImage(Sticker.data,Sticker.shape[1],Sticker.shape[0],Sticker.shape[1] * 3,QtGui.QImage.Format_RGB888)
        self.ui.Label_DrawAllSticker.setPixmap(QtGui.QPixmap.fromImage(showSticker))
    
    def DrawInstructionText(self,curDetect):
        if(self.curState == CurState.OriginalColor_Detect):
            if(curDetect == 1):
                text = '展示中心块为黄色的Up面（绿色中心块朝上） 1/6'
            elif(curDetect == 2):
                text = '展示中心块为蓝色的Front面（黄色中心块朝上） 2/6'
            elif(curDetect == 3):
                text = '展示中心块为红色的Right面（黄色中心块朝上） 3/6'
            elif(curDetect == 4):
                text = '展示中心块为绿色的Back面（黄色中心块朝上） 4/6'
            elif(curDetect == 5):
                text = '展示中心块为橙色的Left面（黄色中心块朝上） 5/6'
            elif(curDetect == 6):
                text = '展示中心块为白色的Down面（蓝色中心块朝上） 6/6'
            else:
                text = '识别完毕'
            self.ui.Text3_Instruction.setText(text)
        elif(self.curState == CurState.CalibrateColors):
            if(curDetect == 1):
                text = '展示中心块为黄色的Up面 1/6'
            elif(curDetect == 2):
                text = '展示中心块为蓝色的Front面 2/6'
            elif(curDetect == 3):
                text = '展示中心块为红色的Right面 3/6'
            elif(curDetect == 4):
                text = '展示中心块为绿色的Back面 4/6'
            elif(curDetect == 5):
                text = '展示中心块为橙色的Left面 5/6'
            elif(curDetect == 6):
                text = '展示中心块为白色的Down面 6/6'
            else:
                text = '展示中心块为黄色的Up面（绿色中心块朝上） 1/6'
            self.ui.Text3_Instruction.setText(text)
    def setNamepair(self,Cube2D):
        CenterColor = [Cube2D.mu,Cube2D.md,Cube2D.ml,Cube2D.mr,Cube2D.mf,Cube2D.mb]
        ColorStr = []
        for color in CenterColor:
            if(color == 1):
                ColorStr.append("黄色")
            elif(color == 2):
                ColorStr.append("蓝色")
            elif(color == 3):
                ColorStr.append("红色")
            elif(color == 4):
                ColorStr.append("绿色")
            elif(color == 5):
                ColorStr.append("橙色")
            elif(color == 6):
                ColorStr.append("白色")
        FinalStr = "U-Up   （上，" + ColorStr[0] + "）\nD-Down （下，" + ColorStr[1] + "）\nL-Left （左，"+ColorStr[2]+"）\nR-Right（右，"+ ColorStr[3] + "）\nF-Front（前，"+ColorStr[4]+"）\nB-Back （后，"+ColorStr[5]+"）"
        return FinalStr
class MyGLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.inc_x = 0
        self.inc_y = 0
        self.accum = (1, -0.2, 0.2, 0)
        self.zoom = 1
        self.theta_x = 0
        # self.setMouseTracking(True)
        self.Cube = Cube2D.Cube2D()
        self.Step = ""
        self.Move_Flag = False
        self.theta_inc = 10
        self.theta = pi / 2 / self.theta_inc
    @Slot(object)
    def receiveCube(self,receiveCube):
        self.Cube = receiveCube.copy()
        # print(self.Cube.front_face)
    @Slot(object)
    def receiveStep(self,receiveStep):
        self.Step = receiveStep
        self.Move_Flag = True
        self.theta_inc = 10
        self.theta = pi / 2 / self.theta_inc
        self.theta = DrawCube3D.Direction(self.Step,self.theta)
        self.theta_x = 0
        
    def initializeGL(self):
        QtOpenGL.QGLWidget.makeCurrent(self)
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glutInit()
        gluLookAt(0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0)
        glLoadIdentity()
        glMatrixMode(GL_PROJECTION)
        width = self.width()
        height = self.height()
        gluPerspective(45, (width/height), 0.5, 40)
        glTranslatef(0.0, 0.0, -17.5)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if self.theta_x < self.theta_inc:
            self.Move_Flag = DrawCube3D.draw_Step(self.Step,self.Move_Flag,self.theta)
            self.theta_x += 1
        self.rot_x = normalize(axisangle_to_q((1.0, 0.0, 0.0), self.inc_x))
        self.rot_y = normalize(axisangle_to_q((0.0, 1.0, 0.0), self.inc_y))
        self.accum = q_mult(self.accum, self.rot_x)
        self.accum = q_mult(self.accum, self.rot_y)

        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(q_to_mat4(self.accum))
        glScalef(self.zoom, self.zoom, self.zoom)
        glViewport(0, 0, self.width(),self.height())
        # print("DrawCube")
        DrawCube3D.draw_cube(self.Cube)
    
    def resizeGL(self,w,h):
        self.rot_x = normalize(axisangle_to_q((1.0, 0.0, 0.0), self.inc_x))
        self.rot_y = normalize(axisangle_to_q((0.0, 1.0, 0.0), self.inc_y))
        self.accum = q_mult(self.accum, self.rot_x)
        self.accum = q_mult(self.accum, self.rot_y)

        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(q_to_mat4(self.accum))
        # print(q_to_mat4(self.accum))
        glScalef(self.zoom, self.zoom, self.zoom)
        glViewport(0, 0, w,h)

    def MyUpdateGL(self):
        # print("update")
        # self.Cube = cube.copy()
        self.updateGL()
        
    def mouseMoveEvent(self,event):
        # print("MouseEvent")
        pos = event.pos()
        tmp_x,tmp_y= pos.x(),pos.y() 
        tmp_x = self.width()/2 - tmp_x
        tmp_y = self.height()/2 - tmp_y
        self.inc_x = tmp_y * pi / 3000
        self.inc_y = tmp_x * pi / 3000
    def mouseReleaseEvent(self,event):
        self.inc_x = 0
        self.inc_y = 0
    def mouseDoubleClickEvent(self,event):
        self.inc_x = 0
        self.inc_y = 0
        self.accum = (1, -0.2, 0.2, 0)

# 程序入口
if __name__ == "__main__":
    os.environ['QT_SCALE_FACTOR']="0.5"
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())