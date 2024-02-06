# -*- coding: utf-8 -*-
"""AllFiltersAndNoises.ipynb

Automatically generated by Colaboratory.
"""

import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
from skimage.util import random_noise
from scipy import signal
from PIL import Image


def show_menu():
    print("")
    print("Selecciona una opción:")
    print("1. Ruido sal y pimienta")
    print("2. Ruido uniforme")
    print("3. Ruido gaussiano")
    print("4. Procesamiento con filtro promedio (unsharp masking)")
    print("5. Filtro promedio")
    print("6. Filtro de mediana")
    print("7. Filtro Gaussiano")
    print("8. Filtro pasa bajos de tamaño variable y filtro promedio")
    print("9. Saturación")
    print("10. Contraste")
    print("11. Métrica de contraste")
    print("12. Gradiente con convolución 2D con filtro pasa altos")
    print("99. Salir")


def choose_opt():
    while True:
        show_menu()

        opt = input("Ingresa el número de la opción: ")

        if opt == '1':
            salt_and_pepper_noise()
        if opt == '2':
            uniform_noise()
        if opt == '3':
            gaussiano_noise()
        if opt == '4':
            unsharp_masking()
        if opt == '5':
            average_filter()
        if opt == '6':
            median_filter()
        if opt == '7':
            gaussiano_filter()
        if opt == '8':
            variable_size_low_pass_filter_and_average_filter()
        if opt == '9':
            saturation()
        if opt == '10':
            contrast()
        if opt == '11':
            contrast_metric()
        if opt == '12':
            gradient_with_2D_convolution_with_high_pass_filter()
        elif opt == '99':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")


def salt_and_pepper_noise():
    # Ruido sal y pimienta

    # Load image
    img = cv2.imread("../data/HCColor2.jpg", cv2.IMREAD_GRAYSCALE)  # gray scale
    noise_img = np.array(255 * random_noise(img, mode='s&p', amount=0.3), dtype='uint8')

    # Display images
    fig = plt.figure(dpi=300)

    fig.add_subplot(1, 2, 1)
    plt.imshow(img, cmap="gray")
    plt.title("Imagen original", fontsize=10)

    fig.add_subplot(1, 2, 2)
    plt.imshow(noise_img, cmap="gray")
    plt.title("Ruido sal y pimienta", fontsize=10)

    plt.savefig("../output/HCColor2_salt_and_pepper_noise_comparative.png")
    plt.show()


def uniform_noise():
    """# Ruido uniforme"""

    # Load image
    img_in = cv2.imread('../data/HCColor1.jpg', cv2.IMREAD_GRAYSCALE)  # gray scale
    nf, nc = img_in.shape
    img_in = img_in.astype(np.float64)

    uni_noise = np.zeros((nf, nc), dtype=np.float64)
    cv2.randu(uni_noise, 0, 255)
    uni_noise = (uni_noise * 0.5).astype(np.float64)
    un_img = cv2.add(img_in, uni_noise)

    # Display images
    fig = plt.figure(dpi=300)

    fig.add_subplot(1, 2, 1)
    plt.imshow(img_in, cmap="gray")
    plt.title("Imagen original", fontsize=10)

    fig.add_subplot(1, 2, 2)
    plt.imshow(un_img, cmap="gray")
    plt.title("Ruido uniforme", fontsize=10)

    plt.savefig("../output/HCColor1_uniform_noise_comparative.png")
    plt.show()


# Histogram
def fn_histogram(input_im):
    v_histogram = np.zeros((1, 256))
    pixel_range = range(0, 255)
    vals_pixel = np.arange(256)

    for pixel_value in pixel_range:
        v_histogram[0, pixel_value] = (input_im == pixel_value).sum()

    v_histogram = list(v_histogram.flatten())
    return v_histogram, vals_pixel


