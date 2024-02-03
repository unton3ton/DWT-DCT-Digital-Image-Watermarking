# conda activate iWM
# conda activate VIP

# https://github.com/diptamath/DWT-DCT-Digital-Image-Watermarking

import numpy as np
import pywt, os
from PIL import Image
from scipy.fftpack import dct, idct


def convert_image(image_name, size):
    img = Image.open(image_name).resize((size, size), 1)
    img = img.convert('L')
    img.save(image_name) 
    image_array = np.array(img.getdata(), dtype=np.cfloat).reshape((size, size))   
    return image_array

def process_coefficients(imArray, model, level):
    coeffs=pywt.wavedec2(data = imArray, wavelet = model, level = level)
    # print(f'\ncoeffs[0].__len__() from process_coefficients = {coeffs[0].__len__()}\n')
    coeffs_H=list(coeffs)   
    return coeffs_H

def apply_dct(image_array):
    size = image_array[0].__len__()
    # print(f'\nsize_apply_dct from apply_dct = {size}\n')
    all_subdct = np.empty((size, size))
    for i in range (0, size, h):
        for j in range (0, size, h):
            subpixels = image_array[i:i+h, j:j+h]
            subdct = dct(dct(subpixels.T, norm="ortho").T, norm="ortho")
            all_subdct[i:i+h, j:j+h] = subdct.real
    return all_subdct

def embed_watermark(watermark_array, orig_image):
    watermark_array_size = watermark_array[0].__len__()
    # print(f'\nwatermark_array_size from embed_watermark = {watermark_array_size}\n')
    watermark_flat = watermark_array.ravel() # watermark_flat_lenght = watermark_size x watermark_size
    ind = 0
    # print(f'\norig_image.__len__() from embed_watermark = {orig_image.__len__()}\n')
    for x in range (0, orig_image.__len__(), h):
        for y in range (0, orig_image.__len__(), h):
            if ind < watermark_flat.__len__():
                subdct = orig_image[x:x+h, y:y+h]
                subdct[k][k] = watermark_flat[ind].real
                orig_image[x:x+h, y:y+h] = subdct
                ind += 1
    # print(f'\nx = {x}; y = {y}; ind = {ind} from embed_watermark\n')
    # print(f'\nsubdct.__len__() from embed_watermark = {subdct.__len__()}')
    # print(f'\nsubdct[11].__len__() from embed_watermark  = {subdct[11].__len__()}') 
    return orig_image

def inverse_dct(all_subdct):
    size = all_subdct[0].__len__()
    # print(f'\nall_subdct[0].__len__() from inverse_dct = {all_subdct[0].__len__()}\n')
    all_subidct = np.empty((size, size))
    for i in range (0, size, h):
        for j in range (0, size, h):
            subidct = idct(idct(all_subdct[i:i+h, j:j+h].T, norm="ortho").T, norm="ortho")
            all_subidct[i:i+h, j:j+h] = subidct
    return all_subidct

def print_image_from_array(image_array, name):
    image_array_copy = image_array.clip(0, 255)
    image_array_copy = image_array_copy.real.astype("uint8")
    img = Image.fromarray(image_array_copy)
    img.save(name)

def get_watermark(dct_watermarked_coeff, watermark_size):
    subwatermarks = []
    # print(f'\ndct_watermarked_coeff.__len__() from get_watermark = {dct_watermarked_coeff.__len__()}\n')
    for x in range (0, dct_watermarked_coeff.__len__(), h):
        for y in range (0, dct_watermarked_coeff.__len__(), h):
            coeff_slice = dct_watermarked_coeff[x:x+h, y:y+h]
            subwatermarks.append(coeff_slice[k][k])
    # print(f'\nx = {x}; y = {y}; coeff_slice[k][k] from get_watermark = {coeff_slice[k][k]}\n') 
    # print(f'\nsubwatermarks.__len__() from get_watermark = {subwatermarks.__len__()}\n')
    watermark = np.array(subwatermarks).reshape(watermark_size, watermark_size)
    return watermark

def recover_watermark(image_array, model='haar', level = 1):
    coeffs_watermarked_image = process_coefficients(image_array, model, level=level)
    dct_watermarked_coeff = apply_dct(coeffs_watermarked_image[0])
    watermark_array = get_watermark(dct_watermarked_coeff, wm_size)
    watermark_array =  np.uint8(watermark_array)
    #Save result
    img = Image.fromarray(watermark_array)
    img.save('recovered_watermark.png')

def w2d(image, watermark):
    model = 'haar'
    level = 1
    image_array = convert_image(image, cover_size)
    # print(f'\nimage_array.__len__() from w2d = {image_array.__len__()}\n')
    # print(f'\nimage_array[0].__len__() from w2d = {image_array[0].__len__()}\n')
    watermark_array = convert_image(watermark, wm_size)
    # print(f'\nwatermark_array.__len__() from w2d = {watermark_array.__len__()}\n')
    coeffs_image = process_coefficients(image_array, model, level=level)
    # print(f'\ncoeffs_image.__len__() from w2d = {coeffs_image.__len__()}\n')
    # print(f'\ncoeffs_image[0].__len__() from w2d = {coeffs_image[0].__len__()}\n')
    dct_array = apply_dct(coeffs_image[0])
    # print(f'\ndct_array.__len__() from w2d = {dct_array.__len__()}\n')
    dct_array = embed_watermark(watermark_array, dct_array)
    # print(f'\ndct_array.__len__() from w2d = {dct_array.__len__()}\n')
    coeffs_image[0] = inverse_dct(dct_array)
    # print(f'\ncoeffs_image[0].__len__() from w2d = {coeffs_image[0].__len__()}\n')
    ## reconstruction
    image_array_H=pywt.waverec2(coeffs_image, model)
    print_image_from_array(image_array_H, 'image_with_watermark.jpg')
    # print(f'\nimage_array_H.__len__() from w2d = {image_array_H.__len__()}\n')

    # recover images
    recover_watermark(image_array = image_array_H, model=model, level = level)


from preprocess_image import preprocess_image
cover_size = 1280 # 1088  
image = "d.jpg" # '11.jpg'
preprocess_image(image, cover_size, 70)

from text_genetation import wmgenerator
wm_size = 39 #46 
wm_msg = "+79998\n887766"
wmgenerator(wm_size, wm_msg, 60)

watermark = 'text.png' 


from math import ceil # округление чисел в большую сторону
wm_size = ceil(cover_size / 2 / ceil(cover_size / 2 / wm_size))
h = ceil(cover_size / 2 / wm_size) # = 14, if  wm_size = 39 # шаг

k = (cover_size//2 - 1) - ((cover_size//2 - 1) // (h))*h # = 11, if h = 14 # номер коэф.внедрения
# print(f"h = {h}, k = {k}")

# # Embed
w2d(image, watermark)


# w_cover_plus_wm, h_cover_plus_wm = Image.open('image_with_watermark.jpg').size
# print(f"w_cover_plus_wm = {w_cover_plus_wm}, h_cover_plus_wm = {h_cover_plus_wm}")


# # Extract
# image_with_wm = 'image_with_watermark.jpg' 

# model = 'haar'
# level = 1
# image_array = convert_image(image_with_wm, cover_size)
# coeffs_image = process_coefficients(image_array, model, level=level)
# image_array_H=pywt.waverec2(coeffs_image, model)
# recover_watermark(image_array = image_array_H, model=model, level = level)