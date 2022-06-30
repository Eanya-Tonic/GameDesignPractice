import numpy as np
import cv2
from cv2 import COLOR_BGR2HSV
import Operation as Op

STICKER_AREA_SIZE_MIN = 7000
STICKER_AREA_SIZE_MAX = 9000

#将每一个面所行成的矩阵全部连接起来，用于输入换原魔方函数中
def concat(up_face, right_face, front_face, down_face, left_face, back_face):
    solution = np.concatenate((up_face, right_face), axis=None)
    solution = np.concatenate((solution, front_face), axis=None)
    solution = np.concatenate((solution, down_face), axis=None)
    solution = np.concatenate((solution, left_face), axis=None)
    solution = np.concatenate((solution, back_face), axis=None)
    return solution

#获得的RGB通过Knn数据集，获得HSV的值，返回对应的6种颜色
def color(bgrlist, knn):
    """
    Takes a tuple input that has (b,g,r) and return the color of that pixel
    """

    bgrtuple = list(tuple(bgrlist))

    b = bgrtuple[0]
    g = bgrtuple[1]
    r = bgrtuple[2]

    imgBGR = np.dstack([b, g, r])
    print(b, g, r)
    hsv_image_input = cv2.cvtColor(imgBGR.astype(np.uint8), COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_image_input)
    colorPred = knn.predict(
        np.array([h[0][0], s[0][0], v[0][0]]).reshape(1, -1))

    if (colorPred[0] == 6):
        return "white"
    elif (colorPred[0] == 1):
        return "yellow"
    elif (colorPred[0] == 2):
        return "blue"
    elif (colorPred[0] == 3):
        return "red"
    elif (colorPred[0] == 4):
        return "green"
    elif (colorPred[0] == 5):
        return "orange"
    else:
        return "grey"

    """
    if (h in range(HSVRange_White[0], HSVRange_White[1])) and (s in range(HSVRange_White[2], HSVRange_White[3])) and (v in range(HSVRange_White[4], HSVRange_White[5])):
        return "white"
    elif (h in range(HSVRange_Yellow[0], HSVRange_Yellow[1])) and (s in range(HSVRange_Yellow[2], HSVRange_Yellow[3])) and (v in range(HSVRange_Yellow[4], HSVRange_Yellow[5])):
        return "yellow"
    elif (h in range(HSVRange_Blue[0], HSVRange_Blue[1])) and (s in range(HSVRange_Blue[2], HSVRange_Blue[3])) and (v in range(HSVRange_Blue[4], HSVRange_Blue[5])):
        return "blue"
    elif ((h in range(HSVRange_Red[0], HSVRange_Red[1])) or (h in range(HSVRange_Red2[0], HSVRange_Red2[1]))) and (s in range(HSVRange_Red[2], HSVRange_Red[3])) and (v in range(HSVRange_Red[4], HSVRange_Red[5])):
        return "red"
    elif (h in range(HSVRange_Green[0], HSVRange_Green[1])) and (s in range(HSVRange_Green[2], HSVRange_Green[3])) and (v in range(HSVRange_Green[4], HSVRange_Green[5])):
        return "green"
    elif (h in range(HSVRange_Orange[0], HSVRange_Orange[1])) and (s in range(HSVRange_Orange[2], HSVRange_Orange[3])) and (v in range(HSVRange_Orange[4], HSVRange_Orange[5])):
        return "orange"
    else:
        return "grey"
    """
    # #if (r >100 and  r*1.3> g > r*0.9 and r*0.9>b>r*0.7):
    # if (-60 < r-g < 60 and 55<r-b<105):
    #     return "yellow"
    # if (r>180 and g<r*0.5 and b< r*0.5):
    #     return "red"
    # if (r-g>20 and r-b>20):
    #     return "orange"
    # if (g-b>30 and g-r>30):
    # #if (g>120 and r <120 and b <120):
    #     return "green"
    # if (b-r >30 and b - g >30):
    #     return "blue"
    # if (g*1.2>r>g*0.8 and g*1.2>b>g*0.8):
    #     return "white"
    # else:
    #     return "grey"



