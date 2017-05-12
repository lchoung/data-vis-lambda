import matplotlib.pyplot as plt
from matplotlib import colors
from functools import partial
import time
import multiprocessing

# Sequential and Parallel Algorithm for 4 core and 40 core machines.

IMG_HEIGHT = 1000
IMG_WIDTH = 1000
NUM_ITERATIONS = 500

def mandelbrotCalcRow(yPos, h, w, maxit):
    zoom_scale = -2.5
    yShift = 1.25
    xShift = 1
    y0 = yPos * (zoom_scale/float(h)) + yShift
    row = []
    for xPos in range (w):
        x0 = xPos * (zoom_scale/float(w)) + xShift
        iteration, z = 0, 0
        c = complex(x0, y0)
        while abs(z) < 2 and iteration < maxit:
            z = z**2 + c
            iteration += 1
        row.append(iteration)
    return row

def mandelbrotCalcSetSeq(h, w, maxit):
    partialCalcRow = partial(mandelbrotCalcRow, h=h, w=w, maxit = maxit)
    mandelImg = map(partialCalcRow, xrange(h))
    return mandelImg

def mandelbrotCalcSetPar(h, w, maxit):
    partialCalcRow = partial(mandelbrotCalcRow, h=h, w=w, maxit = maxit)
    pool = multiprocessing.Pool()
    mandelImg = pool.map(partialCalcRow, xrange(h))
    pool.close()
    pool.join()
    return mandelImg

norm = colors.PowerNorm(0.5)
date_string = time.strftime("%Y-%m-%d-%H:%M")

start_time_seq = time.time()
mandelImgSeq = mandelbrotCalcSetSeq(IMG_HEIGHT, IMG_WIDTH, NUM_ITERATIONS)
end_time_seq = time.time()
plt.imshow(mandelImgSeq, cmap="magma", vmin=0, vmax=IMG_HEIGHT, norm=norm)
plt.savefig('seq'+ date_string +'.png')

start_time_par = time.time()
mandelImgPar = mandelbrotCalcSetPar(IMG_HEIGHT, IMG_WIDTH, NUM_ITERATIONS)
end_time_par = time.time()
plt.imshow(mandelImgPar, cmap="magma", vmin=0, vmax=IMG_HEIGHT, norm=norm)
plt.savefig('par' + date_string +'.png')

print "size: ", IMG_HEIGHT
print "seq: ", end_time_seq - start_time_seq
print "par: ", end_time_par - start_time_par
print "speedup: ", (end_time_seq - start_time_seq) / (end_time_par - start_time_par)


