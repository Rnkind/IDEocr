from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import time


class OcrResMem(object):
    def __init__(self, resList):
        self.resList = tuple(resList[0])

    def checkParam(self, num):
        if num >= len(self.resList):
            return False
        if num < 0:
            return False
        if str(type(num)).find == -1:
            return False
        return True

    def getNum(self):
        return len(self.resList)

    def getLocation(self, num):
        if not self.checkParam(num):
            return None
            
        return self.resList[num][0]

    def getTopLeft(self, num):
        if not self.checkParam(num):
            return None

        return self.getLocation(num)[0]
    
    def getTopRight(self, num):
        if not self.checkParam(num):
            return None
            
        return self.getLocation(num)[1]
        
    def getBottomRight(self, num):
        if not self.checkParam(num):
            return None
            
        return self.getLocation(num)[2]

    def getBottomLeft(self, num):
        if not self.checkParam(num):
            return None
            
        return self.getLocation(num)[3]        

    def getContent(self, num):
        if not self.checkParam(num):
            return None
            
        return self.resList[num][1]

    def getWords(self, num):
        if not self.checkParam(num):
            return None
            
        return self.getContent(num)[0]

    def getAccuray(self, num):
        if not self.checkParam(num):
            return None
            
        return float(self.getContent(num)[1])

    def checkAccuary(self, lowest):
        i = 0
        while i < len(self.resList):
            if self.getAccuray(i) < lowest:
                return False                
            i += 1
        return True

    def deleteLowAccuary(self, lowest):
        if self.checkAccuary(lowest):
            return
        if lowest >= 1:
            self.resList.clear()
            return
        if lowest < 0:
            return
        i = 0
        temp = list(self.resList)
        while i < len(temp):
            if self.getAccuray(i) < lowest:
                temp.pop(i)
            else:
                i += 1
        self.resList = tuple(temp)
     
class OcrDealer(object):
    def __init__(self, img_path, if_time):
        self.lang = "en"
        self.LowsetAccuray = 0.85
        self.ttfPath = "./simfang.ttf"
        self.use_gpu = True
        self.dealTime = 0
        self.result = None
        self.workNormally(img_path, if_time)


    def workNormally(self, img_path, if_time):
        self.creat()
        self.dealInfo(img_path)
        if if_time:
            self.dealTime = self.dealWithTime()
        else:
            self.deal()
            self.dealTime = -1


    def creat(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang=self.lang, use_gpu=self.use_gpu)

    def dealInfo(self, img_path):
        self.img_path = img_path


    def setImgPath(self, img_path):
        self.img_path = img_path


    def deal(self):
        self.result = self.ocr.ocr(self.img_path, cls = True)
        self.resultList = OcrResMem(self.result)

    def dealWithTime(self):
        TimeStart = time.time()
        self.result = self.ocr.ocr(self.img_path, cls = True)
        TimeEnd = time.time()
        self.resultList = OcrResMem(self.result)
        return TimeEnd - TimeStart

    def checkResult(self):
        # check accuray
        return self.checkResult(self.LowsetAccuray)

    def drawRes(self, res_path):
        # put result avaiblly to res_path
        result = self.result[0]
        image = Image.open(self.img_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path=self.ttfPath)
        im_show = Image.fromarray(im_show)
        im_show.save(res_path)

    def getLocation(self, num):
        return self.resultList.getLocation(num)
        
    def getTopLeft(self, num):
        return self.resultList.getTopLeft(num)

    def getTopRight(self, num):
        return self.resultList.getTopRight(num)

    def getBottomLeft(self, num):
        return self.resultList.getBottomLeft(num)

    def getBottomRight(self, num):
        return self.resultList.getBottomRight(num)

    def getContent(self, num):
        return self.resultList.getContent(num)

    def getWords(self, num):
        return self.resultList.getWords(num)

    def getAccuray(self, num):
        return self.resultList.getAccuray(num)

    def getTime(self):
        return self.dealTime

    def deleteLowAccuray(self):
        pass

    @staticmethod
    def checkBreakPoints(BreakPointsView, BreakPointsList):
        """
        @param BreakPointView:Mem list of Breakpoint View
        @param BreakPointList:the BreakPoint actual location 
        """
        
        i = 0
        error = list()
        TrueList = BreakPointsList
        while i < BreakPointsView.getNum():
            words = BreakPointsView.getWords(i)
            if not words.endswith("\d"):
                continue
            temp = list(words)
            res = str()
            while temp[len(temp) - 1].isdigit():
                res += temp.pop(len(temp) - 1)
            
            if TrueList.count(res) == 0:
                error.append(["cannot find breakpoint for any line number", i, words])
            else:
                TrueList.pop(TrueList.index(res))
            i += 1

        if len(TrueList) != 0:
            error.append(["cannot find line number for any breakpoint", TrueList])
        
        return error

    @staticmethod
    def LineNumListDealer(point, number):
        pass

    
        
"""
test = PaddleOCR(use_angle_cls=True, lang = "en", use_gpu=True)
testRes = test.ocr("./breakpoints3.jpg", cls=True)
testResList = OcrResMem(testRes)
print("getLocation0: " + str(testResList.getLocation(-7)))
print("getTL0: " + str(testResList.getTopLeft(0)))
print("getContent1111: " + str(testResList.getContent(1111)))

test = OcrDealer("./breakpoints3.jpg", True)
test.drawRes("./testRes.jpg")
print(test.getAccuray(0))


test = PaddleOCR(use_angle_cls=True, lang = "en", use_gpu=True)
testRes = test.ocr("./breakpoints3.jpg", cls=True)
testResList = OcrResMem(testRes)
print("=" * 50)
print(testResList.resList)
print("=" * 50)
testResList.deleteLowAccuary(0.91)
print(testResList.resList)
"""