def gaussiano_noise():
    """# Ruido gaussiano"""

    # Original image
    img_in = cv2.imread('../data/HCColor1.jpg', cv2.IMREAD_GRAYSCALE)  # gray scale
    nf, nc = img_in.shape
    img_in = img_in.astype(np.float64)

    # Gaussian noise
    gauss_noise = np.zeros((nf, nc), dtype=np.float64)
    cv2.randn(gauss_noise, 50, 10)
    gauss_noise.astype(np.float64)
    cv2.add(img_in, gauss_noise)
    gauss_noiseHist = gauss_noise
    gauss_noiseHist = gauss_noiseHist.astype(np.uint8)

    hist_noise, vecPixels = fn_histogram(gauss_noiseHist)

    # Image + Gaussian noise
    noise_img = cv2.add(img_in, gauss_noise)

    # Display images
    fig = plt.figure(dpi=300)

    fig.add_subplot(2, 2, 1)
    plt.imshow(img_in, cmap="gray", vmin=0, vmax=255)
    plt.axis("off")
    plt.title("Imagen original", fontsize=10)
    plt.colorbar()

    fig.add_subplot(2, 2, 2)
    plt.imshow(gauss_noise, cmap='gray', vmin=0, vmax=255)
    plt.axis("off")
    plt.title("Ruido Gaussiano", fontsize=10)

    fig.add_subplot(2, 2, 3)
    plt.bar(vecPixels, hist_noise, align='center', width=1)
    plt.xlabel("Valor - píxel", fontsize=10)
    plt.ylabel("Frecuencia", fontsize=10)
    plt.title("Histograma ruido Gaussiano", fontsize=10)

    fig.add_subplot(2, 2, 4)
    plt.imshow(noise_img, cmap='gray', vmin=0, vmax=255)
    plt.axis("off")
    plt.title("Imagen + ruido gaussiano", fontsize=10)

    plt.savefig("../output/HCColor1_gaussiano_noise_comparative.png")
    plt.show()


def unsharp_masking():
    """# Procesamiento con filtro promedio (unsharp masking)"""

    # Load image
    img_in = cv2.imread('../data/HCColor2.jpg', cv2.IMREAD_GRAYSCALE)  # gray scale
    nf, nc = img_in.shape
    Fx = img_in.astype(np.float64)

    k_size = 21
    k = 5
    kernel = (1 / (k_size * k_size)) * np.ones([k_size, k_size])
    f_smooth = signal.convolve2d(Fx, kernel, boundary='symm', mode='same')
    Gx = Fx - f_smooth
    f_sharp = Fx + (k * Gx)
    f_sharp.astype(np.uint8)

    # Display images
    fig = plt.figure(dpi=300)

    fig.add_subplot(1, 2, 1)
    plt.imshow(Fx, cmap="gray", vmin=0, vmax=255)
    plt.title("Imagen original", fontsize=10)

    fig.add_subplot(1, 2, 2)
    plt.imshow(f_sharp, cmap="gray", vmin=0, vmax=255)
    plt.title("Con procesamiento de filtro promedio", fontsize=10)

    plt.savefig("../output/HCColor2_unsharp_masking_filter_comparative.png")
    plt.show()


def average_filter():
    """# Filtro promedio"""

    # Load image
    img_in = cv2.imread('../data/GaussianBlur.png', cv2.IMREAD_GRAYSCALE)  # gray scale
    nf, nc = img_in.shape
    img_in = img_in.astype(np.float64)

    gauss_noise = np.zeros((nf, nc), dtype=np.float64)
    cv2.randn(gauss_noise, 50, 10)
    gauss_noise.astype(np.float64)
    k_size = 21
    kernel = (1 / (k_size * k_size)) * np.ones([k_size, k_size])
    noise_img = cv2.add(img_in, gauss_noise)
    lpf_avg = signal.convolve2d(noise_img, kernel, boundary='symm', mode='same')

    # Display images
    fig = plt.figure(dpi=300)

    fig.add_subplot(1, 2, 1)
    plt.imshow(noise_img, cmap="gray", vmin=0, vmax=255)
    plt.title("Original con ruido gaussiano", fontsize=10)

    fig.add_subplot(1, 2, 2)
    plt.imshow(lpf_avg, cmap="gray", vmin=0, vmax=255)
    plt.title("Con procesamiento de filtro promedio", fontsize=10)

    plt.savefig("../output/HCColor1_average_filter_comparative.png")
    plt.show()


