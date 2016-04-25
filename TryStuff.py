# -*- coding: utf-8 -*-
"""
Simple examples demonstrating the use of GLMeshItem.

"""

## Add path to library (just for examples; you do not need this)

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('pyqtgraph example: GLMeshItem')
w.setCameraPosition(distance=40)

g = gl.GLGridItem()
g.scale(2, 2, 1)
w.addItem(g)

import numpy as np

## Example 3:
## sphere

md = gl.MeshData.sphere(rows=10, cols=20)
# colors = np.random.random(size=(md.faceCount(), 4))
# colors[:,3] = 0.3
# colors[100:] = 0.0
colors = np.ones((md.faceCount(), 4), dtype=float)
colors[::2, 0] = 0
colors[:, 1] = np.linspace(0, 1, colors.shape[0])
md.setFaceColors(colors)
m3 = gl.GLMeshItem(meshdata=md, smooth=False)  # , shader='balloon')

m3.translate(5, -5, 0)
w.addItem(m3)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
