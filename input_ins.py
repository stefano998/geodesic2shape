import os
# Qt imports
from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'input_instructions.ui')) 

class Input_instructions(QtGui.QDialog, FORM_CLASS): 
    def __init__(self, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self) 
