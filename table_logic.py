import sys
import string
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from interface import Ui_MainWindow

import sys
import os
cwd = os.getcwd() # current directory
txtFile = "characters.txt"
file_path = os.path.join(cwd, txtFile) # relative path of the text file


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Chinese character features database")

        self.query = QueryThread()
        self.query_button.clicked.connect(self.startQuery)
        self.query.queryResult.connect(self.showQueryTable)

        self.match = MatchThread()
        self.match_button.clicked.connect(self.startMatch)
        self.match.matchResult.connect(self.showMatchTable)

        # add options to the combo box
        self.radical_combo.addItems( ['all', '阝', '口', '扌', '土', '疒', '矢', '爫', '石', '艹', '宀', '广', '厂', '亻', '日', '木', '山', '黑', '灬', '凵', '大', '氵', '罒',
         '巳', '八', '足', '雨', '父', '白', '手', '贝', '页', '王', '文', '舟', '片', '瓜', '力', '十', '彡', '巾', '纟', '月', '方', '钅',
         '刂', '勹', '火', '饣', '鱼', '豸', '心', '匕', '夂', '衤', '车', '竹', '辶', '鼻', '毛', '比', '彳', '禾', '廾', '辛', '门', '革',
         '户', '又', '衣', '干', '冫', '示', '一', '尸', '卜', '马', '忄', '止', '犭', '采', '厶', '飠', '虫', '歹', '人', '曰', '丿', '工',
         '讠', '礻', '亠', '小', '长', '攵', '田', '走', '巛', '臣', '辰', '皿', '戈', '乙', '耳', '齿', '斤', '羽', '赤', '里', '酉', '目',
         '自', '刀', '角', '穴', '川', '丨', '瓦', '丷', '隹', '欠', '米', '子', '寸', '母', '弓', '彐', '儿', '癶', '几', '殳', '鼎', '斗',
         '豆', '女', '立', '夕', '身', '鸟', '而', '二', '糸', '非', '飞', '匚', '气', '风', '用', '肉', '覀', '尢', '甘', '冂', '缶', '高',
         '耒', '骨', '鼓', '谷', '囗', '冖', '见', '鬼', '韦', '行', '豕', '士', '虍', '幺', '黄', '卩', '己', '旡', '齐', '艮', '廴', '金',
         '水', '言', '青', '臼', '丶', '??', '耂', '牛', '黍', '隶', '鹿', '龙', '玄', '麻', '麦', '矛', '面', '乛', '牜', '疋', '爪', '皮',
         '攴', '入', '犬', '羊', '乚', '色', '舌', '生', '氏', '弋', '亅', '首', '鼠', '爻', '聿', '屮', '毋', '香', '血', '牙', '音', '玉',
         '支', '至'])
        self.structure_combo.addItems(['all', '左右结构', '左中右结构', '上下结构', '半包围结构', '单一结构', '上中下结构',
                                       '左上包围结构', '品字结构', '全包围结构', '嵌套结构', '下包围结构', '左包围结构',
                                       '右上包围结构'])
        self.liushu_combo.addItems(['all','形声', '会意', '原为形声', '会意兼形声', '象形', '指事', '原为象形', '?',
                                    '假借', '原为会意', '原为会意兼形声'])

        self.generate = GenerateThread()
        self.generate_button.clicked.connect(self.startGenerate)
        self.generate.generateResult.connect(self.showGenerateTable)

    def startGenerate(self):
        self.generate_table.setRowCount(0)
        self.generate.generationConditions(self.init_box.text(),self.final_box.text(), self.tone_box.text(),
                                           str(self.radical_combo.currentText()), str(self.structure_combo.currentText()),str(self.liushu_combo.currentText()),
                                           self.small_stroke.value(),self.big_stroke.value(),self.small_freq.value(),self.big_freq.value())
        self.generate.start()
        self.generate_table.horizontalHeader().setSectionResizeMode(1)
    def showGenerateTable(self, text):
        rowPosition = self.generate_table.rowCount()
        self.generate_table.insertRow(rowPosition)
        data = text.split()
        for i in range(11):
            self.generate_table.setItem(rowPosition, i, QTableWidgetItem(data[i]))

    def startQuery(self):
        self.query_table.setRowCount(0)
        self.query.charInput(self.query_input.text())
        self.query.start()
        # automatically adjust the horizontal width
        self.query_table.horizontalHeader().setSectionResizeMode(1)
    def showQueryTable(self, text):
        rowPosition = self.query_table.rowCount()
        self.query_table.insertRow(rowPosition)
        data = text.split()
        for i in range(11):
            self.query_table.setItem(rowPosition, i, QTableWidgetItem(data[i]))

    def startMatch(self):
        # clear previous data after each button click
        self.match_table.setRowCount(0)
        if sum([self.check_initial.isChecked(), self.check_final.isChecked(), self.check_tone.isChecked(),
                self.check_radical.isChecked(),self.check_structure.isChecked(), self.check_liushu.isChecked(),
                self.stroke_diff.value() >=0 , self.freq_diff.value() >=0]) == 0:
            self.status.setText("Error: no features are selected!")
        elif self.match_input.text() == '':
            self.status.setText("Error: no character is entered!")
        else:
            self.match.checkConditions(self.check_initial.isChecked(), self.check_final.isChecked(),
                                       self.check_tone.isChecked(), self.check_radical.isChecked(),
                                       self.check_structure.isChecked(), self.check_liushu.isChecked(),
                                       self.stroke_diff.value(), self.freq_diff.value())
            self.match.matchInput(self.match_input.text())
            self.match.start()

            # automatically adjust the horizontal width
            self.match_table.horizontalHeader().setSectionResizeMode(1)
    def showMatchTable(self, text):
        rowPosition = self.match_table.rowCount()
        self.match_table.insertRow(rowPosition)
        data = text.split()
        for i in range(11):
            self.match_table.setItem(rowPosition, i, QTableWidgetItem(data[i]))
        if data[1] == "N/A":
            self.status.setText("No data!")
        else:
            self.status.setText("Succeeded!")