def median_filter():
    """# Filtro de mediana"""

    # Load image
    img = cv2.imread("../data/HCColor2.jpg", cv2.IMREAD_GRAYSCALE)  # gray scale

    k_size = 21
    noise_img = random_noise(img, mode='s&p', amount=0.3)
    noise_img = np.array(255 * noise_img, dtype='uint8')
    lpf_mediana = cv2.medianBlur(noise_img, k_size)

    # Display images
    fig = plt.figure(dpi=300)

    fig.add_subplot(1, 2, 1)
    plt.imshow(img, cmap="gray", vmin=0, vmax=255)
    plt.title("Imagen original", fontsize=10)

    fig.add_subplot(1, 2, 2)
    plt.imshow(lpf_mediana, cmap="gray", vmin=0, vmax=255)
    plt.title("Mediana", fontsize=10)

    plt.savefig("../output/HCColor2_median_filter_comparative.png")
    plt.show()


def gaussiano_filter():
    """# Filtro Gaussiano"""

    # Load image
    img_in = cv2.imread('../data/HCColor1.jpg', cv2.IMREAD_GRAYSCALE)  # gray scale
    nf, nc = img_in.shape
    img_in = img_in.astype(np.float64)

    gauss_noise = np.zeros((nf, nc), dtype=np.float64)
    cv2.randn(gauss_noise, 50, 10)
    gauss_noise.astype(np.float64)
    noise_img = cv2.add(img_in, gauss_noise)
    k_size = 21
    lpf_gaussiano = cv2.GaussianBlur(noise_img, (k_size, k_size), 0)

    # Display images
    fig = plt.figure(dpi=300)

    fig.add_subplot(1, 2, 1)
    plt.imshow(noise_img, cmap="gray", vmin=0, vmax=255)
    plt.title("Original con ruido gaussiano", fontsize=10)

    fig.add_subplot(1, 2, 2)
    plt.imshow(lpf_gaussiano, cmap="gray", vmin=0, vmax=255)
    plt.title("Con procesamiento de filtro gaussiano", fontsize=10)

    plt.savefig("../output/HCColor1_gaussiano_filter_comparative.png")
    plt.show()


def variable_size_low_pass_filter_and_average_filter():
    """# Filtro pasa bajos de tamaño variable y filtro promedio"""

    # Load image
    img_in = cv2.imread('../data/HCColor2.jpg', cv2.IMREAD_GRAYSCALE)  # gray scale

    n = 9
    kernel = (1 / (n * n)) * np.ones([n, n])
    filt_im = signal.convolve2d(img_in, kernel, boundary='symm', mode='same')

    # Display images
    fig = plt.figure(dpi=300)

    fig.add_subplot(1, 2, 1)
    plt.imshow(img_in, cmap="gray", vmin=0, vmax=255)
    plt.title("Imagen original", fontsize=10)

    fig.add_subplot(1, 2, 2)
    plt.imshow(filt_im, cmap="gray", vmin=0, vmax=255)
    plt.title("Filtro pasa bajos y filtro promedio", fontsize=10)

    plt.savefig("../output/HCColor2_variable_size_low_pass_filter_and_average_filter_comparative.png")
    plt.show()


# Contrast method
def fn_histo_contrast_enhance(input_im, out_min, out_max):
    out_im = 0 * input_im
    in_min = np.min(input_im)
    in_max = np.max(input_im)

    m = (out_max - out_min) / (in_max - in_min)
    pixel_input_val = range(in_min, in_max)
    for pixel_value in pixel_input_val:
        out_im[input_im == pixel_value] = (m * (pixel_value - in_min)) + out_min

    return out_im


def saturation():
    """# Saturación"""

    # Load image
    img_in = cv2.imread('../data/HCColor2.jpg', cv2.IMREAD_COLOR)  # color scale
    img_in = cv2.cvtColor(img_in, cv2.COLOR_BGR2RGB)

    im_contrast_enhanced = fn_histo_contrast_enhance(img_in, 0, 255)

    # Display images
    fig = plt.figure(dpi=300)

    fig.add_subplot(1, 2, 1)
    plt.imshow(img_in, cmap="gray", vmin=0, vmax=255)
    plt.title("Imagen original", fontsize=10)

    fig.add_subplot(1, 2, 2)
    plt.imshow(im_contrast_enhanced, cmap="gray", vmin=0, vmax=255)
    plt.title("Imagen con saturación", fontsize=10)

    plt.savefig("../output/HCColor2_saturation_comparative.png")
    plt.show()


