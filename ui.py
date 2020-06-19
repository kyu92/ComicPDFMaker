from PyQt5.QtWidgets import QTextEdit, QWidget, QPushButton, QLabel, \
    QListWidget, QApplication, QHBoxLayout, QVBoxLayout, QFileDialog, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush, QCursor, QIcon, QMouseEvent
from PyQt5.QtCore import QSize, QEvent, Qt, pyqtSignal, QUrl
import sys
import os
from const import Const
import logic

index = 1


class ExecuteLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent=parent)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()


class HelpWindow(QWidget):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        self.window_height = screen_rect.height() // 3
        self.window_width = self.window_height
        self.resize(self.window_width, self.window_height)
        self.move(self.window_width * 2, self.window_width)
        self.setObjectName("help_window")
        self.init_ui()

    def init_ui(self):
        confirm_btn = QPushButton(self)
        confirm_btn.setText("确认")
        confirm_btn.clicked.connect(self.destroy)
        help_label = QLabel(self)
        help_label.setText(Const.HELP_STR)
        size = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size.setHorizontalStretch(0)
        size.setVerticalStretch(0)
        size.setHeightForWidth(help_label.sizePolicy().hasHeightForWidth())
        help_label.setSizePolicy(size)
        help_label.setWordWrap(True)
        h_layout = QHBoxLayout()
        h_layout2 = QHBoxLayout()
        v_layout = QVBoxLayout()
        h_layout.addWidget(help_label)
        h_layout2.addStretch(1)
        h_layout2.addWidget(confirm_btn)
        v_layout.addLayout(h_layout)
        v_layout.addStretch(1)
        v_layout.addLayout(h_layout2)
        self.setLayout(v_layout)


class LogBox(QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)

    def set_log(self, content):
        if isinstance(content, str) or isinstance(content, int)\
                or isinstance(content, float):
            # thread_it(self.append, f"{content}")
            self.append(f"{content}")
        elif isinstance(content, list) or isinstance(content, tuple):
            for each in content:
                self.set_log(each)
        elif isinstance(content, dict):
            for key in content:
                self.set_log(content[key])


