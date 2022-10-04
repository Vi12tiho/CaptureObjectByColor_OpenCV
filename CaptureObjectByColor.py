import cv2
import numpy
# from _tkinter import *
from datetime import datetime

class ColorObject:

    def __init__(self, name, lowBoundColor = [0,0,0], dAreaSet = 400, x = 0, y = 0, highBoundColor = [180,255,255]):
        self.name = name
        self.lowBoundColor = lowBoundColor
        self.highBoundColor = highBoundColor
        self.x = x
        self.y = y
        self.dAreaSet = dAreaSet
        self.lowBorder = numpy.array((lowBoundColor[0],lowBoundColor[1],lowBoundColor[2]), numpy.uint8)
        self.highBorder = numpy.array((highBoundColor[0],highBoundColor[1],highBoundColor[2]), numpy.uint8)
        self.mask = None

    def updateBorder(self):
        self.lowBorder = numpy.array((lowBoundColor[0],lowBoundColor[1],lowBoundColor[2]), numpy.uint8)
        self.highBorder = numpy.array((highBoundColor[0], highBoundColor[1], highBoundColor[2]), numpy.uint8)

    def calcCoordinates(self):
        pass

listColorObject = []

lowTestColor = [150,150,150]
highTestColor = [180,255,255]

firstStartProg = True
countLogs = 1
countColorMask = 5
lowBorder = [0] * countColorMask
highBorder = [0] * countColorMask

numberDevice = 0
lowBoundColor = [110,70,70]
highBoundColor = [150,255,255]
delay = 1       # 1 мс
dAreaSet = 400

x = 0
y = 0

resolution = [800, 600]
autoRec = True

toolsSettingsOn = True

#
def get_calcMilisec(startPointTime):
    nowMicrosec = datetime.now().microsecond

    resMicrosec = nowMicrosec - startPointTime
    if nowMicrosec <= startPointTime:
        resMicrosec = nowMicrosec + (999999 - startPointTime)
    # print(resMicrosec / 1000)

    return resMicrosec / 1000

# FPS
countFramePreSecond = 0
PointSec = 0

def measureFPS():
    global countFramePreSecond, PointSec
    countFramePreSecond += 1
    if datetime.now().second != PointSec:
        PointSec = datetime.now().second
        print(countFramePreSecond)
        countFramePreSecond = 0

# Trackbar
index = 0
layer = 0


def update():
    vis = hsv.copy()
    cv2.drawContours( vis, contours0, index, (255,0,0), 2, cv2.LINE_AA, hierarchy, layer )
    cv2.imshow('contours', vis)


def update_index(v):
    global index
    index = v-1
    update(hsv, contours0, hierarchy)


def update_layer(v):
    global layer
    layer = v
    update()


def insertionTrackbar():

    def update_index(v):
        global index
        index = v - 1
        update(hsv, contours0, hierarchy)

    def update_layer(v):
        global layer
        layer = v
        update()

    pass
#


def initialization():
    pass


def readIniSettings():
    global numberDevice, dAreaSet, delay, autoRec, countColorMask
    escape = False

    with open('Settings.ini', 'r', encoding='UTF-8', newline='') as f:
        for row in f:
            changedRow = ''
            changedRow = row.lstrip()
            changedRow = changedRow.rstrip()
            if not changedRow.find('#') == 0:
                changedRow = changedRow.split('=')
                for i in range(0, len(changedRow)):
                    changedRow[i] = changedRow[i].lstrip()
                    changedRow[i] = changedRow[i].rstrip()
                    if changedRow[i] == '':
                        break
                        escape = True
                    elif i == 1:
                        if changedRow[i-1] == 'number_device':
                            numberDevice = int(changedRow[i])
                        elif changedRow[i-1].find('lowBoundColor') > -1:
                            listBeforeCharEqual = changedRow[i-1].split('_')

                            temp = changedRow[i].split(',')
                            lowBoundColor[0] = int(temp[0])
                            lowBoundColor[1] = int(temp[1])
                            lowBoundColor[2] = int(temp[2])

                            listColorObject.append(ColorObject(listBeforeCharEqual[1], [int(temp[0]), int(temp[1]), int(temp[2])]))
                        elif changedRow[i-1].find('highBoundColor') > -1:
                            listBeforeCharEqual = changedRow[i - 1].split('_')

                            temp = changedRow[i].split(',')
                            highBoundColor[0] = int(temp[0])
                            highBoundColor[1] = int(temp[1])
                            highBoundColor[2] = int(temp[2])

                            if listBeforeCharEqual[1] == listColorObject[-1].name:
                                listColorObject[-1].lowBoundColor = [int(temp[0]), int(temp[1]), int(temp[2])]
                                listColorObject[-1].updateBorder()
                        elif changedRow[i-1] == 'dAreaSet':
                            dAreaSet = int(changedRow[i])
                        elif changedRow[i-1] == 'delay':
                            delay = int(changedRow[i])
                        elif changedRow[i-1] == 'resolution':
                            temp = changedRow[i].split('x')
                            resolution[0] = int(temp[0])
                            resolution[1] = int(temp[1])
                        elif changedRow[i-1] == 'autoRec':
                            autoRec = bool(int(changedRow[i]))
                if escape == True:
                    escape = False
                    continue


def writeData():
    with open('Coordinates.txt', 'w', encoding='UTF-8', newline='') as f:
        record = ''
        record = str(listColorObject[0].x) + ' ' + str(99999) + ' ' + str(listColorObject[0].y) + ' ' + str(99999)
        f.write(record)


def writeLogs(line):
    global countLogs, firstStartProg

    if firstStartProg:
        commanda = 'w'
        firstStartProg = False
    else:
        commanda = 'a'
    with open('Logs.txt', commanda, encoding='UTF-8') as f:
        record = ""
        record = str(countLogs) + ": " + line + "\n"
        f.write(record)
        countLogs += 1