# 获取中心颜色的HSV
def getCenterHSV(bgrlist):
    bgrtuple = list(tuple(bgrlist[4]))

    b = bgrtuple[0]
    g = bgrtuple[1]
    r = bgrtuple[2]

    imgBGR = np.dstack([b, g, r])
    hsv_image_input = cv2.cvtColor(imgBGR.astype(np.uint8), COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_image_input)
    return h, s, v

#识别当前面的颜色
def detect_face(bgr_image_input, contours, bgrlist, knn):
    i = 0
    contour_id = 0
    face = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    blob_colors = np.zeros((10, 6), dtype=int)
    if 1:
        # print(blob_colors)
        result_string = ["hi" for face in range(9)]
        running = 0
        while (running < 9):
            bgrstring = bgrlist[running]
            try:
                blob_colors[running][4] = bgrstring[3]
                blob_colors[running][5] = bgrstring[4]
            except:
                pass
            result_string[running] = color(bgrstring, knn)
            running = running+1
        for i in range(0, 9):  # 比较HSV颜色值分辨颜色
            if(result_string[i] == "white"):
                blob_colors[i][3] = 6
                face[i] = 6
            elif(result_string[i] == "yellow"):
                blob_colors[i][3] = 1
                face[i] = 1
            elif(result_string[i] == "blue"):
                blob_colors[i][3] = 2
                face[i] = 2
            elif(result_string[i] == "red"):
                blob_colors[i][3] = 3
                face[i] = 3
            elif(result_string[i] == "green"):
                blob_colors[i][3] = 4
                face[i] = 4
            elif(result_string[i] == "orange"):
                blob_colors[i][3] = 5
                face[i] = 5

            # if (blob_colors[i][0] in range(HSVRange_White[0], HSVRange_White[1])) and (blob_colors[i][1] in range(HSVRange_White[2], HSVRange_White[3])) and (blob_colors[i][2] in range(HSVRange_White[4], HSVRange_White[5])):
            #     blob_colors[i][3] = 6
            #     face[i] = 6
            # elif (blob_colors[i][0] in range(HSVRange_Yellow[0], HSVRange_Yellow[1])) and (blob_colors[i][1] in range(HSVRange_Yellow[2], HSVRange_Yellow[3])) and (blob_colors[i][2] in range(HSVRange_Yellow[4], HSVRange_Yellow[5])):
            #     blob_colors[i][3] = 1
            #     face[i] = 1
            # elif (blob_colors[i][0] in range(HSVRange_Blue[0], HSVRange_Blue[1])) and (blob_colors[i][1] in range(HSVRange_Blue[2], HSVRange_Blue[3])) and (blob_colors[i][2] in range(HSVRange_Blue[4], HSVRange_Blue[5])):
            #     blob_colors[i][3] = 2
            #     face[i] = 2
            # elif (blob_colors[i][0] in range(HSVRange_Red[0], HSVRange_Red[1])) and (blob_colors[i][1] in range(HSVRange_Red[2], HSVRange_Red[3])) and (blob_colors[i][2] in range(HSVRange_Red[4], HSVRange_Red[5])):
            #     blob_colors[i][3] = 3
            #     face[i] = 3
            # elif (blob_colors[i][0] in range(HSVRange_Green[0], HSVRange_Green[1])) and (blob_colors[i][1] in range(HSVRange_Green[2], HSVRange_Green[3])) and (blob_colors[i][2] in range(HSVRange_Green[4], HSVRange_Green[5])):
            #     blob_colors[i][3] = 4
            #     face[i] = 4
            # elif (blob_colors[i][0] in range(HSVRange_Orange[0], HSVRange_Orange[1])) and (blob_colors[i][1] in range(HSVRange_Orange[2], HSVRange_Orange[3])) and (blob_colors[i][2] in range(HSVRange_Orange[4], HSVRange_Orange[5])):
            #     blob_colors[i][3] = 5
            #     face[i] = 5
        print(face)
        if np.count_nonzero(face) == 9:
            # print(face)
            # print(blob_colors)
            return face, blob_colors
        else:
            # print(blob_colors)
            return [0, 0], blob_colors
    else:
        return [0, 0, 0], blob_colors
        # break


