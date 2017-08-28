# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Geodesic2shapeDialog
                                 A QGIS plugin
 Computes geodetic problems and export the geodesic's line segment of interest to a shapefile.
                             -------------------
        begin                : 2017-07-26
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Stefano Suraci
        email                : stefanosampaio@hotmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Geodesic2shape_dialog_base.ui'))


class Geodesic2shapeDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(Geodesic2shapeDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