class GenerateThread(QThread):
    generateResult = pyqtSignal(str)

    def __init__(self, parent = None):
        super(GenerateThread, self).__init__(parent)

    def generationConditions(self, initial, final, tone, radical, structure, liushu, small_stroke, big_stroke, small_freq, big_freq):
        self.initial = initial
        self.final = final
        self.tone = tone
        # string type
        self.radical = radical
        self.structure = structure
        self.liushu = liushu
        # the following four variables are float, not string
        self.small_stroke = small_stroke
        self.big_stroke = big_stroke
        self.small_freq = small_freq
        self.big_freq = big_freq

    def run(self):
        # check if at least one character is generated
        generateOne = False
        with open(file_path, encoding='utf16') as data:
        # got a bug: 'utf-8' codec can't decode byte 0xff in position 0
        # solution 1: change to utf-16
        # solution 2: use 'rb' read binary
            lines = data.readlines()
            for line in lines:
                # use the flag to check if the character meet all the conditions
                # even one unmet condition will cause the flag to be false
                matchCondition = True
                info = line.split()
                if self.initial:
                    if info[2] != self.initial  :
                        matchCondition = False
                if self.final:
                    if info[3] != self.final  :
                        matchCondition = False
                if self.tone:
                    if info[4] != self.tone:
                        matchCondition = False
                if self.radical != "all":
                    if info[8] != self.radical:
                        matchCondition = False
                if self.structure != "all":
                    if info[6] != self.structure:
                        matchCondition = False
                if self.liushu != "all":
                    if info[7] != self.liushu:
                        matchCondition = False
                ss = self.small_stroke
                bs = self.big_stroke
                sf = self.small_freq
                bf = self.big_freq
                if ss > bs:
                    ss, bs = bs, ss
                if sf > bf:
                    sf, bf = bf, sf
                if not ss < float(info[9]) < bs:
                    matchCondition = False
                if not sf < float(info[10]) < bf:
                    matchCondition = False
                if matchCondition:
                    self.generateResult.emit(line[:-1])
                    generateOne = True
        if generateOne == False:
            self.generateResult.emit("N/A "*11)


class MatchThread(QThread):
    matchResult = pyqtSignal(str)

    def __init__(self, parent = None):
        super(MatchThread, self).__init__(parent)

    def checkConditions(self, initial, final, tone, radical, structure, liushu, str_diff, freq_diff):
        self.initial = initial
        self.final = final
        self.tone = tone
        self.radical = radical
        self.structure = structure
        self.liushu = liushu
        self.str_diff = str_diff
        self.freq_diff = freq_diff

    def matchInput(self, txt):
        self.txt = txt

    def run(self):
        # same character may have multiple pronunciations, store them in a list
        match_input = []
        # check if the input character is in the dictionary
        inDict = False
        with open(file_path, encoding='utf16') as data:
            lines = data.readlines()
            for line in lines:
                if line[0] == self.txt:
                    inDict = True
                    match_input.append(line[:-1])
        if inDict == False:
            # send error message, there should be a space after N/A, otherwise, split() will report error
            self.matchResult.emit( self.txt + ' ' + 'N/A ' * 10)

        if inDict:
            # if the input character is in the dictionary, start to match
            if inDict == True:
                for match in match_input:
                    self.matchResult.emit(match)
                    match_info = match.split()
                    for line in lines:
                        isMatch = True
                        line_info = line.split()
                        # if same unicode, then not match
                        if match_info[1] == line_info[1]:
                            isMatch = False
                        # if self.initial is checked, then match initial
                        if self.initial:
                            if match_info[2] != line_info[2]:
                                isMatch = False
                        if self.final:
                            if match_info[3] != line_info[3]:
                                isMatch = False
                        if self.tone:
                            if match_info[4] != line_info[4]:
                                isMatch = False
                        if self.radical:
                            if match_info[8] != line_info[8]:
                                isMatch = False
                        if self.structure:
                            if match_info[6] != line_info[6]:
                                isMatch = False
                        if self.liushu:
                            if match_info[7] != line_info[7]:
                                isMatch = False
                        if self.str_diff >= 0:
                            if abs(float(match_info[9]) - float(line_info[9])) > float(self.str_diff):
                                isMatch = False
                        if self.freq_diff >= 0:
                            if abs(float(match_info[10]) - float(line_info[10])) > float(self.freq_diff):
                                isMatch = False
                        if isMatch:
                            self.matchResult.emit(line[:-1])
                    self.matchResult.emit("-- "*11)

class QueryThread(QThread):
    queryResult = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QueryThread, self).__init__(parent)

    def charInput(self, txt):
        self.txt = txt
        ##执行线程的run方法

    def run(self):
        query_result = ''
        # create a filter consists of space, numbers, letters, and punctuation
        noncharacter = ' ' + string.digits + string.ascii_letters + string.punctuation
        unique_char = []
        for char in self.txt:
            # if the char is not in the filter, then treat it as a Chinese character
            if char not in noncharacter and char not in unique_char:
                unique_char.append(char)

        for char in unique_char:
            dict_key = False
            with open(file_path, encoding='utf16') as data:
                lines = data.readlines()
                for line in lines:
                    if line[0] == char:
                        query_result = line[:-1]
                        self.queryResult.emit(query_result)
                        dict_key = True
            if dict_key == False:
                query_result = char + " "+ "N/A " * 10
                self.queryResult.emit(query_result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())