from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QToolBar
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QImage

import cv2


class VideoProcessingWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Video Processing")

        self.video_widget = QWidget()
        self.video_layout = QVBoxLayout(self.video_widget)
        self.video_label = QLabel(self.video_widget)
        self.video_layout.addWidget(self.video_label)

        self.open_button = QPushButton("Open Video")
        self.open_button.clicked.connect(self.openVideo)

        self.toolbar = QToolBar()
        self.toolbar.addWidget(self.open_button)
        self.addToolBar(self.toolbar)

        self.setCentralWidget(self.video_widget)

        self.video_path = ""
        self.video_capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.processVideoFrame)

    def openVideo(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Video Files (*.mp4 *.avi)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.video_path = selected_files[0]
                self.video_capture = cv2.VideoCapture(self.video_path)
                self.timer.start(30)  # Запускаем таймер для обработки каждого кадра

    def processVideoFrame(self):
        ret, frame = self.video_capture.read()
        if not ret:
            self.timer.stop()
            return

        # Обработка кадра с использованием OpenCV
        processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Отображение обработанного кадра в QLabel
        q_image = self.convertFrameToQImage(processed_frame)
        pixmap = QPixmap.fromImage(q_image)
        self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio))

    def convertFrameToQImage(self, frame):
        height, width = frame.shape
        bytes_per_line = width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        return q_image


if __name__ == "__main__":
    app = QApplication([])
    window = VideoProcessingWindow()
    window.show()
    app.exec()
