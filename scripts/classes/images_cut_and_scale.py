# -*- coding: utf-8 -*-
"""VAI92__S3_TrGeom.ipynb

Automatically generated by Colaboratory.
"""

# Importar numpy para dar soporte a:
# Concatenación de matrices - np.concatenate
import numpy as np
import math
# Importar el módulo cv2 de la librería opencv
import cv2
# Soporte para visualización.
import matplotlib.pyplot as plt

from PIL import Image
from PIL.Image import Resampling

"""(a.) Enlazar Google Drive y cargar imagen en variable."""

# Se debe conectar con el Drive, y luego buscar la ruta correcta para leer la imagen
inputIm = cv2.imread('../../data/kodim05.png', cv2.IMREAD_GRAYSCALE)
plotInputIm = plt.imshow(inputIm, cmap="gray")
plt.show()

"""(b.) Cambiar el tamaño de una imagen, usando cv2.resize. Cambiar tamaño = escalamiento.
Referencia:

https://docs.opencv.org/3.4/da/d6e/tutorial_py_geometric_transformations.html
"""

# Note que este enfoque es uno de los dos posibles sugeridos en la página arriba.
# En este caso el nuevo tamaño de la imagen se especifica de forma manual.

# Enfoque 1. Note que en este caso, el tamaño final es menor que el de la imagen de entrada.
# resizedIm = cv2.resize(inputIm, (100, 100), interpolation=cv2.INTER_AREA) # Prestar atención


# Enfoque 2. En este caso, la imagen final va a tener un tamaño mayor al de la imagen de entrada.
# resizedIm = cv2.resize(inputIm,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)


# Otra versión, donde primero se calculan y almacenan en variables, el alto y el ancho de la imagen.
height, width = inputIm.shape[:2]
kScalar = 2
resizedIm = cv2.resize(inputIm, (kScalar * width, kScalar * height), interpolation=cv2.INTER_CUBIC)

plotresizeIm = plt.imshow(resizedIm, cmap="gray")
plt.savefig("../../output/kodim05_scaling.png")
plt.show()

"""(c.) ¿Cómo organizar para el caso en que se requiera reducir el tamaño a un fracción, en principio un número no
entero?

El caso donde se aumenta a una parte en específico de una imagen, se conoce usualmente como zoom. Implemente un zoom
para una ROI de la imagen seleccionada a mano. Considere por ejemplo hacer zoom a las letras con el modelo de la 3ra
moto; de izquierda a derecha.
"""

height, width = inputIm.shape[:2]
kScalar = 0.1
newRowSize = math.trunc(np.around(kScalar * width))
newColSize = int(np.around(kScalar * height))
resizedIm = cv2.resize(inputIm, (newRowSize, newColSize), interpolation=cv2.INTER_AREA)

plotresizeIm = plt.imshow(resizedIm, cmap="gray")
plt.savefig("../../output/kodim05_reduced_size.png")
plt.show()

# Recorte de imagen
width = 275
height = 220
x = 65
y = 70
crop_img = inputIm[height:height + y, width:width + x]

# Ampliar imagen
height, width = crop_img.shape[:2]
kScalar = 30
resizedIm = cv2.resize(crop_img, (kScalar * width, kScalar * height), interpolation=cv2.INTER_CUBIC)

plotInputIm = plt.imshow(resizedIm, cmap="gray", interpolation='bilinear', aspect='equal')
plt.savefig("../../output/kodim05_zoom_big.png")
plt.show()

"""(e.) Traslación de una imagen. Implica un desplazamiento geométrico de las coordendas de los píxeles en una imagen.
Matemáticamente, se obtiene operando una matriz de entrada, con una matriz de transformación cuya forma es la siguiente:
![M_translation.png](data:image/png;base64,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)"""

rows, cols = inputIm.shape
Tx = 100
Ty = 50
M = np.float32([[1, 0, Tx], [0, 1, Ty]])
xyShiftedIm = cv2.warpAffine(inputIm, M, (cols, rows))

plotresizeIm = plt.imshow(xyShiftedIm, cmap="gray")
plt.savefig("../../output/kodim05_movement.png")
plt.show()

"""(f.)"""

nFilas, nCols = inputIm.shape
# cols-1 and rows-1 are the coordinate limits.

# Sintáxis: c2v.getRotationMatrix2D(center,angle,scale):
#           https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html#gafbbc470ce83812914a70abfb604f4326
M = cv2.getRotationMatrix2D(((nCols - 1) / 2.0, (nFilas - 1) / 2.0), 45, 1.0)
rotatedIm = cv2.warpAffine(inputIm, M, (nCols, nFilas))

plotresizeIm = plt.imshow(rotatedIm, cmap="gray")
plt.savefig("../../output/kodim05_rotation.png")
plt.show()

inputIm = cv2.imread('../../data/kodim05.png', cv2.IMREAD_GRAYSCALE)
plotInputIm = plt.imshow(inputIm, cmap="gray")
# Recorte de imagen
width = 275
height = 220
x = 65
y = 70
crop_img = inputIm[height:height + y, width:width + x]

# Ampliar imagen
height, width = crop_img.shape[:2]
kScalar = 1
resizedIm = cv2.resize(crop_img, (kScalar * width, kScalar * height), interpolation=cv2.INTER_CUBIC)

plotInputIm = plt.imshow(resizedIm, cmap="gray", interpolation='bilinear', aspect='equal')
plt.savefig("../../output/kodim05_zoom_small.png")
plt.show()

# inputIm[filaInicial:finalFinal, colInicial:colFinal]=ROI
# inputIm[412:512, 668:768]=ROI
# len(412:512)


im1 = Image.open('../../data/kodim05.png')

inputIm = cv2.imread('../../data/kodim05.png', cv2.IMREAD_GRAYSCALE)
crop_im2 = plt.imshow(inputIm, cmap="gray")
# Recorte de imagen
width = 275
height = 220
x = 65
y = 70
crop_img = inputIm[height:height + y, width:width + x]

# Ampliar imagen
height, width = crop_img.shape[:2]
kScalar = 30
resizedIm = cv2.resize(crop_img, (kScalar * width, kScalar * height), interpolation=cv2.INTER_CUBIC)
cv2.imwrite('../../data/logo.png', resizedIm)
im2 = Image.open('../../data/logo.png')

basewidth = 100  # set new width
wpercent = (basewidth / float(im2.size[0]))
hsize = int((float(im2.size[1]) * float(wpercent)))
im2 = im2.resize((basewidth, hsize), Resampling.LANCZOS)  # scale image

width_im1, height_im1 = im1.size
width_im2, height_im2 = im2.size

im1.paste(im2, (width_im1 - width_im2, height_im1 - height_im2), im2)  # set im2 in corner
im1.save('../../output/kodim05_with_logo.png', quality=95)

composition = cv2.imread('../../output/kodim05_with_logo.png', cv2.IMREAD_GRAYSCALE)
imgplotGG = plt.imshow(composition, cmap="gray")
plt.show()
