import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QFileDialog, QSlider, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QRadioButton, QButtonGroup,)
from PyQt5.QtGui import QFont, QFontDatabase, QColor, QPainter, QImage, QPixmap
import pyqtgraph.opengl as gl
from pyqtgraph.opengl import GLViewWidget
from PyQt5.QtCore import Qt, QTimer, QEvent
import pyqtgraph as pg

import numpy as np
import pandas as pd


class GLWidget(gl.GLViewWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.overlay_text = {}

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Helvetica", 16))

        for text, x, y, size in self.overlay_text.values():
            painter.setFont(QFont("Helvetica", size))
            painter.drawText(x, y, text)

    def update_overlay_text(self, key, text, x, y, size):
        self.overlay_text.update({key: (text, x, y, size)})
        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.gesture_dictionary = {
            0: "fist",
            1: "spiderman",
            2: "OK",
            3: "claw",
            4: "stretch",
            5: "point",
            6: "pinch",
            7: "close",
            8: "three point",
            9: "gun",
            10: "six",
            11: "thumbs up",
            12: "relax",
            13: "open",
            14: "down",
            15: "up",
            16: "left",
            17: "right",
            18: None,
        }

        self.picture_to_gesture = {
            'gesture2': "claw",
            'gesture3': "spiderman",
            'gesture4': "six",
            'gesture6': "OK",
            'gesture7': "point",
            'gesture8': "gun",
            'gesture9': "thumbs up",
            'gesture10': "stretch",
            'gesture11': "fist",
            'gesture12': "three point",
            'gesture13': "pinch",
            'gesture14': "close",
            'wrist1': "right",
            'wrist2': "up",
            'wrist3': "down",
            'wrist4': "open",
            'wrist5': "left",
        }


        # Initialize GUI components
        handpose_graphs = QHBoxLayout()
        self.gl_widget = GLWidget()
        self.gl_widget.update_overlay_text("title", "Mediapipe Handpose (Actual)", 10, 30, 14)
        self.gl_widget.sizeHint = lambda: pg.QtCore.QSize(800, 400)  # Set a larger window size

        handpose_graphs.addWidget(self.gl_widget)

        self.eit_plot = pg.PlotWidget()
        self.eit_plot.showGrid(x = True, y = True)
        self.eit_plot.setLabel('left', 'EIT Signal')
        self.eit_plot.setLabel('bottom', 'Linux Timestamp', units ='index')
        pen_colors = ['r', 'g', 'b', 'y', 'm', 'c', (255, 165, 0), (128, 0, 128)]
        self.eit_plots = [self.eit_plot.plot(pen=pen_colors[i]) for i in range(8)]

        self.gesture_plot = pg.PlotWidget()
        self.gesture_plot.showGrid(x = True, y = True)
        self.gesture_plot.setLabel('left', 'Gesture')
        self.gesture_plot.setLabel('bottom', 'Linux Timestamp', units ='index')
        self.gesture_plots = [self.gesture_plot.plot(pen=pen_colors[i]) for i in range(2)]

        self.timeline = QSlider(Qt.Horizontal)
        self.timeline.setTickPosition(QSlider.NoTicks)  # No tick marks
        self.timeline.setSingleStep(1)  # Set the single step to 1 for fine control
        self.timeline.setMinimum(0)  # Start of your range
        self.timeline.setMaximum(4999)  # End of your range (5000 points)
        self.timeline.valueChanged.connect(self.timeline_value_changed)

        control_buttons = QHBoxLayout()
        self.load_button = QPushButton('Load File')
        self.load_button.clicked.connect(self.open_file_dialog)
        self.play_button = QPushButton('Play', checkable=True)
        self.play_button.clicked.connect(self.play_button_clicked)

        control_buttons.addWidget(self.load_button)
        control_buttons.addWidget(self.play_button)

        self.annotation_enabled = False
        self.playing = False



        # Layout setup
        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        layout.addLayout(handpose_graphs)
        layout.addWidget(self.gesture_plot)
        layout.addWidget(self.eit_plot)
        layout.addWidget(self.timeline)
        layout.addLayout(control_buttons)
        

        self.labeled_data = None
        self.original_hand_data = None
        self.prelabeled_gestures = None
        self.index_value = 0

        # Set the central widget and show the GUI
        self.setCentralWidget(central_widget)
        self.show()

        # Create a QTimer for animation updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.animation_loop)
        # self.timer.start(30)  # 20 milliseconds
        

    def open_file_dialog(self):
        # This method will be called when the 'Load file' button is clicked
        options = QFileDialog.Options()
        # Uncomment the following line if you want a native file dialog.
        # options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "All Files (*);;PKL Files (*.pkl)", options=options)
        if file_name:
            # Add code here to handle the file loading
            self.load_handpose_data(file_name)
            self.load_button.setText("Loaded: " + file_name.split('/')[-1])

    def load_handpose_data(self, file_name):
        # Add code here to load the handpose data
        data = pd.read_pickle(file_name)

        if 'mphands_data' in data.columns:
            self.handpose_actual = np.stack(data['mphands_data'].tolist()).reshape(-1, 21, 3) * 10
        else:
            self.handpose_actual = None
        if 'gesture_label' in data.columns:
            self.gesture_actual = data['gesture_label'].to_numpy()
        else:
            self.gesture_actual = None

        self.eit_data = np.stack(data['eit_data'].tolist()) - np.mean(np.stack(data['eit_data'].tolist()), axis=0)


        self.timestamps = np.array([i for i in range(len(self.eit_data))])

        self.timeline.setMaximum(len(self.timestamps)-1)

        if self.gesture_actual is not None and self.handpose_actual is not None:
            self.update_plot(self.gl_widget, self.handpose_actual[0, :, 0], self.handpose_actual[0, :, 1], self.handpose_actual[0, :, 2], 0)
            self.gesture_plots[0].setData(self.timestamps[0:100], self.gesture_actual[0:100])
        elif self.gesture_actual is not None:
            self.update_plot(self.gl_widget, None, None, None, 0)
            self.gesture_plots[0].setData(self.timestamps[0:100], self.gesture_actual[0:100])
        elif self.handpose_actual is not None:
            self.update_plot(self.gl_widget, self.handpose_actual[0, :, 0], self.handpose_actual[0, :, 1], self.handpose_actual[0, :, 2], None)
            self.gesture_plots[0].setData()

        for i in range(8):
            self.eit_plots[i].setData(self.timestamps[0:100], self.eit_data[0:100, 40+i])




    def play_button_clicked(self, pressed):
        # This method will be called when the 'Play' button is clicked
        # You will need to implement the logic to play the handpose data
        if pressed:
            self.timer.start(50)
            self.playing = True
            if self.annotation_enabled and self.gesture_group.checkedId() != 12:
                self.start_timestamp = self.timestamps[self.index_value]
        else:
            self.timer.stop()
            self.playing = False
        self.play_button.setText("Play: " + str(pressed))

    def annotate_button_clicked(self, pressed):
        # This method will be called when the 'Annotate' button is clicked
        # You will need to implement the logic to annotate the handpose data
        self.annotation_enabled = pressed
        self.annotate_button.setText("Annotate: " + str(pressed))


    def timeline_value_changed(self, value):
        self.index_value = value
        if self.gesture_actual is not None and self.handpose_actual is not None:
            self.update_plot(self.gl_widget, self.handpose_actual[value, :, 0], self.handpose_actual[value, :, 1], self.handpose_actual[value, :, 2], self.gesture_actual[value])
            self.gesture_plots[0].setData(self.timestamps[value:min(100+value, len(self.timestamps)-1)], self.gesture_actual[value:min(100+value, len(self.timestamps)-1)])
        elif self.gesture_actual is not None:
            self.update_plot(self.gl_widget, None, None, None, self.gesture_actual[value])
            self.gesture_plots[0].setData(self.timestamps[value:min(100+value, len(self.timestamps)-1)], self.gesture_actual[value:min(100+value, len(self.timestamps)-1)])
        elif self.handpose_actual is not None:
            self.update_plot(self.gl_widget, self.handpose_actual[value, :, 0], self.handpose_actual[value, :, 1], self.handpose_actual[value, :, 2], None)

        for i in range(8):
            self.eit_plots[i].setData(self.timestamps[value:min(100+value, len(self.timestamps)-1)], self.eit_data[value:min(100+value, len(self.timestamps)-1), 40+i])

    # Function to update the plots with new data
    def update_plot(self, plot, x, y, z, gesture):
        plot.clear()

        if x is not None:
            # Create scatter plot
            scatter = gl.GLScatterPlotItem(pos=np.column_stack((x, y, z)), color=(0.5, 0.5, 0.5, 1.0), size=15)  # Increase size to 0.1
            plot.addItem(scatter)

            # Create lines for hand connections
            connections = [(0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
                        (0, 5), (5, 6), (6, 7), (7, 8),  # Index finger
                        (0, 9), (9, 10), (10, 11), (11, 12),  # Middle finger
                        (0, 13), (13, 14), (14, 15), (15, 16),  # Ring finger
                        (0, 17), (17, 18), (18, 19), (19, 20),  # Little finger
                        (5, 9), (9, 13), (13, 17)]  
            
            colors = [(1, 0.2, 0.2, 0.8), (0.2, 1, 0.2, 0.8), (0.2, 0.2, 1.0, 0.8),
                    (1, 0.2, 1.0, 0.8), (1, 1.0, 0.2, 0.8), (0.8, 0.8, 0.8 , 0.8)]

            for i in range(len(connections)):
                connection = connections[i]
                line_x = [x[connection[0]], x[connection[1]]]
                line_y = [y[connection[0]], y[connection[1]]]
                line_z = [z[connection[0]], z[connection[1]]]

                if 0 in connection or i > 19:
                    color = colors[5]
                else:
                    color = colors[int(np.floor(i/4))]
                line = gl.GLLinePlotItem(pos=np.column_stack((line_x, line_y, line_z)), color=color, width=10.0)
                plot.addItem(line)
            
            # # Set plot camera parameters
            # plot.opts['distance'] = 5
            # plot.opts['rotationMethod'] = 'quaternion'

            axes = gl.GLAxisItem()
            plot.addItem(axes)

            grid = gl.GLGridItem()
            plot.addItem(grid)

        if gesture is not None:
            plot.update_overlay_text("gesture", "Gesture: " + str(gesture) + " " + str(self.gesture_dictionary[gesture] if gesture in self.gesture_dictionary else None), plot.width()-300, plot.height()-150, 14)
        else:
            plot.update_overlay_text("gesture", "Gesture: None", plot.width()-300, plot.height()-150, 14)


    def animation_loop(self):
        # This method will be called by the QTimer to update the animation
        # You will need to implement the logic to update the animation
        if self.playing:

            self.index_value += 1
            if self.index_value >= len(self.timestamps):
                self.play_button.setChecked(False)
                self.playing = False
                self.timer.stop()
                self.index_value -= 1
                self.timeline.setValue(self.index_value)
                self.timeline_value_changed(self.index_value)
                return
            self.timeline.setValue(self.index_value)
            self.timeline_value_changed(self.index_value)
            if self.annotation_enabled:
                if self.index_value < len(self.labeled_data):
                    self.labeled_data[self.index_value] = None if self.gesture_group.checkedId() == 18 else self.gesture_group.checkedId()
                else:
                    self.play_button.setChecked(False)
                    self.playing = False
                    self.timer.stop()
            if self.annotation_enabled and self.gesture_group.checkedId() == 18:
                self.start_timestamp = self.timestamps[self.index_value]
            if self.annotation_enabled and self.gesture_group.checkedId() != 18 and self.timestamps[self.index_value] - self.start_timestamp > 1.5:
                self.none_button.setChecked(True)
                self.play_button_clicked(False)


    def keyPressEvent(self, event):
        # Override keyPressEvent to respond to the space bar
        if event.key() == Qt.Key_F:
            # Toggle the play button's checked state
            # self.play_button.setChecked(not self.play_button.isChecked())
            self.play_button_clicked(not self.playing)
        else:
            super().keyPressEvent(event)  # Call the parent class method to ensure default behavior