# Contrast method
def fnHistoContrastEnhance(input_im, out_min, out_max, inc):
    outIm = 0 * input_im
    inMin = np.min(input_im)
    inMax = np.max(input_im)
    pixelInputVal = range(inMin, inMax)

    if inc:
        for pixel_value in pixelInputVal:
            outIm[input_im == pixel_value] = ((out_max - out_min) / (inMax - inMin)) * (pixel_value - inMin) + out_min
    else:
        for pixel_value in pixelInputVal:
            outIm[input_im == pixel_value] = ((pixel_value - inMin) / (inMax - inMin)) * (out_max - out_min) + out_min
    return outIm


def contrast():
    """# Contraste"""

    # Load image
    msg_in = cv2.imread('../data/HCColor2.jpg', cv2.IMREAD_GRAYSCALE)  # gray scale

    imContrastEnhanced = fnHistoContrastEnhance(msg_in, 0, 100, True)

    # Display images
    fig = plt.figure(dpi=300)

    fig.add_subplot(1, 2, 1)
    plt.imshow(msg_in, cmap="gray", vmin=0, vmax=255)
    plt.title("Imagen original", fontsize=10)

    fig.add_subplot(1, 2, 2)
    plt.imshow(imContrastEnhanced, cmap="gray", vmin=0, vmax=255)
    plt.title("Imagen con contraste", fontsize=10)

    plt.savefig("../output/HCColor2_contrast_comparative.png")
    plt.show()


# Contrast method
def fn_contrast(input_im, contrast_type):
    l_min = np.min(input_im)
    l_max = np.max(input_im)

    if "Luminance" == contrast_type:  # Relación entre la luminancia de un área de interés más brillante y la de un
        # área adyacente más oscura
        contrast_f = (l_max - l_min) / (l_min + 1)
    elif "Simple" == contrast_type:
        contrast_f = l_max / (l_min + 1)
    elif "Michelson" == contrast_type:  # Relación entre la dispersión y la suma de las dos luminancias. Esta
        # definición se usa típicamente en la teoría del
        contrast_f = (l_max - l_min) / (
                    l_max + l_min)  # procesamiento de señales para determinar la calidad de una señal en relación con
        # su nivel de ruido
    else:
        print("Nombre inválido para métrica de contraste.")

    return contrast_f


def contrast_metric():
    """# Métrica de contraste
    Evalúa numéricamente el contraste de imágenes etiquetadas como de alto o bajo contraste"""

    # Load image
    msg_in = cv2.imread('../data/HCColor2.jpg', cv2.IMREAD_GRAYSCALE)  # gray scale

    contrast_feat = fn_contrast(msg_in, "Michelson")
    print(contrast_feat)


def gradient_with_2D_convolution_with_high_pass_filter():
    """# Gradiente con convolución 2D con filtro pasa altos"""

    # Load image
    msg_in = cv2.imread('../data/HCColor2.jpg', cv2.IMREAD_GRAYSCALE)  # gray scale

    # high pass Filter
    Hx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    Hy = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
    # Convolution 2D
    Gx = signal.convolve2d(msg_in, Hx, boundary='symm', mode='same')
    Gy = signal.convolve2d(msg_in, Hy, boundary='symm', mode='same')
    MG = np.sqrt((Gx ** 2) + (Gy ** 2))

    # Display images
    fig = plt.figure(dpi=300)

    fig.add_subplot(1, 2, 1)
    plt.imshow(msg_in, cmap="gray")
    plt.title("Imagen original", fontsize=10)

    fig.add_subplot(1, 2, 2)
    plt.imshow(MG, cmap="gray")
    plt.title("Convolución 2D con filtro pasa altos", fontsize=10)

    plt.savefig("../output/HCColor2_gradient_with_2D_convolution_with_high_pass_filter_comparative.png")
    plt.show()


if __name__ == '__main__':
    choose_opt()


"""# Aplicación unsharp masking"""


def fn_unsharp_masking(R, k, k_size):
    kernel = (1 / (k_size * k_size)) * np.ones([k_size, k_size])
    f_smooth = signal.convolve2d(R, kernel, boundary='symm', mode='same')
    Gx = R - f_smooth
    f_sharp = R + (k * Gx)
    f_sharp.astype(np.uint8)
    return f_sharp


# Load image
msg_in = cv2.imread('../data/ratsmoothmuscle2.jpg', cv2.IMREAD_COLOR)  # color scale
msg_in = msg_in.astype(np.float64)

