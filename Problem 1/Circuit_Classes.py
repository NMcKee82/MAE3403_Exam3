#region imports
from X2Q2_SP24 import doPlot,simulate
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from abc import ABC, abstractmethod
#these imports are necessary for drawing a matplot lib graph on my GUI
#no simple widget for this exists in QT Designer, so I have to add the widget in code.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
#endregion

#region RLC circuit classes (MVC)
class circuitModel():
    def __init__(self):
        self.nodes=[]
        self.resistors=[]
        self.capacitors=[]
        self.inductors=[]
        self.voltageSources=[]
        self.wires=[]

class circuitView():
    def __init__(self, dw=None):
        if dw is not None:
            self.setDisplayWidgets(dw)
            self.setupImageLabel()
            self.setupPlot()

    def setDisplayWidgets(self, dw=None):
        if dw is not None:
            pass
            self.layout_VertInput, self.layout_VertMain, self.form = dw #unpack widgets appropriately = dw

    def setupImageLabel(self):
        """
        Displays picture of circuit from Circuit1.png in a label widget
        :return:
        """
        #region setup a label to display the image of the circuit
        self.pixMap = qtg.QPixmap()  # instantiate a QPixmap object from qtg (see imports)
        self.pixMap.load("Circuit1.png")
        self.image_label = qtw.QLabel()  # instantiate a QLabel object from qtw (see imports)
        self.image_label.setPixmap(self.pixMap)
        self.layout_VertInput.addWidget(self.image_label)
        #endregion

    def setupPlot(self):
        """
        Create the figure, canvas, axes and toolbar objects and place them on GUI
        :return:
        """
        self.figure = Figure(figsize=(8, 8), tight_layout=True, frameon=True, facecolor='none')
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot()
        self.toolbar=NavigationToolbar2QT(self.canvas, self.form)
        self.layout_VertMain.addWidget(self.toolbar)
        self.layout_VertMain.addWidget(self.canvas)

    def doPlot(self, args):
        self.canvas.figure.clear()
        self.ax = self.figure.add_subplot()
        doPlot(args, ax = self.ax)
        self.canvas.draw()
class circuitController():
    def __init__(self, args):
        """
        This is the class for a circuitContorller.  It has a model and view for the circuit.
        :param args: a tuple with input widgets and display widgets
        """
        self.inputWidgets, self.displayWidgets = args

        #unpack the input widgets
        self.line_edit_L, self.line_edit_R, self.line_edit_C, self.line_edit_A, self.line_edit_f, self.line_edit_p, self.line_edit_t, self.line_edit_pts = self.inputWidgets# unpack widgets appropriately =s elf.inputWidgets

        self.Model = circuitModel()
        self.View = circuitView(dw=self.displayWidgets)

    def calculate(self):
        """
        Simulates the circuit by calling from X2Q1_SP22 functions.
        Step 1:  read inputs from GUI and clear figure.
        Step 2:  call simulate from import.
        Step 3:  call doPlot from import.
        :return:
        """
        L = float(self.line_edit_L.text())  # read from line edit objects and convert to floating point number
        R = float(self.line_edit_R.text())  # read from line edit objects and convert to floating point number
        C = float(self.line_edit_C.text())  # read from line edit objects and convert to floating point number
        A = float(self.line_edit_A.text())  # read from line edit objects and convert to floating point number
        f = float(self.line_edit_f.text())  # read from line edit objects and convert to floating point number
        p = float(self.line_edit_p.text())  # read from line edit objects and convert to floating point number
        t = float(self.line_edit_t.text())  # read from line edit objects and convert to floating point number
        pts = float(self.line_edit_pts.text())  # read from line edit objects and convert to floating point number

        I = simulate(L=L, R=R, C=C, A=A, f=f, p=p, t=t, pts=pts)  # call simulate
        self.View.doPlot((R,I.t, I))

#endregion
