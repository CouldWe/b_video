import sys

from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLineEdit, QPushButton, QLabel
from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout, QMessageBox
from save_file import MyThread


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('bilibili视频解析')
        self.resize(800,200)
        screen_pos=QDesktopWidget().availableGeometry().center()
        qrect=self.frameGeometry()
        qrect.moveCenter(screen_pos)
        window_layout=QVBoxLayout()
        window_layout.addLayout(self.init_form())
        window_layout.addLayout(self.init_footer())
        self.setLayout(window_layout)
        self.show()
    def init_form(self):
        form_layout=QHBoxLayout()
        self.url_input=QLineEdit()
        self.url_input.setPlaceholderText('请输入视频链接')
        self.url_input.setFixedHeight(40)
        form_layout.addWidget(self.url_input)
        return form_layout
    def init_footer(self):
        footer_layout=QHBoxLayout()
        self.status_label=QLabel('')
        footer_layout.addWidget(self.status_label)
        footer_layout.addStretch()
        self.stop_btn = QPushButton('清除')
        self.stop_btn.setFixedHeight(40)
        self.stop_btn.setFixedWidth(60)
        self.stop_btn.clicked.connect(self.stop_task)
        footer_layout.addWidget(self.stop_btn)

        self.start_btn=QPushButton('下载')
        self.start_btn.setFixedHeight(40)
        self.start_btn.setFixedWidth(60)
        self.start_btn.clicked.connect(self.start_task)
        footer_layout.addWidget(self.start_btn)
        return footer_layout
    def stop_task(self):
        if self.url_input.text() == '':
            return
        self.status_label.setText('')
        self.url_input.clear()
    def start_task(self):
        if self.url_input.text() == '':
            QMessageBox.warning('error','链接为空')
            return
        self.status_label.setText('下载中')
        print(self.url_input.text())
        th=MyThread(self.url_input.text(),self)
        th.success.connect(self.task_success)
        th.start()
    def task_success(self, result_status):
        self.status_label.setText('下载完成')
