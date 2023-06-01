# This Python file uses the following encoding: utf-8
import sys
import os
import math
from pathlib import Path


from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsPixmapItem, QGraphicsScene, QGraphicsLineItem
from PySide6.QtCore import QFile, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap, QColor, QPen


import cv2
import numpy as np
import model

class BaseWidget(QMainWindow, model.Proccess4Draw):
  def __init__(self, parent=None):
    super().__init__(parent)
    model.Proccess4Draw.__init__(self)
    
    loader  = QUiLoader()
    path    = os.fspath(Path(__file__).resolve().parent / "ui/form.ui")

    ui_file = QFile(path)
    ui_file.open(QFile.ReadOnly)
    self.ui = loader.load(ui_file)
    ui_file.close()
    self.setCentralWidget(self.ui)
    self.setWindowTitle("Image Processing")
            

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

    self.win = "ui/form.ui"