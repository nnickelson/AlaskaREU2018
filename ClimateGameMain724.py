# RK Estimator method for CO2 emissions and costs
# Estimator based on method by Dr. Vladimir Alexeev
# GUI by Nathan Nickelson

# Main function call file
# Set this file


import sys
import pyqtgraph as pg
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph.Qt import *
from pyqtgraph import *
import ClimateGameGUI724 as CGT


# Main call function and initialization of the main window that graphical components in it
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = CGT.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
