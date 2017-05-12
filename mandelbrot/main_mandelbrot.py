import json
import matplotlib.pyplot as plt
from matplotlib import colors
import grequests
import time

# Client code for calling Lambda functions

IMG_HEIGHT = 1000
IMG_WIDTH = 1000
NUM_ITERATIONS = 500

plot = [0 for i in xrange(IMG_HEIGHT)] # image to show mandelbrot
fill = [1 for i in xrange(IMG_WIDTH)]

def getUrls(i):
    rows = getRows(i, IMG_HEIGHT)
    return 'https://5crg7fo9x7.execute-api.us-west-2.amazonaws.com/prod/?h=' + str(IMG_HEIGHT) + '&w=' + str(IMG_WIDTH) + '&max_iterations=' + str(NUM_ITERATIONS) + '&rows=' + rows

def mandelbrot(h, w, max_iterations):
    reqs = [grequests.post(url) for url in urls]
    return grequests.map(reqs)

def getRows(i, h):
    rows = ""
    row = i
    while row < h:
        rows += str(row) + ","
        row+=NUM_LAMBDAS

    return rows[:-1]

def filterResponses():
    for resp in responses:
        if resp != None:
            content = resp.content
            if 'stackTrace' not in content:
                d = json.loads(json.loads(content))
                for key, val in d.iteritems():
                    plot[int(key)] = val


NUM_LAMBDAS = min(IMG_HEIGHT / 10, 200)
#start timer
start_time = time.time()

urls = [getUrls(i) for i in xrange(NUM_LAMBDAS)]
mandel_start = time.time()
responses = mandelbrot(IMG_HEIGHT, IMG_WIDTH, NUM_ITERATIONS)
mandel_end = time.time()
filterResponses()

# end timer
end_time = time.time()

print "num lambdas: ", NUM_LAMBDAS
norm = colors.PowerNorm(0.5)
plt.imshow(plot, cmap="magma", vmin=0, vmax=IMG_HEIGHT, norm=norm)
plt.savefig('lambda.png')
print "size: ", IMG_HEIGHT
print "num lambdas: ", NUM_LAMBDAS
print 'totaltime: ', end_time - start_time
print 'mandeltime: ', mandel_end - mandel_start 
