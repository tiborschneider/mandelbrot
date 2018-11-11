import numpy as np
from PIL import Image
import itertools
from p_tqdm import p_map

minReal = -2
maxReal = 1
minImag = -1.5
maxImag = 1.5
bailout = 1500
resolution = 1500

def isInMandelbrot(c):
    i = 0
    x = 0
    # while i < bailout and np.abs(x) < 2:
    while i < bailout and (np.real(x) > -2 or
                           np.real(x) < 2 or
                           np.imag(x) > -2 or
                           np.imag(x) < 2):
        x = x*x+c
        i += 1

    if (i == bailout and np.abs(x) < 2):
        return True, i
    else:
        return False, i


def isRowInMandelbrot(re):
    imag = np.linspace(minImag, maxImag, resolution, endpoint = False)
    row = np.zeros((resolution,), dtype=bool)
    for i, im in enumerate(imag):
        row[i] = isInMandelbrot(re+1j*im)[0]
    return row

def createMandelbrotSet():
    real = np.linspace(minReal, maxReal, resolution, endpoint = False)

    result = p_map(isRowInMandelbrot, real.tolist())

    result = np.array(result, dtype=np.bool)

    return result

def fromComplexToIndex(z):
    # scale, such that minReal/minImag->0 and maxReal/maxImag->1
    x = (np.real(z)-minReal)/(maxReal-minReal)
    y = (np.imag(z)-minImag)/(maxImag-minImag)

    # get index
    ix = int(x*resolution)
    iy = int(y*resolution)

    return ix,iy


def processBuddhaRow(args):
    re = args[0]
    imag = np.linspace(minImag, maxImag, resolution, endpoint = False)
    mask = args[1]
    result = np.zeros((resolution, resolution), dtype=int)
    for im in imag[np.invert(mask)]:
        # create partial buddha
        i = 0
        c = re + 1j*im
        x = c
        while i < bailout and (np.real(x) > -2 and
                               np.real(x) < 2 and
                               np.imag(x) > -2 and
                               np.imag(x) < 2):
            #draw point
            (ix,iy) = fromComplexToIndex(x)
            if (0 <= ix < resolution) and (0 <= iy < resolution):
                result[fromComplexToIndex(x)] += 1
            x = x*x+c
            i += 1

    return result


def createBuddha(mandelbrotSet):
    real = np.linspace(minImag, maxImag, resolution)
    
    result = p_map(processBuddhaRow, list(zip(real, mandelbrotSet)))

    # sum all smaller images to one large buddha
    buddha = np.zeros(result[0].shape)
    for r in result:
        buddha = buddha + r

    # scale buddha such that it is from range 0..255
    buddha = 255 * buddha / buddha.max()
    return buddha.astype(np.uint8)

def main():

    # create mandelbrotset
    print("Create Mandelbrot Set...")
    mandelbrotSet = createMandelbrotSet()


    # create buddha
    print("Create Buddha..")
    buddha = createBuddha(mandelbrotSet)


    img = Image.fromarray(buddha)
    img.show()



if __name__ == '__main__':
    main()


    
