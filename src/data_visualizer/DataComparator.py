import sys
from PyQt5.QtWidgets import QApplication



sys.path.append('../../')
from src.data_visualizer.DataComparatorVisualizer import MainWindow


# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Install the event filter for the application
    ex = MainWindow()

    style = 'dark'
    if style == 'dark':
        app.setStyleSheet("""
        QWidget { 
            background-color: #0B0B0B; 
        }
        QPushButton {
            color: white;
            background-color: gray;
            border: 1px solid white;
            border-radius: 10px;   /* rounded corners */
            padding: 30px;
            font: 20px "Helvetica";
        }
        QPushButton:hover {
            background-color: darkgray;
        }
        QPushButton:checked {
            background-color: black;
        }
        QPushButton:pressed {
            background-color: black;
        }

        QRadioButton {
            color: white;
            background-color: gray;
            border: 1px solid white;
            border-radius: 10px;   /* rounded corners */
            padding: 30px;
            font: 20px "Helvetica";
        }
        QRadioButton:hover {
            background-color: darkgray;
        }
        QRadioButton:checked {
            background-color: black;
        }
        QRadioButton:pressed {
            background-color: black;
        }

        QLabel {
            color: white;
        }

        """)
    else:
        app.setStyleSheet("""
        QWidget { 
            background-color: #FBFBFB; 
        }
        QPushButton {
            color: black;
            background-color: lightgray;
            border: 1px solid black;
            border-radius: 10px;   /* rounded corners */
            padding: 5px;
            font: 14px "Helvetica";
        }
        QPushButton:hover {
            background-color: darkgray;
        }
        QPushButton:checked {
            background-color: red;
        }
        QPushButton:pressed {
            background-color: darkred;
        }

        QRadioButton {
            color: black;
            background-color: lightgray;
            border: 1px solid black;
            border-radius: 10px;   /* rounded corners */
            padding: 5px;
            font: 14px "Helvetica";
        }
        QRadioButton:hover {
            background-color: darkgray;
        }
        QRadioButton:checked {
            background-color: red;
        }
        QRadioButton:pressed {
            background-color: darkred;
        }

        QLabel {
            color: black;
        }
        """)


    sys.exit(app.exec_())