R = msg_in[:, :, 0]
G = msg_in[:, :, 1]
B = msg_in[:, :, 2]
k = 2
filter_size = 21
R_UM = fn_unsharp_masking(R, k, filter_size)
G_UM = fn_unsharp_masking(G, k, filter_size)
B_UM = fn_unsharp_masking(B, k, filter_size)
rgb_UM = (np.dstack((R_UM, G_UM, B_UM))).astype(np.float64)

# Display imageS
mosaic = cv2.hconcat((msg_in, rgb_UM))

"""# Histograma para imagen en escala de grises"""

# Load image
msg_in = cv2.imread('../data/HCColor2.jpg', cv2.IMREAD_GRAYSCALE)  # gray scale


# Histogram method
def fn_histogram(input_im):
    v_histogram = np.zeros((1, 256))
    pixel_range = range(0, 256)

    for pixel_value in pixel_range:
        v_histogram[0, pixel_value] = (input_im == pixel_value).sum()

    return v_histogram


histogram_EG = fn_histogram(msg_in)
histogram_EG = list(histogram_EG.flatten())
vals_pixel = np.arange(256)

# Display diagram
plt.bar(vals_pixel, histogram_EG, align='center', width=1)
plt.ylabel('Valor - píxel')
plt.ylabel('Frecuencia')
plt.title('Histograma de imagen en escala de grises')
plt.show()

"""# Histograma para imagen en escala de colores"""

# Load image
msg_in = cv2.imread('../data/HCColor2.jpg', cv2.IMREAD_COLOR)  # color scale


# Histogram method
def fn_histogram(input_im):
    v_histogram = np.zeros((1, 256))
    pixel_range = range(0, 256)

    for pixel_value in pixel_range:
        v_histogram[0, pixel_value] = (input_im == pixel_value).sum()

    return v_histogram


# Red
histogramRC = fn_histogram(msg_in[:, :, 0])
histogramRC = list(histogramRC.flatten())
# Green
histogramGC = fn_histogram(msg_in[:, :, 1])
histogramGC = list(histogramGC.flatten())
# Blue
histogramBC = fn_histogram(msg_in[:, :, 2])
histogramBC = list(histogramBC.flatten())

vals_pixel = np.arange(256)

# Display diagram
fig, axs = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
axs[0].bar(vals_pixel, histogramRC, align='center', width=1)
axs[1].bar(vals_pixel, histogramGC, align='center', width=1)
axs[2].bar(vals_pixel, histogramBC, align='center', width=1)

"""# Combinar 2 imágenes (Composición)"""

# Load images
A = cv2.imread('../data/Cameraman.png', cv2.IMREAD_GRAYSCALE)  # gray scale
B = cv2.imread('../data/Rice.png', cv2.IMREAD_GRAYSCALE)  # gray scale

A = A[0:1024, 0:1022]
k = 0.5  # Set to combine 2 images
C = (k * A) + ((1 - k) * B)

# Display image
imgplot_C = plt.imshow(C, cmap="gray")
plt.colorbar()

"""# Detección de movimiento"""

# Load images
im_A = cv2.imread('../data/sub_A.png', cv2.IMREAD_GRAYSCALE)  # gray scale
im_B = cv2.imread('../data/sub_B.png', cv2.IMREAD_GRAYSCALE)  # gray scale

remainder = im_A - im_B

# Display images
fig = plt.figure(dpi=300)

fig.add_subplot(2, 2, 1)
plt.imshow(im_A, cmap="gray")
plt.axis("off")
plt.title("Imagen A", fontsize=10)

fig.add_subplot(2, 2, 2)
plt.imshow(im_B, cmap="gray")
plt.title("Imagen B", fontsize=10)

fig.add_subplot(2, 2, 3)
plt.imshow(remainder, cmap="gray")
plt.title("Detección de movimiento", fontsize=10)

"""# Detección de movimiento con umbralización y operaciones lógicas (XOR operador)"""

# Load images
im_A = cv2.imread('../data/scr3.png', cv2.IMREAD_GRAYSCALE)  # gray scale
im_B = cv2.imread('../data/scr4.png', cv2.IMREAD_GRAYSCALE)  # gray scale

k = 0.5  # to combine 2 images
thr = 160  # umbral (0 - 255)

im_A[im_A <= thr] = 1
im_A[im_A > thr] = 0
im_B[im_B <= thr] = 1
im_B[im_B > thr] = 0

