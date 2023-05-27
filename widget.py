# This Python file uses the following encoding: utf-8
import sys
import os
from pathlib import Path


from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsPixmapItem, QGraphicsScene, QGraphicsLineItem
from PySide6.QtCore import QFile, Slot, Signal, QObject, QThreadPool, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap, QImage, QColor, QPen

from ui_form import Ui_Widget

import cv2
import numpy as np

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


        # ========== GRAPIC SCREENS ==========
        self.loaded_img_screen = self.ui.loaded_img

        self.loaded_img_scene = QGraphicsScene()
        self.loaded_img_screen.setScene(self.loaded_img_scene)

        self.processed_img_screen = self.ui.processed_img

        self.processed_img_scene = QGraphicsScene()
        self.processed_img_screen.setScene(self.processed_img_scene)


        # ========== EVENTS ==========
        self.ui.load_img_btn.clicked.connect(self.onLoad)
        self.ui.process_img_btn.clicked.connect(self.onProcces)
        self.processed_img_scene.mousePressEvent = self.onSceneClicked


        # ========== GLOBAL VARS ==========
        self.cv_load_image = 0
        self.input_pixmap = 0
        self.processed_pixmap = 0
        self.point_count = 0
        self.points_arr = []
        self.line = None


    def onLoad(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec(): # открытия диал окна
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                self.cv_load_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                self.input_pixmap = QPixmap(file_path)
                self.setBlocksImage(self.loaded_img_screen, self.loaded_img_scene, self.input_pixmap)



    def onProcces(self):
        if not self.input_pixmap:
            return
        
        img = self.getHistoEqualizatedImg(self.cv_load_image)

        file_path = 'temp_img.png'
        cv2.imwrite(file_path, img)
        self.processed_pixmap = QPixmap(file_path)

        self.setBlocksImage(self.processed_img_screen, self.processed_img_scene, self.processed_pixmap)



    def setBlocksImage(self, graphic_block, graphic_scene, img):
        graphic_scene.clear()

        # Create a QGraphicsPixmapItem with the given QPixmap
        pixmap_item = QGraphicsPixmapItem(img)

        # Add the QGraphicsPixmapItem to the QGraphicsScene
        graphic_scene.addItem(pixmap_item)

        # Fit the view to the pixmap size
        graphic_block.fitInView(pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)



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
    


    # ========== EVENTS ==================== EVENTS ==========
    # ========================================================

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if self.input_pixmap and self.processed_pixmap:
            self.setBlocksImage(self.loaded_img_screen, self.loaded_img_scene, self.input_pixmap)
            self.setBlocksImage(self.processed_img_screen, self.processed_img_scene, self.processed_pixmap)

        elif self.input_pixmap:
            self.setBlocksImage(self.loaded_img_screen, self.loaded_img_scene, self.input_pixmap)



    def onSceneClicked(self, event):
        if not self.processed_pixmap:
            return
        
        dot_radius = 10

        #? Если изображения нет то точки будут задавать ширину и из за этого их координаты будут не верны.
        pos = event.scenePos()
        scene_rect = self.processed_img_scene.sceneRect()

        # if not scene_rect.contains(pos):
        # Если координаты выходят за границы сцены, ограничиваем их в пределах сцены
        # Единица дает место погрешности при округлении
        pos.setX(
            max(scene_rect.left() + int(dot_radius/2) + 1, 
                min(pos.x(), scene_rect.right() - int(dot_radius/2) - 1)
                ))
        pos.setY(
            max(scene_rect.top() + int(dot_radius/2) + 1, 
                min(pos.y(), scene_rect.bottom() - int(dot_radius/2) - 1)
                ))
            

        # Увеличиваем счетчик добавленных точек 
        self.point_count += 1
        dot_coords = (pos.x()-int(dot_radius/2),pos.y()-int(dot_radius/2))

        
        self.points_arr.append(dot_coords)

        # Рисуем красную точку на сцене в месте клика
        self.processed_img_scene.addEllipse(
            dot_coords[0], dot_coords[1],
            dot_radius, dot_radius, 
            QColor("red")
            )
        # self.processed_img_scene.addEllipse(
        #     pos.x()-int(dot_radius/2), 
        #     pos.y()-int(dot_radius/2), 
        #     dot_radius, dot_radius, 
        #     QColor("red")
        #     )
        # Если это третья точка, очищаем сцену
        if self.point_count % 2 == 0:

            self.line = QGraphicsLineItem()
            self.line.setPen(QPen(Qt.black, 2))
            # self.line.setLine(start_point.x(), start_point.y(), 200, 200)  # Укажите координаты конечной точки линии здесь
            self.line.setLine(
                self.points_arr[0][0] + int(dot_radius/2), 
                self.points_arr[0][1] + int(dot_radius/2), 
                self.points_arr[1][0] + int(dot_radius/2), 
                self.points_arr[1][1] + int(dot_radius/2))
            
            self.processed_img_scene.addItem(self.line)

        elif self.point_count % 3 == 0:
            if self.line is not None:
                self.processed_img_scene.removeItem(self.line)
                self.line = None
            self.setBlocksImage(
                self.processed_img_screen, 
                self.processed_img_scene, 
                self.processed_pixmap
                )

            self.point_count = 0
            self.points_arr = []




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    
    sys.exit(app.exec())
