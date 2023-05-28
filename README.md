# **Image Processing Widget**

- [**Image Processing Widget**](#image-processing-widget)
	- [**Prerequisites**](#prerequisites)
	- [**Features**](#features)
	- [**Image Processing Techniques**](#image-processing-techniques)
	- [**Usage**](#usage)
	- [**Troubleshooting**](#troubleshooting)
	- [**License**](#license)
	- [**Acknowledgments**](#acknowledgments)


This is a Python application that allows users to load, process, and save images using various image processing techniques. The application provides a graphical user interface (GUI) built with PySide6 library.

## **Prerequisites**

Before running the application, make sure you have the following dependencies installed:

- Python 3.x
- OpenCV (cv2 module)
- NumPy
- PySide6

Installation

1. Clone the repository or download the code files to your local machine.

1. Install the required dependencies mentioned above.

1. Run the widget.py file using the following command:

	```bash
	python widget.py
	```

## **Features**

- **Load Image:** Click the "Load Image" button to open a file dialog and select an image file (supported formats: PNG, XPM, JPG, JPEG, BMP). The loaded image will be displayed in the "Loaded Image" section of the GUI.
- **Process Image:** After loading an image, click the "Process Image" button to apply image processing techniques. The processed image will be displayed in the "Processed Image" section of the GUI.
- **Adjust Slider:** Drag the vertical slider to adjust the processing condition. The value range is between 0 and 20 with 0.1 single step.
- **Save Image:** Click the "Save Image" button to save the processed image. A file dialog will open to choose the destination folder and provide a filename.

## **Image Processing Techniques**

The application applies the following image processing techniques to the loaded image:

1. Contrast Limited Adaptive Histogram Equalization (CLAHE): Enhances the contrast of the image based on the local histograms.
1. Gaussian Blur: Applies a Gaussian blur filter to the processed image.
1. Laplacian Filter: Detects edges and enhances details in the image.

## **Usage**

1. Launch the application.
1. Click the "Load Image" button and select an image file from your local machine.
1. The loaded image will be displayed in the "Loaded Image" section.
1. Adjust the vertical slider to set the processing condition (0-20).
1. Click the "Process Image" button to apply the image processing techniques.
1. The processed image will be displayed in the "Processed Image" section.
1. If desired, you can add points on the processed image by clicking on the image. Every two points will be connected with a red line, and the length of the line will be displayed below the image.
1. To save the processed image, click the "Save Image" button and choose the destination folder and filename.

Note: The application supports only grayscale images (loaded image and processed image).

## **Troubleshooting**

- If an image fails to load or process, make sure it is in a supported format (PNG, XPM, JPG, JPEG, BMP) and the file is not corrupted.
- Ensure that you have the necessary permissions to read from the file location and write to the save destination.

## **License**

This project is licensed under the ***MIT License***.

## **Acknowledgments**

The application uses the following libraries and frameworks:

- **OpenCV** - Computer vision and image processing library.
- **NumPy** - Numerical computing library for Python.
- **PySide6** - Python binding for the Qt framework.

The code structure and GUI design were inspired by various image processing applications and examples available online.