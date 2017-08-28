# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Geodesic2shape
                                 A QGIS plugin
 Computes geodetic problems and export the geodesic's line segment of interest to a shapefile.
                             -------------------
        begin                : 2017-07-26
        copyright            : (C) 2017 by Stefano Suraci
        email                : stefanosampaio@hotmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Geodesic2shape class from file Geodesic2shape.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Geodesic2shape import Geodesic2shape
    return Geodesic2shape(iface)