class RootWindows(QWidget):

    def __init__(self):
        super().__init__()
        self.comic_files_path = list()
        self.setObjectName("root_window")
        self.setWindowTitle("ComicPDFMaker")
        self.setWindowIcon(QIcon(":/resources/ico.ico"))
        self.test_button = ExecuteLabel(self)
        self.test_button.clicked.connect(self.execute)
        self.files_list = QListWidget(self)
        self.files_list.setObjectName("files_list")
        self.log_box = LogBox(self)
        self.log_box.setObjectName("log_box")
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        self.window_height = screen_rect.height() // 2
        self.window_width = screen_rect.width() // 2
        self.init_ui()

    def init_ui(self):
        self.resize(self.window_width, self.window_height)
        self.test_button.setPixmap(QPixmap(":/resources/start_leave.png").scaled(
            QSize(self.window_width // 8, self.window_height // 8), Qt.KeepAspectRatio))
        self.test_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.test_button.setMouseTracking(True)
        self.test_button.installEventFilter(self)
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(":/resources/bg.png").scaled(
            QSize(self.window_width, self.window_height), Qt.KeepAspectRatio)))
        self.setPalette(palette)
        help_btn = QPushButton(self)
        help_btn.setObjectName("help_btn")
        help_btn.setToolTip("点击此处查看使用帮助")
        help_btn.setStyleSheet("""#help_btn{
                    height:%s;
                    width:%s;
                    border: 0;
                    border-image: url(:/resources/help.png);
        }""" % (self.window_height // 12, self.window_height // 12))
        help_btn.setCursor(QCursor(Qt.PointingHandCursor))
        help_btn.clicked.connect(self.get_help)
        widget_title1 = QLabel(self)
        widget_title2 = QLabel(self)
        widget_title1.setText("文件列表")
        widget_title1.setFont(QFont("仿宋", 10))
        widget_title1.setObjectName("widget_title_files_list")
        widget_title2.setText("日志")
        widget_title2.setFont(QFont("仿宋", 10))
        widget_title2.setObjectName("widget_title_log")
        open_files_btn = QPushButton(self)
        open_files_btn.setText("选择文件夹")
        open_files_btn.setFont(QFont("楷体", 15))
        open_files_btn.setObjectName("select_files_btn")
        open_files_btn.setCursor(QCursor(Qt.PointingHandCursor))
        open_files_btn.clicked.connect(self.select_files)
        h_layout = QHBoxLayout()
        v_layout = QVBoxLayout()
        h_layout2 = QHBoxLayout()
        h_layout3 = QHBoxLayout()
        h_layout4 = QHBoxLayout()
        h_layout.addWidget(self.test_button)
        h_layout.addStretch(1)
        h_layout.addWidget(help_btn)
        h_layout2.addWidget(open_files_btn)
        h_layout2.addStretch(1)
        h_layout3.addWidget(widget_title1)
        h_layout3.addStretch(2)
        h_layout3.addWidget(widget_title2, stretch=8)
        h_layout4.addWidget(self.files_list)
        h_layout4.addWidget(self.log_box, stretch=1)
        v_layout.addLayout(h_layout)
        v_layout.addLayout(h_layout2)
        v_layout.addLayout(h_layout3)
        v_layout.addLayout(h_layout4)
        self.setLayout(v_layout)

    def eventFilter(self, obj, event) -> bool:
        # print(obj, event)
        if obj == self.test_button:
            if event.type() == QEvent.Enter:
                self.test_button.setPixmap(QPixmap(":/resources/start_enter.png").scaled(
                    QSize(self.window_width // 8, self.window_height // 8), Qt.KeepAspectRatio))
            elif event.type() == QEvent.Leave:
                self.test_button.setPixmap(QPixmap(":/resources/start_leave.png").scaled(
                    QSize(self.window_width // 8, self.window_height // 8), Qt.KeepAspectRatio))
        return QWidget.eventFilter(self, obj, event)

    def select_files(self):
        global index
        openfile = None
        if os.name == 'nt':
            openfile = QFileDialog.getExistingDirectoryUrl(self, '选择文件夹',
                                                           QUrl(os.path.join(os.path.expanduser('~'), "Desktop")))
        else:
            openfile = QFileDialog.getExistingDirectoryUrl(self, '选择文件夹',
                                                           QUrl('/'))
        if not openfile.isEmpty():
            part = openfile.path().replace('/', '', 1)
            dirs = os.listdir(part)
            for each in dirs:
                if os.path.isfile(f"{part}/{each}"):
                    self.files_list.addItem(f'---------第{index}部分---------')
                    self.files_list.addItem(f"{each}")
                    print(f"{each}是文件，已跳过")
                    logic.thread_it(self.log_box.set_log, f"{each}是文件，已跳过")
                    index += 1
                else:
                    self.files_list.addItem(f'---------第{index}部分---------')
                    self.files_list.addItems(os.listdir(f"{part}/{each}"))
                    files = list(map(lambda file: f"{part}/{each}/{file}", os.listdir(f"{part}/{each}")))
                    self.comic_files_path += files
                    index += 1
            self.comic_files_path = list(set(self.comic_files_path))
            self.comic_files_path.sort()
            print(self.comic_files_path)

    def get_help(self):
        help_window = HelpWindow(self)
        help_window.show()

    def execute(self):
        # name = self.output_name.text()
        if os.name == 'nt':
            path = QFileDialog.getSaveFileUrl(
                self, "请保存文件", os.path.join(os.path.expanduser('~'), "Desktop"), "pdf files(*.pdf)")
            # type: (QUrl, str)
        else:
            path = QFileDialog.getSaveFileUrl(
                self, "请保存文件", '/',
                "pdf files(*.pdf)")  # type: (QUrl, str)
        name = path[0].url()
        logic.thread_it(logic.rea, self.comic_files_path, name, self.log_box)


if __name__ == '__main__':
    import resources
    resources.qInitResources()
    app = QApplication(sys.argv)
    app.setStyleSheet(Const.QSS)
    root = RootWindows()
    root.show()
    sys.exit(app.exec())