import cv2
import numpy
# from _tkinter import *
import datetime

lowTestColor = [150,150,150]
highTestColor = [180,255,255]

firstStartProg = True
countLogs = 1
countMask = 5
lowBorder = [0] * countMask
highBorder = [0] * countMask

numberDevice = 0
lowBoundColor = [110,70,70]
highBoundColor = [150,255,255]
delay = 1       # 1 мс
dAreaSet = 400

x = 0
y = 0

resolution = [(3840, 1080),
              (1920, 1080),
              (1366, 1024),
              (1024, 768),
              (800, 600)]

def initialization():
    pass

def readIniSettings():
    escape = False

    with open('Settings.ini', 'r', encoding='UTF-8', newline='') as f:
        global numberDevice, dAreaSet, delay
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
                        if changedRow[i-1] == 'lowBoundColor':
                            temp = changedRow[i].split(',')
                            lowBoundColor[0] = int(temp[0])
                            lowBoundColor[1] = int(temp[1])
                            lowBoundColor[2] = int(temp[2])
                        if changedRow[i-1] == 'highBoundColor':
                            temp = changedRow[i].split(',')
                            highBoundColor[0] = int(temp[0])
                            highBoundColor[1] = int(temp[1])
                            highBoundColor[2] = int(temp[2])
                        if changedRow[i-1] == 'dAreaSet':
                            dAreaSet = int(changedRow[i])
                        if changedRow[i-1] == 'delay':
                            delay = int(changedRow[i])
                if escape == True:
                    escape = False
                    continue

def writeData():
    global x, y
    with open('Coordinates.txt', 'w', encoding='UTF-8', newline='') as f:
        record = ''
        record = str(x) + ' ' + str(99999) + ' ' + str(y) + ' ' + str(99999)
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
    global x, y

    lowBorder[0] = numpy.array((lowBoundColor[0],lowBoundColor[1],lowBoundColor[2]), numpy.uint8)
    highBorder[0] = numpy.array((highBoundColor[0],highBoundColor[1],highBoundColor[2]), numpy.uint8)

    lowBorder[1] = numpy.array((lowTestColor[0],lowTestColor[1],lowTestColor[2]), numpy.uint8)
    highBorder[1] = numpy.array((highTestColor[0],highTestColor[1],highTestColor[2]), numpy.uint8)
    # lowBorder[2] = numpy.array((lowBoundColor[0],lowBoundColor[1],lowBoundColor[2]), numpy.uint8)
    # highBorder[2] = numpy.array((highBoundColor[0],highBoundColor[1],highBoundColor[2]), numpy.uint8)
    # lowBorder[3] = numpy.array((lowBoundColor[0],lowBoundColor[1],lowBoundColor[2]), numpy.uint8)
    # highBorder[3] = numpy.array((highBoundColor[0],highBoundColor[1],highBoundColor[2]), numpy.uint8)
    # lowBorder[4] = numpy.array((lowBoundColor[0],lowBoundColor[1],lowBoundColor[2]), numpy.uint8)
    # highBorder[4] = numpy.array((highBoundColor[0],highBoundColor[1],highBoundColor[2]), numpy.uint8)

    cadr_hsv = cv2.cvtColor(cadr, cv2.COLOR_BGR2HSV)
    mask_0 = cv2.inRange(cadr_hsv, lowBorder[0], highBorder[0])      # В диапазоне цвета - белый на видео(за пределами -чёрный)

    mask_1 = cv2.inRange(cadr_hsv, lowBorder[1], highBorder[1])
    # mask_2 = cv2.inRange(cadr_hsv, lowBorder[2], highBorder[2])
    # mask_3 = cv2.inRange(cadr_hsv, lowBorder[3], highBorder[3])
    # mask_4 = cv2.inRange(cadr_hsv, lowBorder[4], highBorder[4])

    test_result = cv2.addWeighted(mask_0,0.5,mask_1,0.5,0)  # image blending g(x)=(1−α)f0(x)+αf1(x) (α  from 0→1)

    result = cv2.bitwise_and(cadr_hsv, cadr_hsv, mask = test_result)
    # result = cv2.bitwise_or(result, result, mask = mask_1)
    result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

    moments = cv2.moments(mask_0, 1)     # 1 - для работы с бинарными изображениями
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']

    # x=0

    if dArea > dAreaSet:
        x = int(dM10 / dArea)       # Центр изображения x
        y = int(dM01 / dArea)       # Центр изображения y
        cv2.circle(result, (x, y), 4, (0,0,255), -1)     # -1 - для заливки
    else:
        x = 0
        y = 0
    print('x =',x, 'y =', y)

    cv2.imshow("Test", result)

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

while True:
    ret, frame = video.read()

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

video.release()
cv2.destroyAllWindows()