# Implements XOR operator
im_C = (k * im_A) + ((1 - k) * im_B)
im_C[im_C <= 0] = 0
im_C[im_C > 0] = 1

# Display image
fig = plt.figure(dpi=300)

fig.add_subplot(2, 2, 1)
plt.imshow(im_A, cmap="gray")
plt.axis("off")
plt.title("Imagen A", fontsize=10)

fig.add_subplot(2, 2, 2)
plt.imshow(im_B, cmap="gray")
plt.title("Imagen B", fontsize=10)

fig.add_subplot(2, 2, 3)
plt.imshow(im_C, cmap="gray")
plt.title("Detección de movimiento", fontsize=10)

"""# Composición de 2 imágenes, una imagen reducida en una esquina
Una de las imágenes, concretamente una versión reducida, estará en la esquina inferior derecha de la otra imagen
"""

# Load images
im1 = Image.open('../data/Cameraman.png')
im2 = Image.open('../data/Rice.png')

base_width = 342  # set new size in horizontal to image 2
w_percent = (base_width / float(im2.size[0]))
h_size = int((float(im2.size[1]) * float(w_percent)))
im2 = im2.resize((base_width, h_size), Image.ANTIALIAS)  # scale image

width_im1, height_im1 = im1.size
width_im2, height_im2 = im2.size

# Save image combined
im1.paste(im2, (width_im1 - width_im2, height_im1 - height_im2), im2)  # set im2 in corner right down
im1.save('../data/Cameraman_Rice.png', quality=95)

# Load image combined
composition = cv2.imread('../data/Cameraman_Rice.png', cv2.IMREAD_GRAYSCALE)  # gray scale
# Display image
img_plot_GG = plt.imshow(composition, cmap="gray")
plt.colorbar()

"""# Brillo con operaciones aritméticas suma y multiplicación (Subir brillo)"""

# Load image
img_int = cv2.imread('../data/D1.jpg', cv2.IMREAD_GRAYSCALE)  # gray scale

scalar = 64  # Set brightness level
low_brightness_im = cv2.add(img_int, scalar)
minimo = low_brightness_im.min()  # TODO

# Display images
fig = plt.figure(dpi=300)

fig.add_subplot(1, 2, 1)
plt.imshow(img_int, cmap="gray")
plt.title("Imagen original", fontsize=10)

fig.add_subplot(1, 2, 2)
plt.imshow(low_brightness_im, cmap="gray")
plt.title("Imagen con mas brillo", fontsize=10)

"""# Brillo con operaciones aritméticas remainder y división (Bajar brillo)"""

# Load image
img_int = cv2.imread('../data/Brighten.jpg', cv2.IMREAD_GRAYSCALE)  # gray scale

scalar = 150  # Set brightness level
high_brightness_im = cv2.subtract(img_int, scalar)

# Display images
fig = plt.figure(dpi=300)

fig.add_subplot(1, 2, 1)
plt.imshow(img_int, cmap="gray")
plt.title("Imagen original", fontsize=10)

fig.add_subplot(1, 2, 2)
plt.imshow(high_brightness_im, cmap="gray")
plt.title("Imagen con menos brillo", fontsize=10)

"""# Inverso de una imagen (Imágen en negativo)"""

# Load image
A = cv2.imread('../data/Cameraman.png', cv2.IMREAD_GRAYSCALE)  # gray scale

invA = np.invert(np.copy(A))

# Display images
fig = plt.figure(dpi=300)

fig.add_subplot(1, 2, 1)
plt.imshow(A, cmap="gray")
plt.title("Imagen original", fontsize=10)

fig.add_subplot(1, 2, 2)
plt.imshow(invA, cmap="gray")
plt.title("Imagen inverso", fontsize=10)

"""# Operador umbral para imágenes en escala de grises (Imágen en blanco y negro)"""

# Load image
A = cv2.imread('../data/Cameraman.png', cv2.IMREAD_GRAYSCALE)  # gray scale

thr_im = np.copy(A)
thr = 127
thr_im[A <= thr] = 0
thr_im[A > thr] = 1

# Display images
fig = plt.figure(dpi=300)

fig.add_subplot(1, 2, 1)
plt.imshow(A, cmap="gray")
plt.title("Imagen original", fontsize=10)

