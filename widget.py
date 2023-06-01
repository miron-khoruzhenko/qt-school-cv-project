# This Python file uses the following encoding: utf-8
import sys
import os
import math
from pathlib import Path


from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsPixmapItem, QGraphicsScene, QGraphicsLineItem
from PySide6.QtCore import QFile, Qt, QTimer
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap, QColor, QPen, QImage


import cv2
import numpy as np
import model


class Widget(QMainWindow,model.Proccess4Draw):
    def __init__(self, parent=None):

        super().__init__(parent)
        model.Proccess4Draw.__init__(self)
        
        self.winName = "ui/image_process.ui"
        self.winTitle = "Image Processing"
        self.mode = 'image'

        self.setupUI(self.winName, self.winTitle)


    def setupUI(self, winName, title):
        loader  = QUiLoader()
        path    = os.fspath(Path(__file__).resolve().parent / winName)

        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)
        self.setWindowTitle(title)

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
        self.ui.load_img_btn.clicked.connect(self.onLoadBtnPress)

        self.ui.change_window.clicked.connect(self.changeWindows)

        self.processed_img_scene.mousePressEvent = self.onSceneClicked


        # ========== GLOBAL VARS ==========
        self.cv_load_image = None
        self.cv_processed_image = None
        
        self.input_pixmap = None
        self.processed_pixmap = None

        self.point_count = 0
        self.points_arr = []
        self.line = None

        self.is_timer_working = None

        if self.mode == "image":
            self.ui.process_img_btn.clicked.connect(self.onProcessImg)
            self.ui.save_btn.clicked.connect(self.onSaveBtnPress)

        else:
            self.ui.process_video_btn.clicked.connect(self.onProcessVideo)
            self.ui.stop_btn.clicked.connect(self.onStopContinueBtnPress)
            self.timer = 0
            self.is_timer_working = False


    def changeWindows(self):

        if self.mode == "image":
            self.winName = "ui/video_process.ui"
            self.winTitle = "Video Processing"
            self.mode = "video"

        else:
            self.winName = "ui/image_process.ui"
            self.winTitle = "Image Processing"
            self.mode = "image"
            if self.timer != 0:
                self.timer.stop()
                self.timer = 0

        self.setupUI(self.winName, self.winTitle)


    # ========== OnPress ==================== OnPress ==========
    # ==========================================================


    def onLoadBtnPress(self):
        if self.mode == "image":
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
        else:
            video_path, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi)")
            if video_path:
                self.video_capture = cv2.VideoCapture(video_path)
                self.processVideo()  # Начало обработки видео


    def onSaveBtnPress(self):
        if not self.processed_pixmap:
            return
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.jpeg)", options=options)

        if save_path:
            cv2.imwrite(save_path + '.png', self.cv_processed_image)  # Сохранение изображения по выбранному пути
            print("Image saved successfully.")


    def onProcessImg(self):
        if not self.input_pixmap:
            return
        
        self.cv_processed_image = self.getClaheHisto(self.cv_load_image)

        self.processed_pixmap = self.convertFrameToPixmap(self.cv_processed_image)

        self.setBlocksImage(self.processed_img_screen, self.processed_img_scene, self.processed_pixmap)


    def onProcessVideo(self):
        if self.timer != 0:
            return
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.processVideo)
        self.timer.start(30)  # Запускаем таймер
        self.is_timer_working = True


    def onStopContinueBtnPress(self):
        if self.timer == 0:
            return 
    
        if self.is_timer_working:
            self.timer.stop()
            self.is_timer_working = False
        else:
            self.timer.start(30)
            self.is_timer_working = True


    def processVideo(self):        
        ret, frame = self.video_capture.read()


        if not ret:
            self.timer.stop()
            self.timer = 0 
            self.is_timer_working = False
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        processed_frame = self.getClaheHisto(frame)

        self.input_pixmap = self.convertFrameToPixmap(frame)
        self.processed_pixmap = self.convertFrameToPixmap(processed_frame)

        self.setBlocksImage(self.loaded_img_screen, self.loaded_img_scene, self.input_pixmap)
        self.setBlocksImage(self.processed_img_screen, self.processed_img_scene, self.processed_pixmap)


    def convertFrameToPixmap(self, frame):
        height, width = frame.shape

        qimage = QImage(frame.data, width, height, QImage.Format_Grayscale8)

        pixmap = QPixmap.fromImage(qimage)

        return pixmap


    def setBlocksImage(self, graphic_block, graphic_scene, img):
        graphic_scene.clear()
        pixmap_item = QGraphicsPixmapItem(img)
        graphic_scene.addItem(pixmap_item)
        graphic_block.fitInView(pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)

    
    def clearGraphicItems(self):
        # Удаляет линии и точки со сцены. 
        # Должен быть до setBlockImage потому что там идет отчистка сцены
        if self.line:
            self.processed_img_scene.removeItem(self.line)
            self.line = None

        self.point_count = 0
        self.points_arr = []


    def getClaheHisto(self, img):
        ddepth = cv2.CV_16S
        kernel_size = 3

        processed_img = self.clahe_process(img, self.slider.value()/100)

        src = self.get_blur_guassian(processed_img)
        dst = cv2.Laplacian(src, ddepth, ksize=kernel_size)
        img2 = cv2.convertScaleAbs(dst)
        
        return self.addImg(img1=processed_img, img2=img2)



    # ========== EVENTS ==================== EVENTS ==========
    # ========================================================

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if self.input_pixmap and self.processed_pixmap:
            self.clearGraphicItems() # должен быть выше setBlocksImage
            self.setBlocksImage(self.loaded_img_screen, self.loaded_img_scene, self.input_pixmap)
            self.setBlocksImage(self.processed_img_screen, self.processed_img_scene, self.processed_pixmap)

        elif self.input_pixmap:
            self.setBlocksImage(self.loaded_img_screen, self.loaded_img_scene, self.input_pixmap)




    def onSceneClicked(self, event):

        if not self.processed_pixmap or self.is_timer_working:
            return
        
        dot_radius = 10

        #? Если изображения нет то точки будут задавать ширину и из за этого их координаты будут не верны.
        pos = event.scenePos()
        scene_rect = self.processed_img_scene.sceneRect()

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
                (self.points_arr[0][0] - self.points_arr[0][1])**2 + 
                (self.points_arr[1][0] - self.points_arr[1][1])**2
            )
            distance = int(distance*100)/100

            self.processed_img_scene.addItem(self.line)
            self.length_label.setText('Length: ' + str(distance))

        elif self.point_count % 3 == 0:
            self.clearGraphicItems()

            self.setBlocksImage(
                self.processed_img_screen, 
                self.processed_img_scene, 
                self.processed_pixmap
                )





if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    
    sys.exit(app.exec())