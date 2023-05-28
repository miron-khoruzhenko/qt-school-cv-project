# This Python file uses the following encoding: utf-8
import sys
import os
import math
from pathlib import Path


from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsPixmapItem, QGraphicsScene, QGraphicsLineItem
from PySide6.QtCore import QFile, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap, QColor, QPen

# from ui_form import Ui_Widget

import cv2
import numpy as np
import model

class Widget(QMainWindow,model.Proccess4Draw):
    def __init__(self, parent=None):

        super().__init__(parent)
        model.Proccess4Draw.__init__(self)
        
        loader  = QUiLoader()
        path    = os.fspath(Path(__file__).resolve().parent / "form.ui")

        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)

        self.slider_value=0.0

        # ========== GRAPIC SCREENS ==========
        self.loaded_img_screen = self.ui.loaded_img

        self.loaded_img_scene = QGraphicsScene()
        self.loaded_img_screen.setScene(self.loaded_img_scene)

        self.processed_img_screen = self.ui.processed_img

        self.processed_img_scene = QGraphicsScene()
        self.processed_img_screen.setScene(self.processed_img_scene)

        self.length_label = self.ui.length_label
        self.slider = self.ui.vertical_slider


        # ========== EVENTS ==========
        self.ui.load_img_btn.clicked.connect(self.onLoad)
        self.ui.process_img_btn.clicked.connect(self.onProcces)
        self.ui.save_btn.clicked.connect(self.onSave)
        self.processed_img_scene.mousePressEvent = self.onSceneClicked
        self.slider.valueChanged.connect(self.onSliderChange)

        # ========== GLOBAL VARS ==========
        self.cv_load_image = None
        self.cv_processed_image = None
        
        self.input_pixmap = None
        self.processed_pixmap = None

        self.point_count = 0
        self.points_arr = []
        self.line = None
        
    def onSliderChange(self, value):
        # self.slider_value=self.slider.value()
        print(value)


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


    def onSave(self):
        if not self.processed_pixmap:
            return
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.jpeg)", options=options)

        if save_path:
            cv2.imwrite(save_path + '.png', self.cv_processed_image)  # Сохранение изображения по выбранному пути
            print("Image saved successfully.")



    def onProcces(self):
        if not self.input_pixmap:
            return
        
        ddepth = cv2.CV_16S
        kernel_size = 3
        self.cv_processed_image = self.local_histogram_equalization(
            self.clahe_process(self.cv_load_image),condution=self.slider.value())
        src = self.get_blur_guassian(self.cv_processed_image)
        dst = cv2.Laplacian(src, ddepth, ksize=kernel_size)
        img2 = cv2.convertScaleAbs(dst)
        
        # self.cv_processed_image = self.getHistoEqualizatedImg(self.cv_load_image)
        self.cv_processed_image = self.addImg(img1=self.cv_processed_image, img2=img2)
        file_path = 'temp_img.png'
        cv2.imwrite(file_path, self.cv_processed_image)
        
        self.processed_pixmap = QPixmap(file_path)
        os.remove(file_path)

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

        # Если это третья точка, очищаем сцену
        if self.point_count % 2 == 0:

            self.line = QGraphicsLineItem()
            self.line.setPen(QPen(Qt.red, 2))
            # self.line.setLine(start_point.x(), start_point.y(), 200, 200)  # Укажите координаты конечной точки линии здесь
            self.line.setLine(
                self.points_arr[0][0] + int(dot_radius/2), 
                self.points_arr[0][1] + int(dot_radius/2), 
                self.points_arr[1][0] + int(dot_radius/2), 
                self.points_arr[1][1] + int(dot_radius/2)
            )

            distance = math.sqrt(
                (self.points_arr[0][0] - self.points_arr[1][0])**2 + 
                (self.points_arr[0][1] - self.points_arr[0][1])**2
            )
            distance = int(distance*100)/100

            self.processed_img_scene.addItem(self.line)
            self.length_label.setText('Length: ' + str(distance))

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
