from PyQt5.Qt import QApplication
import sys
import os

address = os.path.realpath(".")
sys.path.append(os.path.join(address, 'QT'))
sys.path.append(os.path.join(address, 'QT\\UI'))
sys.path.append(os.path.join(address, 'QT\\module'))
sys.path.append(os.path.join(address, 'QT\\UI\\UI_COLOR'))
sys.path.append(os.path.join(address, 'QT\\UI\\UI_CSS'))
sys.path.append(os.path.join(address, 'QT\\UI\\UI_MODEL'))
sys.path.append(os.path.join(address, 'QT\\UI\\UI_Function'))
sys.path.append(os.path.join(address, 'QT\\UI\\UI_Function\\yololite'))

from UI_SUM import UI
import matplotlib
import seaborn as sns

matplotlib.use('Qt5Agg')

if __name__ == "__main__":
    # QApplication.setStyle(QStyleFactory.create("windowsvista"))
    app = QApplication(sys.argv)
    ex = UI(debug=False)
    status = app.exec_()
    sys.exit(status)
