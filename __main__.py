import resources
import sys
from const import Const
import ui
from PyQt5.Qt import QApplication


resources.qInitResources()
app = QApplication(sys.argv)
app.setStyleSheet(Const.QSS)
root = ui.RootWindows()
root.show()
sys.exit(app.exec())