KERNEL_CORE = 5
ADAPTIVE = 51

#转换成灰度值，找到轮廓
def FindContour(bgr_image_input):
    FinalContours = []
    gray = cv2.cvtColor(bgr_image_input, cv2.COLOR_BGR2GRAY)  # 转灰度
    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (KERNEL_CORE, KERNEL_CORE))
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    gray = cv2.Canny(gray, 128, 256)
    # gray = cv2.adaptiveThreshold(
    #     gray, 80, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, ADAPTIVE, 7)  # 转灰度
    try:
        _, contours, hierarchy = cv2.findContours(
            gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    except:
        contours, hierarchy = cv2.findContours(
            gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for i, cnt in enumerate(contours):
        # 如果层级关系中的第三个参数为-1，表示没有下一级第一个子轮廓，那么这个肯定是内轮廓，如果不为-1，则为外轮廓
        if hierarchy[0][i][2] != -1:
            FinalContours.append(cnt)
    contours = FinalContours
    return contours

#通过以上，画出轮廓
def DrawContour(bgr_image_input, contours):
    contour_id = 0
    for contour in contours:  # 对每一个轮廓的内容进行颜色识别
        A1 = cv2.contourArea(contour)
        contour_id = contour_id + 1
        # cv2.drawContours(bgr_image_input, [contour], 0, (255, 255, 0), 2)
        if A1 < STICKER_AREA_SIZE_MAX and A1 > STICKER_AREA_SIZE_MIN:
            perimeter = cv2.arcLength(contour, True)
            epsilon = 0.01 * perimeter
            approx = cv2.approxPolyDP(contour, epsilon, True)
            hull = cv2.convexHull(contour)
            if cv2.norm(((perimeter / 4) * (perimeter / 4)) - A1) < 500:
                cv2.drawContours(bgr_image_input, [
                                 contour], 0, (255, 255, 0), 2)  # 绘制轮廓
    return bgr_image_input

STICKER_AREA_TILE_SIZE = 60
STICKER_AREA_TILE_GAP = 5
STICKER_AREA_OFFSET = 5

STICKER_CONTOUR_COLOR = (36, 255, 12)
BGR_YELLOW = (0, 235, 235)
BGR_RED = (5, 0, 143)
BGR_GREEN = (0, 207, 28)
BGR_ORANGE = (48, 110, 248)
BGR_BLUE = (172, 72, 0)
BGR_WHITE = (255, 255, 255)

#绘制3D模型的颜色
def draw_stickers(frame, face, offset_x, offset_y):
    """Draws the given stickers onto the given frame."""
    index = -1
    for row in range(3):
        for col in range(3):
            index += 1
            x1 = (offset_x + STICKER_AREA_TILE_SIZE * col) + \
                STICKER_AREA_TILE_GAP * col
            y1 = (offset_y + STICKER_AREA_TILE_SIZE * row) + \
                STICKER_AREA_TILE_GAP * row
            x2 = x1 + STICKER_AREA_TILE_SIZE
            y2 = y1 + STICKER_AREA_TILE_SIZE

            # shadow
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 0, 0),
                -1
            )
            if face[index] == 1:
                color = BGR_YELLOW
            elif face[index] == 2:
                color = BGR_BLUE
            elif face[index] == 3:
                color = BGR_RED
            elif face[index] == 4:
                color = BGR_GREEN
            elif face[index] == 5:
                color = BGR_ORANGE
            elif face[index] == 6:
                color = BGR_WHITE
            else:
                color = (125, 125, 125)
                # foreground color
            cv2.rectangle(
                frame,
                (x1 + 1, y1 + 1),
                (x2 - 1, y2 - 1),
                color,
                -1,
            )
    return frame


MINI_STICKER_AREA_TILE_SIZE = 20
MINI_STICKER_AREA_TILE_GAP = 3
MINI_STICKER_AREA_OFFSET = 0
COLOR_PLACEHOLDER = (150, 150, 150)

