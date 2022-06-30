from scipy import stats
import numpy as np
import Function as Fc


DETECT_TIMES = 8


def DetectFace(faces, curDetect, colorString, knn):
    DetectDone_Flag = False
    CenterCorrect_Flag = False
    face, blob_colors = Fc.detect_face(colorString, knn)  # 识别颜色
    detected_face = []
    # print(blob_colors)
    if len(face) == 9:  # 识别到九个
        faces.append(face)  # 加入队列
        if len(faces) == DETECT_TIMES:  # 达到识别次数
            face_array = np.array(faces)
            detected_face = stats.mode(face_array)[0]  # 取众数作为识别结果
            DetectDone_Flag = True
            if(detected_face[0][4] == curDetect):
                CenterCorrect_Flag = True
            return face, blob_colors, DetectDone_Flag, CenterCorrect_Flag, detected_face  # 返回
    return faces, blob_colors, DetectDone_Flag, CenterCorrect_Flag, detected_face