fig.add_subplot(1, 2, 2)
plt.imshow(thr_im, cmap="gray")
plt.title("Imagen en blanco y negro", fontsize=10)

"""# Cambiar tamaño (escalamiento) de una imagen (Subir tamaño)"""

# Load image
input_im = cv2.imread('../data/kodim05.png', cv2.IMREAD_GRAYSCALE)  # gray scale

height, width = input_im.shape[:2]
k_scalar = 2  # Duplicate X2 image size
resized_im = cv2.resize(input_im, (k_scalar * width, k_scalar * height), interpolation=cv2.INTER_CUBIC)

# Display images
fig = plt.figure(dpi=300)

fig.add_subplot(1, 2, 1)
plt.imshow(input_im, cmap="gray", vmin=0, vmax=255, interpolation='bilinear', aspect='equal')
plt.title("Imagen original", fontsize=10)

fig.add_subplot(1, 2, 2)
plt.imshow(resized_im, cmap="gray", vmin=0, vmax=255, interpolation='bilinear', aspect='equal')
plt.title("Imagen con tamaño mayor", fontsize=10)

"""# Cambiar tamaño (escalamiento) de una imagen (Bajar tamaño)"""

# Load image
input_im = cv2.imread('../data/kodim05.png', cv2.IMREAD_GRAYSCALE)  # gray scale

height, width = input_im.shape[:2]
k_scalar = 0.1  # Set to reduce image
new_row_size = math.trunc(np.around(k_scalar * width))
new_col_size = int(np.around(k_scalar * height))
resized_im = cv2.resize(input_im, (new_row_size, new_col_size), interpolation=cv2.INTER_AREA)

# Display images
fig = plt.figure(dpi=300)

fig.add_subplot(1, 2, 1)
plt.imshow(input_im, cmap="gray", vmin=0, vmax=255, interpolation='bilinear', aspect='equal')
plt.title("Imagen original", fontsize=10)

fig.add_subplot(1, 2, 2)
plt.imshow(resized_im, cmap="gray", vmin=0, vmax=255, interpolation='bilinear', aspect='equal')
plt.title("Imagen con tamaño menor", fontsize=10)

"""# Recorte de imagen"""

# Load image
input_im = cv2.imread('../data/kodim05.png', cv2.IMREAD_GRAYSCALE)  # gray scale

width = 275  # Set position initial in horizontal
height = 220  # Set position initial in vertical
x = 65  # Set pixels to length in horizontal
y = 70  # Set pixels to length in vertical

crop_img = input_im[height:height + y, width:width + x]

# Up resolution
height, width = crop_img.shape[:2]
k_scalar = 2  # Set size to up resolution to image
resized_im = cv2.resize(crop_img, (k_scalar * width, k_scalar * height), interpolation=cv2.INTER_CUBIC)

# Display images
fig = plt.figure(dpi=300)

fig.add_subplot(1, 2, 1)
plt.imshow(input_im, cmap="gray", vmin=0, vmax=255, interpolation='bilinear', aspect='equal')
plt.title("Imagen original", fontsize=10)

fig.add_subplot(1, 2, 2)
plt.imshow(resized_im, cmap="gray", vmin=0, vmax=255, interpolation='bilinear', aspect='equal')
plt.title("Recorte", fontsize=10)

"""# Desplazamiento geométrico de las coordendas de los píxeles en una imagen"""

# Load image
input_im = cv2.imread('../data/kodim05.png', cv2.IMREAD_GRAYSCALE)  # gray scale

rows, cols = input_im.shape
Tx = 100
Ty = 50
M = np.float32([[1, 0, Tx], [0, 1, Ty]])
xy_shifted_im = cv2.warpAffine(input_im, M, (cols, rows))

# Display image
plot_resize_im = plt.imshow(xy_shifted_im, cmap="gray")
plt.colorbar()

"""# Rotación de una imagen"""

# Load image
input_im = cv2.imread('../data/kodim05.png', cv2.IMREAD_GRAYSCALE)  # gray scale

n_rows, nCols = input_im.shape
M = cv2.getRotationMatrix2D(((nCols - 1) / 2.0, (n_rows - 1) / 2.0), 45, 1.0)
rotated_im = cv2.warpAffine(input_im, M, (nCols, n_rows))

# Display image
plot_resize_im = plt.imshow(rotated_im, cmap="gray")
plt.colorbar()