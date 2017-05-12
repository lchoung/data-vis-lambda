import json

# Lambda function method to run. Gets data from API call

def lambda_handler(event, context):
    row_input = event['rows']
    ROWS = stringToArray(row_input)
    h = int(event['h'])
    w = int(event['w'])
    max_iterations = int(event['max_iterations'])

    response = {}
    for yPos in ROWS:
        response[int(yPos)] = mandelbrotCalcRow(int(yPos), h, w, max_iterations)

    return json.dumps(response)

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
    
def stringToArray(input):
    return input.split(',')