def captureColor(cadr):
    # listMask = []
    countColorMask = len(listColorObject)

    # pointTime1 = datetime.now().microsecond

    cadr_hsv = cv2.cvtColor(cadr, cv2.COLOR_BGR2HSV)

    for i in range(0, countColorMask):
        # listMask.append(cv2.inRange(cadr_hsv, listColorObject[i].lowBorder, listColorObject[i].highBorder))
        listColorObject[i].mask = cv2.inRange(cadr_hsv, listColorObject[i].lowBorder, listColorObject[i].highBorder)
        if i == 0:      # if color only 1
            maskMerge = listColorObject[i].mask
        if i == 1:
            maskMerge = cv2.addWeighted(listColorObject[i - 1].mask, 0.5, listColorObject[i].mask, 0.5, 0)
        elif i > 1:
            maskMerge = cv2.addWeighted(maskMerge, 0.5, listColorObject[i].mask, 0.5, 0)

    processedCadr = cv2.bitwise_and(cadr_hsv, cadr_hsv, mask = maskMerge)
    processedCadr = cv2.cvtColor(processedCadr, cv2.COLOR_HSV2BGR)

    # mask_0 = cv2.inRange(cadr_hsv, lowBorder[0], highBorder[0])      # В диапазоне цвета - белый на видео(за пределами -чёрный)

    # mask_1 = cv2.inRange(cadr_hsv, lowBorder[1], highBorder[1])

    # test_result = cv2.addWeighted(mask_0,0.5,mask_1,0.5,0)  # image blending g(x)=(1−α)f0(x)+αf1(x) (α  from 0→1)

    # test_result = cv2.addWeighted(listMask[0], 0.5, listMask[1], 0.5, 0)


    # result = cv2.bitwise_and(cadr_hsv, cadr_hsv, mask = test_result)
    # result = cv2.bitwise_or(result, result, mask = mask_1)
    # result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

    for i in range(0, countColorMask):
        moments = cv2.moments(listColorObject[i].mask, 1)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']

        # x=0
        if dArea > listColorObject[i].dAreaSet:
            x = int(dM10 / dArea)       # Центр изображения x
            y = int(dM01 / dArea)       # Центр изображения y
            cv2.circle(processedCadr, (x, y), 4, (0,0,255), -1)     # -1 - для заливки
        else:
            x = 0
            y = 0
        # print('x =',x, 'y =', y)
        listColorObject[i].x = x
        listColorObject[i].y = y

    # cv2.imshow("Test", result)
    cv2.imshow("Test", processedCadr)


if __name__ == '__main__':
    # initialization()

    readIniSettings()
    # print(numberDevice, lowBoundColor, highBoundColor, dAreaSet, delay, sep='\n')

    cv2.namedWindow("Test")
    # create trackbars for color change
    # cv2.createTrackbar('H_l','Test',lowTestColor[0],180,lambda q:q)
    # cv2.createTrackbar('S_l','Test',lowTestColor[1],255,lambda q:q)
    # cv2.createTrackbar('V_l','Test',lowTestColor[2],255,lambda q:q)
    # cv2.createTrackbar('H_h','Test',highTestColor[0],180,lambda q:q)
    # cv2.createTrackbar('S_h','Test',highTestColor[1],255,lambda q:q)
    # cv2.createTrackbar('V_h','Test',highTestColor[2],255,lambda q:q)
    # create switch for ON/OFF functionality
    # switch = '0 : OFF \n1 : ON'
    # cv2.createTrackbar(switch, 'Test',0,1,lambda q:q)


    video = cv2.VideoCapture(numberDevice)

    fps = video.get(cv2.CAP_PROP_FPS)
    print("fps: ", fps)
    writeLogs("fps: " + str(fps))
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("size: ", size)
    writeLogs("size: " + str(size))

    # contours0, hierarchy = cv2.findContours(listMask[0].copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # update_index(0)
    # update_layer(0)
    # cv2.createTrackbar("contour", "contours", 0, 7, update_index)
    # cv2.createTrackbar("layers", "contours", 0, 7, update_layer)

    listTime_ms = []

    while True:
        pointTime1 = datetime.now().microsecond
        # measureFPS()

        ret, frame = video.read()
        if autoRec == False:
            frame = cv2.resize(frame, resolution, interpolation=cv2.INTER_CUBIC)
        # lowTestColor[0] = cv2.getTrackbarPos('H_l','Test')
        # lowTestColor[1] = cv2.getTrackbarPos('S_l','Test')
        # lowTestColor[2] = cv2.getTrackbarPos('V_l','Test')
        # highTestColor[0] = cv2.getTrackbarPos('H_h','Test')
        # highTestColor[1] = cv2.getTrackbarPos('S_h','Test')
        # highTestColor[2] = cv2.getTrackbarPos('V_h','Test')
        # s = cv2.getTrackbarPos(switch,'Test')

        try:

            captureColor(frame)
            writeData()

        except:
            video.release()
            raise

        c = cv2.waitKey(delay)
        if c == 27:
            break

        countFramePreSecond += 1
        if datetime.now().second != PointSec:
            PointSec = datetime.now().second
            print(countFramePreSecond, end=": ")

            summEl = 0
            for el in listTime_ms:
                # print(el, end= "\t")
                summEl += el
            print(summEl/countFramePreSecond)      # Среднее-арифметическое
            listTime_ms.clear()
            # print()

            countFramePreSecond = 0
        else:
            listTime_ms.append(get_calcMilisec(pointTime1))

        # get_calcMilisec(pointTime1)

    video.release()
    cv2.destroyAllWindows()