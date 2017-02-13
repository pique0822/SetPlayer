from PIL import Image, ImageDraw

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


circ = Image.open("imgs/circle20.png")
im = Image.open("imgs/test.jpg")

blue_delta = 50
red_delta = 100
green_delta = 5

#darker < 1.0 < lighter

img = im.point(lambda p: p * 1.3)


rCount = 0
bCount = 0
gCount = 0

xPix = []
yPix = []

for x in range(img.width):
    for y in range(img.height):
        rgb = img.getpixel((x,y))
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]

        if red>=green+red_delta and red>=blue+red_delta:
            rCount += 1
            xPix.append(x)
            yPix.append(y)
        elif green>=red+green_delta and green>=blue+green_delta:
            gCount += 1
        elif blue>=red+blue_delta and blue>=green+blue_delta:#works well to detect the shape
            bCount += 1



"""print("red: ",rCount)
print("green: ",gCount)
print("blue: ",bCount)"""

xAvg = int(mean(xPix))
yAvg = int(mean(yPix))

print((xAvg,yAvg))

#The program goes up and down. column by column, xval by xVal

display = img.copy()
display.paste(circ,(xAvg-10,yAvg-10,xAvg+10,yAvg+10))
draw_img = ImageDraw.Draw(display)

def drawShape(xValues,yValues):
    error = 30
    minX = min(xValues)
    maxX = max(xValues)
    minY = min(yValues)
    maxY = max(yValues)

    yRange = maxY - minY+1

    #Creates a matrix that has a 1 where there is a pixel and a 0 wher there is not
    #A 2 represents a collection larger than a whole i.e. a 'cluster' of pixels
    blob = {}
    yTemp = yValues.copy()
    for x in range(len(xValues)):
        col = []
        for y in range(minY,maxY+1):
            if len(yTemp) > 0:
                if not yTemp[0] == y:
                    col.append(0)
                else:
                    col.append(1)
                    yTemp.pop(0)

        if len(col)>0:
            blob[x] = col

    #Can be used to see the blob that was made
    blob_file = open("blobs/blob.txt",'w')
    out = ""
    for x in blob.keys():
        for v in blob[x]:
            out += str(v)
        out+= "\n"

    blob_file.write(out)
    blob_file.close()

    print(minX,maxX,minY,maxY)

    if minX - error <= xValues[0] <= minX + error and minY - error <= yValues[0] <= minY + error:#Checks top left corner
        if maxX - error <= xValues[len(xValues)-1] <= maxX + error and maxY - error <= yValues[len(yValues)-1] <= maxY + error:#checks bottom right corner
            draw_img.line([(min(xPix),min(yPix)),(max(xPix),min(yPix))],fill=0,width=10)
            draw_img.line([(min(xPix),max(yPix)),(max(xPix),max(yPix))],fill=0,width=10)
            draw_img.line([(min(xPix),min(yPix)),(min(xPix),max(yPix))],fill=0,width=10)
            draw_img.line([(max(xPix),min(yPix)),(max(xPix),max(yPix))],fill=0,width=10)
            return "Square"
    else:
        return "Blob"

print(drawShape(xPix,yPix))

display.show()
