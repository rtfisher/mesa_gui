import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QComboBox, QLabel, QInputDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import mesa_reader as mr

def read_variable_names_from_file(file_path):
    with open(file_path, 'r') as file:
        # Skip the first three lines
        for _ in range(5):
            next(file)
        # Read the sixth line
        variable_names_line = next(file)
        # Split the line into variable names based on whitespace
        variable_names = variable_names_line.split()
    return variable_names

# Sample function to load your data
def load_data(logfile_path):
    # Read in all variables from the variable_names list
    # and store them in a pandas DataFrame

    # Read the variable names from the file
    logfile = logfile_path + '/LOGS/history.data'
    variable_names = read_variable_names_from_file(logfile)

# Create a MESA reader MesaData object for the history.data file
    h = mr.MesaData('LOGS/history.data')

    # Initialize an empty dictionary to store the data
    data_dict = {}

    # Iterate over each variable name in the list variable_names

    for variable_name in variable_names:
        # Retrieve the data for the current variable name using the h.data method
        data_dict[variable_name] = h.data (variable_name)

    df = pd.DataFrame(data_dict)

#    data = pd.DataFrame({
#        'Time': [1, 2, 3, 4, 5],
#        'Temperature': [3000, 3200, 3400, 3600, 3800],
#        'Luminosity': [100, 150, 200, 250, 300],
#        # Add more fields as per your LOG file
#    })
    return df

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MESAPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MESA Data Plotter')

        # Load data modification to use file_path
        file_path = '.'  # Specify the file path or directory as needed
        self.data = load_data(file_path)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        self.x_selector_label = QLabel('x axis:')
        self.x_selector = QComboBox()
        self.x_selector.addItems(self.data.columns)

        self.y_selector_label = QLabel('y axis:')
        self.y_selector = QComboBox()
        self.y_selector.addItems(self.data.columns)

# After the y_selector and before the plot_button
        self.x_axis_style_label = QLabel('x axis style:')
        self.x_axis_style = QComboBox()
        self.x_axis_style.addItems(['Linear', 'Log'])
        self.y_axis_style_label = QLabel('y axis style:')
        self.y_axis_style = QComboBox()
        self.y_axis_style.addItems(['Linear', 'Log'])

# Create plot button. Connect the button to the plot method. Display it as a light blue button.
        self.plot_button = QPushButton('Plot')
        self.plot_button.setStyleSheet("QPushButton {background-color: #0097A7; border-radius: 5px;}")
        self.plot_button.clicked.connect(self.plot)

# Create save plot button. Connect the button to the save_plot method. Display it as a light blue button.
        self.save_plot_button = QPushButton('Save Plot')
        self.save_plot_button.setStyleSheet("QPushButton {background-color: #0097A7; border-radius: 5px;}")
        self.save_plot_button.clicked.connect(self.save_plot)

        layout = QVBoxLayout()
        layout.addWidget(self.x_selector_label)
        layout.addWidget(self.x_selector)
        layout.addWidget(self.y_selector_label)
        layout.addWidget(self.y_selector)
        layout.addWidget(self.x_axis_style_label)
        layout.addWidget(self.x_axis_style)
        layout.addWidget(self.y_axis_style_label)
        layout.addWidget(self.y_axis_style)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.save_plot_button)
        layout.addWidget(self.canvas)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def plot(self):
        x_var = self.x_selector.currentText()
        y_var = self.y_selector.currentText()
        log_xaxis = self.x_axis_style.currentText() == 'Log'
        log_yaxis = self.y_axis_style.currentText() == 'Log'
        self.canvas.axes.clear()  # Clear previous plot

        # Choose plotting function based on axis style selections
        if log_xaxis and log_yaxis:
            plot_func = self.canvas.axes.loglog
        elif log_xaxis:
            plot_func = self.canvas.axes.semilogx
        elif log_yaxis:
            plot_func = self.canvas.axes.semilogy
        else:
            plot_func = self.canvas.axes.plot

        plot_func(self.data[x_var], self.data[y_var])  # Use the chosen plotting function
        self.canvas.axes.set_xlabel(x_var)
        self.canvas.axes.set_ylabel(y_var)
#    self.canvas.axes.grid(True)
        self.canvas.draw()

    def save_plot(self):
        fileName, ok = QInputDialog.getText(self, "Save Plot", "File name:", text="plot.png")
        if ok and fileName:
            self.canvas.figure.savefig(fileName)

# Initialize the application and display the main window, pass on as arguments
# any command line arguments to the application; just placeholders for now
app = QApplication(sys.argv)
window = MESAPlotter()
window.show()
sys.exit(app.exec_())