#绘制对应的展开模型的颜色
def draw_2d_cube_state(frame, solution):
    """
    Create a 2D cube state visualization and draw the self.result_state.

    We're gonna display the visualization like so:
                -----
              | Y Y Y |
              | Y Y Y |
              | Y Y Y |
        -----   -----   -----   -----
      | O O O | B B B | R R R | G G G |
      | O O O | B B B | R R R | G G G |
      | O O O | B B B | R R R | G G G |
        -----   -----   -----   -----
              | W W W |
              | W W W |
              | W W W |
                -----
    So we're gonna make a 4x3 grid and hardcode where each side has to go.
    Based on the x and y in that 4x3 grid we can calculate its position.
    """
    grid = {
        'yellow': [1, 0],
        'oringe': [0, 1],
        'blue': [1, 1],
        'red': [2, 1],
        'green': [3, 1],
        'white': [1, 2],
    }

    # The offset in-between each side (white, red, etc).
    side_offset = MINI_STICKER_AREA_TILE_GAP * 3

    # The size of 1 whole side (containing 9 stickers).
    side_size = MINI_STICKER_AREA_TILE_SIZE * 3 + MINI_STICKER_AREA_TILE_GAP * 2

    # The X and Y offset is placed in the bottom-right corner, minus the
    # whole size of the 4x3 grid, minus an additional offset.
    # offset_x =  (side_size * 4) + (side_offset * 3) + MINI_STICKER_AREA_OFFSET
    # offset_y = 500 + (side_size * 3) + (side_offset * 2) + MINI_STICKER_AREA_OFFSET
    offset_x = MINI_STICKER_AREA_OFFSET
    offset_y = MINI_STICKER_AREA_OFFSET

    for side, (grid_x, grid_y) in grid.items():
        curFace = []
        index = -1
        if(grid_x == 1 and grid_y == 0):
            curFace = solution[0:9]
        elif(grid_x == 0 and grid_y == 1):
            curFace = solution[36:45]
        elif(grid_x == 1 and grid_y == 1):
            curFace = solution[18:27]
        elif(grid_x == 2 and grid_y == 1):
            curFace = solution[9:18]
        elif(grid_x == 3 and grid_y == 1):
            curFace = solution[45:54]
        elif(grid_x == 1 and grid_y == 2):
            curFace = solution[27:36]
        for row in range(3):
            for col in range(3):
                if(index <= 7):
                    index += 1
                else:
                    break
                x1 = int((offset_x + MINI_STICKER_AREA_TILE_SIZE * col) +
                         (MINI_STICKER_AREA_TILE_GAP * col) + ((side_size + side_offset) * grid_x))
                y1 = int((offset_y + MINI_STICKER_AREA_TILE_SIZE * row) +
                         (MINI_STICKER_AREA_TILE_GAP * row) + ((side_size + side_offset) * grid_y))
                x2 = int(x1 + MINI_STICKER_AREA_TILE_SIZE)
                y2 = int(y1 + MINI_STICKER_AREA_TILE_SIZE)

                foreground_color = COLOR_PLACEHOLDER
                # if side in self.result_state:
                #     foreground_color = color_detector.get_prominent_color(self.result_state[side][index])
                if curFace[index] == 1:
                    foreground_color = BGR_YELLOW
                elif curFace[index] == 2:
                    foreground_color = BGR_BLUE
                elif curFace[index] == 3:
                    foreground_color = BGR_RED
                elif curFace[index] == 4:
                    foreground_color = BGR_GREEN
                elif curFace[index] == 5:
                    foreground_color = BGR_ORANGE
                elif curFace[index] == 6:
                    foreground_color = BGR_WHITE
                else:
                    foreground_color = (125, 125, 125)

                # shadow
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 0),
                    -1
                )

                # foreground color
                cv2.rectangle(
                    frame,
                    (x1 + 1, y1 + 1),
                    (x2 - 1, y2 - 1),
                    foreground_color,
                    -1
                )
    return frame


