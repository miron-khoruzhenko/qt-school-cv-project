# This Python file uses the following encoding: utf-8
import sys
import os
from pathlib import Path


from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QFile, Slot, Signal, QObject, QThreadPool
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap, QImage


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget

import cv2
import numpy as np
import matplotlib.pyplot as plt

class Widget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        loader  = QUiLoader()
        path    = os.fspath(Path(__file__).resolve().parent / "form.ui")

        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)

        self.loaded_img_screen = self.ui.loaded_img
        self.loaded_img_graph = self.ui.loaded_img_graph

        self.processed_img_screen = self.ui.processed_img
        self.processed_img_graph = self.ui.processed_img_graph
        self.cv_load_image = 0
        self.pixmap = 0
        # self.label = self.ui.loaded_img

        self.ui.load_img_btn.clicked.connect(self.onOpen)
        self.ui.process_img_btn.clicked.connect(self.onProcces)



    
    def onPush(self):
        # self.
        # pixmap = 
        print(self.ui.label.text(), QPixmap)   

    def onProcessBtnPush(self):
        pass

    def onOpen(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        # print(file_dialog.exec())
        if file_dialog.exec(): # открытия диал окна
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                self.cv_load_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                # print(self.cv_load_image)
                self.pixmap = QPixmap(file_path)
                self.setBlocksImage(self.loaded_img_screen, self.loaded_img_graph, self.pixmap)


    def onProcces(self):
        img = self.getHistoEqualizatedImg(self.cv_load_image)
        hist = self.getFrequencyArray(img)
        plot = self.getPlotPixmap(hist)

        file_path = 'temp_img.png'

        cv2.imwrite(file_path, img)

        pixmap = QPixmap(file_path)

        # pixmap = self.convertToPixmap(img)

        self.setBlocksImage(self.processed_img_screen, self.processed_img_graph, pixmap)

    
    # def convertToPixmap(self, cv_img):
    #     cv_img = cv2.cvtColor(cv_img, cv2.gray)

    #     height, width, channel = cv_img.shape
    #     bytes_per_line = width * channel
    #     qimage = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format_RGB888)

    #     return qimage




    def setBlocksImage(self, img_block, graph_block, img):
        hist = self.getFrequencyArray(self.cv_load_image)

        plot_QPixmap = self.getPlotPixmap(hist)

        # pixmap.scaledToHeight(200)
        # self.loaded_img_screen.setPixmap(pixmap.scaled(200, 200))  # Set the image in the label
        print(self.loaded_img_screen)

        img_block.setPixmap(img.scaledToHeight(200))  # Set the image in the label
        graph_block.setPixmap(plot_QPixmap.scaledToHeight(200))  # Set the image in the label


    def getPlotPixmap(self, plot):
        plt.bar(range(256), plot)

        temp_file = 'temp_plot.png'
        plt.savefig(temp_file)

        return QPixmap(temp_file)
    

    def getFrequencyArray(self, cv_img):
        # Create an empty numpy array to store the histogram
        hist = np.zeros((256), dtype=int)

        # Iterate over each pixel in the image
        for i in range(cv_img.shape[0]):
            for j in range(cv_img.shape[1]):
                # Increment the histogram bin corresponding to the pixel value
                hist[cv_img[i,j]] += 1

        return hist


    def getHistoEqualizatedImg(self, cv_img):
        hist = self.getFrequencyArray(cv_img)

        cdf = np.cumsum(hist) 
        img_eq = ((cdf[cv_img]) * 255 / (cv_img.size)).astype(np.uint8)

        return img_eq
    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.wind
    widget = Widget()
    # widget.onPush()
    widget.show()
    
    sys.exit(app.exec())
