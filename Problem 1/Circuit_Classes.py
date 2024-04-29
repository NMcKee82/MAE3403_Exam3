from PyQt5 import QtWidgets, QtGui, QtCore
from scipy.integrate import solve_ivp
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import sys

# Import your Ui_MainForm class from P1_GUI
from P1_GUI import Ui_MainForm


class circuitModel():
    def __init__(self):
        self.nodes = []
        self.resistors = []
        self.capacitors = []
        self.inductors = []
        self.voltageSources = []
        self.wires = []

    def simulate(self, L, R, C, A, f, p, t, pts):
        def rlc_circuit(t, y):
            V = A * np.sin(2 * np.pi * f * t + p)  # Sinusoidal input
            iL, iR, vC = y  # Unpack the state vector
            diLdt = (V - R * iR - vC) / L  # Inductor current derivative
            diRdt = (vC / R) - iR  # Resistor current derivative (i2)
            dvCdt = iR / C  # Capacitor voltage derivative
            return [diLdt, diRdt, dvCdt]

        # Initial conditions: iL(0) = 0, iR(0) = 0, vC(0) = 0
        y0 = [0, 0, 0]
        t_span = (0, t)
        t_eval = np.linspace(0, t, int(pts))

        sol = solve_ivp(rlc_circuit, t_span, y0, t_eval=t_eval)

        return sol.t, sol.y


class circuitView():
    def __init__(self, dw=None):
        if dw is not None:
            self.setDisplayWidgets(dw)
            self.setupImageLabel()
            self.setupPlot()

    def setDisplayWidgets(self, dw=None):
        if dw is not None:
            self.layout_VertInput, self.layout_VertMain, self.form = dw

    def setupImageLabel(self):
        self.pixMap = QtGui.QPixmap("Circuit1.png")
        self.image_label = QtWidgets.QLabel()
        self.image_label.setPixmap(self.pixMap)
        self.layout_VertInput.addWidget(self.image_label)

    def setupPlot(self):
        self.figure = Figure(figsize=(8, 8), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.toolbar = NavigationToolbar(self.canvas, self.form)
        self.layout_VertMain.addWidget(self.toolbar)
        self.layout_VertMain.addWidget(self.canvas)

    def doPlot(self, simulation_results):
        t, y = simulation_results
        self.ax.clear()
        self.ax.plot(t, y[0], label='i1 (Inductor Current)')
        self.ax.plot(t, y[1], label='i2 (Resistor Current)')
        self.ax.plot(t, y[2], label='Vc (Capacitor Voltage)')
        self.ax.set_title('RLC Circuit Transient Response')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Current (A) / Voltage (V)')
        self.ax.legend()
        self.canvas.draw()


class circuitController():
    def __init__(self, args):
        self.inputWidgets, self.displayWidgets = args
        self.line_edit_L, self.line_edit_R, self.line_edit_C, self.line_edit_A, self.line_edit_f, self.line_edit_p, self.line_edit_t, self.line_edit_pts = self.inputWidgets
        self.Model = circuitModel()
        self.View = circuitView(dw=self.displayWidgets)

    def calculate(self):
        L = float(self.line_edit_L.text())
        R = float(self.line_edit_R.text())
        C = float(self.line_edit_C.text())
        A = float(self.line_edit_A.text())
        f = float(self.line_edit_f.text())
        p = float(self.line_edit_p.text())
        t = float(self.line_edit_t.text())
        pts = float(self.line_edit_pts.text())

        simulation_results = self.Model.simulate(L, R, C, A, f, p, t, pts)
        self.View.doPlot(simulation_results)


class MainApplication(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        self.controller = circuitController(self.get_input_widgets())
        self.setup_connections()

    def get_input_widgets(self):
        inputWidgets = (
            self.ui.le_Inductance, self.ui.le_Resistance, self.ui.le_Capacitence,
            self.ui.le_Amplitude, self.ui.le_Freq, self.ui.le_Phase,
            self.ui.le_simTime, self.ui.le_simPts
        )
        displayWidgets = (self.ui.layout_VertInput, self.ui.layout_VertMain, self)
        return inputWidgets, displayWidgets

    def setup_connections(self):
        self.ui.pb_Calculate.clicked.connect(self.calculate)

    def calculate(self):
        self.controller.calculate()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainForm = MainApplication()
    mainForm.show()
    sys.exit(app.exec_())
