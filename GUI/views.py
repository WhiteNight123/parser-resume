from PyQt6.QtWidgets import QWidget, QDialog, QFileDialog
from PyQt6.QtCore import QThread
from PyQt6.QtGui import QPixmap, QFont
from .jianli import JianLi
from functools import partial
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt

from .ui.main_window import Ui_widget
from .ui.parse_result_dialog import Ui_Dialog
from .ui.resume_visiual_dialog import Ui_Dialog2
import re


# 主界面
class Window(QWidget, Ui_widget):
    def __init__(self):
        super().__init__()
        self._setupUI()
        # 展示解析结果的dialog
        self.result_dialog = Result_Dialog()
        self.visiual_dialog = Resume_Visiual_Dialog()
        self._connectSignalsSlots()

    def _setupUI(self):
        self.setupUi(self)
        self.title_text.setStyleSheet("font-size: 20px;font-weight: bold;")
        self._updateStateWhenNoFile()
        self._updateStateWhenNoText()

    def _connectSignalsSlots(self):
        self.select_button.clicked.connect(self.select_file)
        self.parse_button1.clicked.connect(self.parseResume)
        self.parse_button2.clicked.connect(self.parseResume2)

    # 选择文件
    def select_file(self):
        file_dialog = QFileDialog()
        # 支持的文件格式
        file_format ="Word Files (*.docx);;Text Files (*.txt);;PDF Files (*.pdf);;PNG Files (*.png)"
        files, _ = file_dialog.getOpenFileNames(self, "选择文件", "", file_format)
        # 多文件简历分析
        if len(files) > 1:
            self.parseResume3()
        # 单文件简历分析
        elif len(files) == 1:
            file_path = files[0]
            self.file_path_label.setText(f"文件路径: {file_path}")
            self.selected_file_path = file_path
            self.loadFiles()

    # 上传文件
    def loadFiles(self):
        if hasattr(self, "selected_file_path"):
            destination_path = "./tmp"  # 保存文件的目标路径
            destination_file_path = f"{destination_path}/{self.selected_file_path.split('/')[-1]}"
            try:
                with open(self.selected_file_path, "rb") as source_file:
                    with open(destination_file_path, "wb") as destination_file:
                        destination_file.write(source_file.read())
                print("文件上传成功！")
                self._updateStateWhenFileLoaded()
            except Exception as e:
                print(f"文件上传失败: {str(e)}")
        else:
            print("请先选择要上传的文件！")

    # 根据文件提取简历信息
    def parseResume(self):
        self._updateStateWhenParsing()
        self._runJianLiThread()

    # 根据文字提取简历信息
    def parseResume2(self):
        text = self.resume_text_edit.toPlainText()
        if len(text) <= 20:
            self.file_path_label.setText("简历文字太短！")
            return
        self._updateStateWhenParsing()
        self._runJianLiThread2(text)

    # 提取多份简历
    def parseResume3(self):
        self._updateStateWhenParsing()
        self._runJianLiThread3()

    def _runJianLiThread(self):
        # 提取文件名
        suffix = re.search(r'[^\\/:*?"<>|\r\n]+$',
                           self.selected_file_path).group(0)
        path = "./tmp/" + suffix
        self._thread = QThread()
        self._jianli = JianLi()
        self._jianli.moveToThread(self._thread)
        # Rename
        self._thread.started.connect(partial(self._jianli.prase, path))
        # Update state
        self._jianli.resumeParsed.connect(self._updateStateWhenresumeParsed)
        self._jianli.resumeFiled.connect(self._praseFailed)
        # Clean up
        self._jianli.finished.connect(self._thread.quit)
        self._jianli.finished.connect(self._jianli.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        # Run the thread
        self._thread.start()

    def _runJianLiThread2(self, text):
        self._thread = QThread()
        self._jianli = JianLi()
        self._jianli.moveToThread(self._thread)
        # Rename
        self._thread.started.connect(partial(self._jianli.prase2, text))
        # Update state
        self._jianli.resumeParsed.connect(self._updateStateWhenresumeParsed)
        self._jianli.resumeFiled.connect(self._praseFailed)
        # Clean up
        self._jianli.finished.connect(self._thread.quit)
        self._jianli.finished.connect(self._jianli.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        # Run the thread
        self._thread.start()

    def _runJianLiThread3(self):
        self._thread = QThread()
        self._jianli = JianLi()
        self._jianli.moveToThread(self._thread)
        # Rename
        self._thread.started.connect(self._jianli.resume_visiual)
        # Update state
        self._jianli.resumeVisiualParsed.connect(
            self._updateStateWhenresumeVisiualParsed)
        self._jianli.resumeFiled.connect(self._praseFailed)
        # Clean up
        self._jianli.finished.connect(self._thread.quit)
        self._jianli.finished.connect(self._jianli.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        # Run the thread
        self._thread.start()

    # 解析完成后展示结果
    def _updateStateWhenresumeParsed(self, result):
        self.result_dialog.data = result
        self.result_dialog.updataUi()
        self.result_dialog.show()
        self.progressBar.setVisible(False)

    # 解析完成后展示结果
    def _updateStateWhenresumeVisiualParsed(self, result):
        self.file_path_label.setText("解析成功")
        self.visiual_dialog.data = result
        self.visiual_dialog.updataUi()
        self.visiual_dialog.show()
        self.progressBar.setVisible(False)

    # 解析失败
    def _praseFailed(self, msg):
        self.progressBar.setVisible(False)
        self.file_path_label.setText(msg)

    # 没有上传文件时的状态
    def _updateStateWhenNoFile(self):
        self.parse_button1.setEnabled(False)
        self.progressBar.setVisible(False)

    # 没有输入文本时的状态
    def _updateStateWhenNoText(self):
        self.progressBar.setVisible(False)

    # 上传文件后的状态
    def _updateStateWhenFileLoaded(self):
        self.parse_button1.setEnabled(True)

    # 正在解析的状态
    def _updateStateWhenParsing(self):
        self.parse_button1.setEnabled(False)
        self.file_path_label.setText("正在解析")
        self.progressBar.setVisible(True)


# 解析结果的Dialog
class Result_Dialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.title_text.setStyleSheet("font-size: 18px;font-weight: bold;")
        self._connectSignalsSlots()
        self.data = {}

    def _connectSignalsSlots(self):
        self.ok_button.clicked.connect(self.closeDialog)

    # 关闭弹窗
    def closeDialog(self):
        self.close()

    # 更新结果
    def updataUi(self):
        pixmap1 = QPixmap('./resources/photo.png')
        self.user_image.setPixmap(pixmap1)
        self.user_image.setScaledContents(True)
        pixmap2 = QPixmap('./resources/photo.png')
        self.name_image.setPixmap(pixmap2)
        self.name_image.setScaledContents(True)
        data = self.data
        pixmap3 = QPixmap('./resources/birthday.png')
        self.birthday_image.setPixmap(pixmap3)
        self.birthday_image.setScaledContents(True)
        pixmap4 = QPixmap('./resources/age.png')
        self.age_image.setPixmap(pixmap4)
        self.age_image.setScaledContents(True)
        pixmap5 = QPixmap('./resources/politics.png')
        self.politics_image.setPixmap(pixmap5)
        self.politics_image.setScaledContents(True)
        pixmap6 = QPixmap('./resources/education.png')
        self.education_image.setPixmap(pixmap6)
        self.education_image.setScaledContents(True)
        pixmap7 = QPixmap('./resources/phone.png')
        self.phone_image.setPixmap(pixmap7)
        self.phone_image.setScaledContents(True)
        pixmap8 = QPixmap('./resources/school.png')
        self.school_image.setPixmap(pixmap8)
        self.school_image.setScaledContents(True)
        pixmap9 = QPixmap('./resources/work_year.png')
        self.work_year_image.setPixmap(pixmap9)
        self.work_year_image.setScaledContents(True)
        pixmap10 = QPixmap('./resources/label.png')
        self.label_image.setPixmap(pixmap10)
        self.label_image.setScaledContents(True)
        pixmap11 = QPixmap('./resources/salary.png')
        self.salary_image.setPixmap(pixmap11)
        self.salary_image.setScaledContents(True)
        pixmap12 = QPixmap('./resources/work.png')
        self.work_image.setPixmap(pixmap12)
        self.work_image.setScaledContents(True)
        pixmap13 = QPixmap('./resources/priority.png')
        self.priority_image.setPixmap(pixmap13)
        self.priority_image.setScaledContents(True)
        self.name_text.setText(data['姓名'])
        self.birthday_text.setText(data['出生年月'])
        self.age_text.setText(data['年龄'])
        self.political_text.setText('群众')
        self.degree_text.setText(data['最高学历'])
        self.phone_text.setText(data['电话'])
        self.school_text.setText(data['毕业院校'])
        self.work_year_text.setText(str(data['工作年限']))
        self.player_label1_text.setText(data['标签1'])

        self.player_label2_text.setText(data['标签2'])
        self.player_label3_text.setText(data.get('标签3', ""))
        self.salary_text.setText(data['预计薪酬'])
        self.match_position_text.setText(data.get('匹配岗位', "暂无"))
        if '优先级' not in data:
            self.priority_text.setText("暂无")
        if '市场' in data.get('匹配岗位', "暂无") :
            pixmap14 = QPixmap('./resources/market.png')
            self.match_position_image.setPixmap(pixmap14)
            self.match_position_image.setScaledContents(True)
        elif '设计' in data.get('匹配岗位', "暂无") :
            pixmap14 = QPixmap('./resources/design.png')
            self.match_position_image.setPixmap(pixmap14)
            self.match_position_image.setScaledContents(True)
        elif '主管' in data.get('匹配岗位', "暂无") :
            pixmap14 = QPixmap('./resources/manager.png')
            self.match_position_image.setPixmap(pixmap14)
            self.match_position_image.setScaledContents(True)
        elif '产品' in data.get('匹配岗位', "暂无") :
            pixmap14 = QPixmap('./resources/product.png')
            self.match_position_image.setPixmap(pixmap14)
            self.match_position_image.setScaledContents(True)
        elif '财' in data.get('匹配岗位', "暂无") :
            pixmap14 = QPixmap('./resources/finance.png')
            self.match_position_image.setPixmap(pixmap14)
            self.match_position_image.setScaledContents(True)

# 解析结果的Dialog

class Resume_Visiual_Dialog(QDialog, Ui_Dialog2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.title_text.setStyleSheet("font-size: 18px;font-weight: bold;")
        self._connectSignalsSlots()
        self.data = {}

    def _connectSignalsSlots(self):
        self.ok_button.clicked.connect(self.closeDialog)

    # 关闭弹窗
    def closeDialog(self):
        self.close()

    # 更新结果
    def updataUi(self):
        data = self.data
        plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
        plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题
        fig1 = Figure(figsize=(8, 1))
        fig1.subplots_adjust(left=0.15, bottom=0.25)  # 调整边缘空间
        canvas1 = FigureCanvas(fig1)
        ax1 = fig1.add_subplot(111)
        # 绘制学历统计柱状图
        education_counts = data['最高学历'].value_counts()
        education_counts.plot(kind='bar', ax=ax1)
        ax1.set_title('学历统计')
        ax1.set_xlabel('学历')
        ax1.set_ylabel('人数')
        self.verticalLayout_1.addWidget(canvas1)

        # 绘制年龄段统计饼图
        age_bins = [0, 20, 30, 40, 50, 100]
        age_labels = ['20以下', '20-30', '30-40', '40-50', '50以上']
        age_groups = pd.cut(data['年龄'], bins=age_bins,
                            labels=age_labels, right=False)
        age_counts = age_groups.value_counts()
        fig2 = Figure(figsize=(8, 8))
        canvas2 = FigureCanvas(fig2)
        ax2 = fig2.add_subplot(111)
        age_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax2)
        ax2.set_title('年龄段统计')
        ax2.set_ylabel('')
        self.verticalLayout_2.addWidget(canvas2)

        # 毕业院校统计水平条形图：
        fig3 = Figure(figsize=(10, 6))
        fig3.subplots_adjust(left=0.3, bottom=0.15)  # 调整边缘空间
        canvas3 = FigureCanvas(fig3)
        ax3 = fig3.add_subplot(111)
        top_universities = self.data['毕业院校'].value_counts().nlargest(10)
        top_universities.plot(kind='barh', ax=ax3)
        ax3.set_title('毕业院校统计')
        ax3.set_xlabel('人数')
        ax3.set_ylabel('毕业院校')
        self.verticalLayout_3.addWidget(canvas3)

        # 工作年限统计饼图：
        fig4 = Figure(figsize=(100, 100))
        canvas4 = FigureCanvas(fig4)
        ax4 = fig4.add_subplot(111)
        work_experience_counts = data['工作年限'].value_counts()
        work_experience_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax4)
        ax4.set_title('工作年限统计')
        ax4.set_ylabel('')
        self.verticalLayout_4.addWidget(canvas4)
