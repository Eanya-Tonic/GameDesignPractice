from scipy import stats
import numpy as np
import Function as Fc


DETECT_TIMES = 8
def DrawContours(bgr_image_input):
    contours = Fc.FindContour(bgr_image_input)
    img = bgr_image_input
    Output = Fc.DrawContour(img,contours)
    return Output,contours

def DetectFace(faces,bgr_image_input,contours,curDetect,colorString,knn):
    DetectDone_Flag = False
    CenterCorrect_Flag = False
    img = bgr_image_input
    face,blob_colors = Fc.detect_face(img,contours,colorString,knn)#识别颜色
    detected_face = []
    # print(blob_colors)
    if len(face) == 9:#识别到九个
        faces.append(face)#加入队列
        if len(faces) == DETECT_TIMES:#达到识别次数
            face_array = np.array(faces)
            detected_face = stats.mode(face_array)[0]#取众数作为识别结果
            DetectDone_Flag = True
            if(detected_face[0][4] == curDetect):
                CenterCorrect_Flag = True
            return face,blob_colors,DetectDone_Flag,CenterCorrect_Flag,detected_face#返回
    return faces,blob_colors,DetectDone_Flag,CenterCorrect_Flag,detected_face