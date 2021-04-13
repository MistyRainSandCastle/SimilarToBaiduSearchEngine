# -*- coding: utf-8 -*-
from SearchSpider.Modules.CommonModule import EXTRACT_IFNO
from lxml.html import etree
import re
import numpy as np
from datetime import datetime

class ExtractInfo:
    def __init__(self):
        self.titleText = ''
        self.time = ''
        self.contentText = ''
        self.nodeList = []

    def IsValidYear(self,year):
        try:
            year=int(year)
        except:
            year=9999
        return 2000<=year<=datetime.today().year

    def ExtractIndexDate(self,htmlText):
        regSub = "([1-2][0-9]{3})[^0-9]{1,3}?([0-1]?[0-9])[^0-9]{0,3}?([0-3]?[0-9]?)"
        reResSub = re.findall(regSub, htmlText, flags=re.S)
        maxYear=""
        for item in reResSub[:-1]:
            if self.IsValidYear(item[0]):
                if maxYear and item[0]>maxYear:
                    self.time=item[0]+"-01-01"
                elif not maxYear:
                    maxYear=item[0]
                    self.time = item[0]+"-01-01"
        if len(reResSub)==1 and self.IsValidYear(reResSub[0][0]):
            self.time=reResSub[0][0]+"-01-01"
    def ExtactProcess(self, htmlText, isIndex):
        htmlText = re.sub(r'</?span.*?>|&.{1,6}?;|</?tr.*?>|</?td.*?>', '', htmlText, flags=re.S)
        etreeObj = etree.HTML(htmlText)
        self.titleText = self.ChangeNodeText("".join(etreeObj.xpath('//title/text()')))
        etree.strip_elements(etreeObj, *EXTRACT_IFNO['USELESS_TAG'],with_tail=False)
        if isIndex:
            self.ExtractIndexPro(etreeObj)
            self.ExtractIndexDate("".join(etreeObj.xpath('//text()')))
        else:
            self.ExtractPagePro(etreeObj)

    def ExtractIndexPro(self, etreeObj):
        otherAvg, otherNodes = self.GetAvgLen(etreeObj.xpath('//body//*[name(.)!="a" and count(*)=0]'))
        for item, otherLen in otherNodes:
            parentNode = item.getparent()
            if (otherLen < 0.5 * otherAvg or otherLen < 5) and parentNode is not None:
                parentNode.remove(item)
        linkAvg, linkNodes = self.GetAvgLen(etreeObj.xpath('//body//a'))
        for item, linkLen in linkNodes:
            parentNode = item.getparent()
            if (linkLen < linkAvg or linkLen < 5) and parentNode is not None:
                parentNode.remove(item)
        self.contentText = self.ChangeNodeText("".join(etreeObj.xpath('//body//text()')))

    def GetAvgLen(self, NodesList):
        count = 0
        sum = 0
        Nodes = []
        for item in NodesList:
            itemText = item.xpath('.//text()')
            linkLen = len(self.ChangeNodeText("".join(itemText)).strip())
            Nodes.append([item, linkLen])
            if linkLen > 4:
                count += 1
                sum += linkLen
        return sum / count if count else 0, Nodes

    def ExtractPagePro(self, etreeObj):
        self.ExtractPage(etreeObj.xpath('//body/*'))
        score_list = [x[7] for x in self.nodeList]
        std=1
        if len(self.nodeList)>1:
            std = np.std(score_list, ddof=1)
        maxItem = None
        maxScore = None
        maxIndex = 0
        mayDate=""
        replaceDate=""
        for index, item in enumerate(self.nodeList):
            SBDi = (item[1] - item[3]) / (item[5] + 1) if item[1] - item[3] > 0 else 1
            score = np.log(std) * item[7] * np.log10(item[6] + 2) * np.log(SBDi) * np.sqrt(item[5])
            if item[8]:
                replaceDate=item[8]
            if not maxScore or maxScore < score:
                maxScore = score
                maxItem = item
                maxIndex = index
                if replaceDate:
                    mayDate=replaceDate
                    replaceDate=""

        if  maxItem :
            self.contentText = self.nodeList[maxIndex][0]
            dateIndex=maxIndex
            if not self.time:
                notConentIndex = maxIndex - maxItem[2]
                dateIndex = notConentIndex
                while dateIndex >= 0 and notConentIndex - dateIndex <= 5:
                    if self.nodeList[dateIndex][8]:
                        self.time = self.nodeList[dateIndex][8]
                        break
                    dateIndex -= 1
                if not self.time:
                    dateIndex = maxIndex
                    while dateIndex > notConentIndex:
                        if self.nodeList[dateIndex][8]:
                            self.time = self.nodeList[dateIndex][8]
                            break
                        dateIndex -= 1
                if not self.time:
                    self.time=mayDate
            if not self.titleText:
                titleIndex = dateIndex
                while titleIndex >= 0 and dateIndex - titleIndex <= 15:
                    if self.nodeList[titleIndex][9]:
                        self.titleText = self.nodeList[titleIndex][9]
                        break
                    titleIndex -= 1

    def ExtractPage(self, SelectInfo):
        elemList = []
        for item in SelectInfo:
            try:
                tag = item.tag
            except:
                tag = EXTRACT_IFNO['NONE']
            if not tag in EXTRACT_IFNO['USELESS_TAG']:
                nodeText = self.ChangeNodeText("".join(item.xpath('.//text()'))).strip()
                if nodeText:
                    childList = self.ExtractPage(item.xpath('./*'))
                    Ti, TGi, LTi, LTGi, Sbi, PNum,calTGi = self.GetNodeInfo(nodeText, tag)
                    subTi = subTGi = subLTi = subLTGi = subPNum =subCalTGi= 0
                    for childItem in childList:
                        subTi += childItem[1]
                        subTGi += childItem[2]
                        subLTi += childItem[3]
                        subLTGi += childItem[4]
                        subPNum += childItem[6]
                        subCalTGi+=childItem[8]
                    LTi = (LTi - subTi if LTi > 0 else LTi) + subLTi
                    TGi += subTGi
                    LTGi += subLTGi
                    PNum += subPNum
                    calTGi+=subCalTGi
                    a = 1 / LTGi if LTGi else 1
                    TDi = ((Ti - LTi) / (calTGi - LTGi)) * a if calTGi - LTGi > 0 else 0
                    elemList.append([nodeText, Ti, TGi, LTi, LTGi, Sbi, PNum, TDi,calTGi])
                    self.nodeList.append([nodeText, Ti, TGi, LTi, LTGi, Sbi, PNum, TDi, self.ExtractDate(nodeText),
                                          self.ExtractTitle(nodeText, tag)])
        return elemList

    def GetNodeInfo(self, nodeText, tag):
        Sbi = len(re.findall(EXTRACT_IFNO['SIGNSET'], nodeText, flags=re.S))
        Ti = len(nodeText) ** 1.5
        TGi = 1
        calTGi=1
        LTi = 0
        LTGi = 0
        PNum = 0
        if tag == EXTRACT_IFNO['LINK']:
            LTi = Ti
            LTGi = TGi
        elif tag == EXTRACT_IFNO['CONTENT']:
            PNum = 1
        if tag!=EXTRACT_IFNO['LINK'] and len(nodeText)<10:
            calTGi=0
        if ('Copyright' in nodeText or '版权所有' in nodeText) and '©' in nodeText:
            Ti**=0.5
            calTGi=1
        return Ti, TGi, LTi, LTGi, Sbi, PNum,calTGi

    def ChangeNodeText(self, str):
        subStr = re.sub('[\n\r\t]', '', str, flags=re.S)
        return re.sub(' +', ' ', subStr, flags=re.S)

    def ExtractDate(self, str):
        reg = "((发布|更新|编辑)?(时间|日期).{0,3})?([1-2][0-9]{3})[^0-9]{1,3}?([0-1]?[0-9])[^0-9]{1,3}?([0-3]?[0-9])"
        probDate = ''
        if not self.time:
            reRes = re.findall(reg, str, flags=re.S)
            for item in reRes:
                if self.IsValidYear(item[3]):
                    if item[1]:
                        self.time="-".join(item[3:])
                        break
                    elif not probDate :
                        probDate="-".join(item[3:])
            if not self.time:
                regSub="^日期.{0,3}?([1-2][0-9]{3})[^0-9]{1,3}?([0-1]?[0-9])[^0-9]{1,3}?([0-3]?[0-9])"
                reResSub=re.findall(regSub,str, flags=re.S)
                if len(reResSub)==1:
                    if self.IsValidYear(reResSub[0][0]):
                        self.time = "-".join(reResSub[0])
        return probDate

    def ExtractTitle(self, str, tag):
        return str if not self.titleText and len(tag) and tag[0] == 'h' else ''

    def GetDate(self):
        return self.time

    def GetContent(self):
        return self.contentText

    def GetTitle(self):
        return self.titleText