LINE_COLOR = (255, 255, 255)
TIP_LENGTH = 0.2

#绘制指令
def DrawInstruction(bgr_image_input, blob_colors, condition):
    if(condition == Op.Operation_ToShow.N):
        pass
    elif(condition == Op.Operation_ToShow.T_R):
        centroid1 = blob_colors[6]
        centroid2 = blob_colors[8]
        centroid3 = blob_colors[3]
        centroid4 = blob_colors[5]
        centroid5 = blob_colors[0]
        centroid6 = blob_colors[2]
        point1 = (int(centroid2[4]), int(centroid2[5]))
        point2 = (int(centroid1[4]), int(centroid1[5]))
        point3 = (int(centroid4[4]), int(centroid4[5]))
        point4 = (int(centroid3[4]), int(centroid3[5]))
        point5 = (int(centroid6[4]), int(centroid6[5]))
        point6 = (int(centroid5[4]), int(centroid5[5]))
        cv2.arrowedLine(bgr_image_input, point1, point2,
                        LINE_COLOR, 5, 4, 0, TIP_LENGTH)
        cv2.arrowedLine(bgr_image_input, point3, point4,
                        LINE_COLOR, 5, 4, 0, TIP_LENGTH)
        cv2.arrowedLine(bgr_image_input, point5, point6,
                        LINE_COLOR, 5, 4, 0, TIP_LENGTH)
    elif(condition == Op.Operation_ToShow.T_F):
        centroid1 = blob_colors[8]
        centroid2 = blob_colors[6]
        centroid3 = blob_colors[5]
        centroid4 = blob_colors[3]
        centroid5 = blob_colors[2]
        centroid6 = blob_colors[0]
        point1 = (int(centroid2[4]), int(centroid2[5]))
        point2 = (int(centroid1[4]), int(centroid1[5]))
        point3 = (int(centroid4[4]), int(centroid4[5]))
        point4 = (int(centroid3[4]), int(centroid3[5]))
        point5 = (int(centroid6[4]), int(centroid6[5]))
        point6 = (int(centroid5[4]), int(centroid5[5]))
        cv2.arrowedLine(bgr_image_input, point1, point2,
                        LINE_COLOR, 5, 4, 0, TIP_LENGTH)
        cv2.arrowedLine(bgr_image_input, point3, point4,
                        LINE_COLOR, 5, 4, 0, TIP_LENGTH)
        cv2.arrowedLine(bgr_image_input, point5, point6,
                        LINE_COLOR, 5, 4, 0, TIP_LENGTH)
    elif(condition == Op.Operation_ToShow.Wrong_All or condition == Op.Operation_ToShow.Wrong_Center):
        print("出错了")
    else:
        if(condition == Op.Operation_ToShow.R):
            centroid1 = blob_colors[8]
            centroid2 = blob_colors[2]
        elif(condition == Op.Operation_ToShow.r):
            centroid1 = blob_colors[2]
            centroid2 = blob_colors[8]
        elif(condition == Op.Operation_ToShow.L):
            centroid1 = blob_colors[0]
            centroid2 = blob_colors[6]
        elif(condition == Op.Operation_ToShow.l):
            centroid1 = blob_colors[6]
            centroid2 = blob_colors[0]
        elif(condition == Op.Operation_ToShow.U):
            centroid1 = blob_colors[2]
            centroid2 = blob_colors[0]
        elif(condition == Op.Operation_ToShow.u):
            centroid1 = blob_colors[0]
            centroid2 = blob_colors[2]
        elif(condition == Op.Operation_ToShow.D):
            centroid1 = blob_colors[6]
            centroid2 = blob_colors[8]
        elif(condition == Op.Operation_ToShow.d):
            centroid1 = blob_colors[8]
            centroid2 = blob_colors[6]
        point1 = (int(centroid1[4]), int(centroid1[5]))
        point2 = (int(centroid2[4]), int(centroid2[5]))
        cv2.arrowedLine(bgr_image_input, point1, point2,
                        LINE_COLOR, 5, 4, 0, TIP_LENGTH)
    return bgr_image_input
