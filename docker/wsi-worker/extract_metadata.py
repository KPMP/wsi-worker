import openslide
import sys
import json
import math

def getCurrentLetter(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

def calculateGrids(metadata):
    verticalSize = 500
    horizontalSize = 500
    lineThickness = 13
    vertical = verticalSize / float(metadata['openslide']['mpp_y']);
    horizontal = horizontalSize / float(metadata['openslide']['mpp_y']);
    overlay = []
    overlayLabel = []
    # Make sure we have the necessary information for the slide before we calculate
    if ((metadata != None) and metadata['aperio'] and metadata['aperio']['OriginalHeight'] != None and metadata['aperio']['OriginalWidth'] != None):
        width = int(metadata['aperio']['OriginalWidth'])
        height = int(metadata['aperio']['OriginalHeight'])
        gridLineLengthForHeight = (math.ceil(((height + horizontal) / horizontal)) - 1) * horizontal;
        gridLineLengthForWidth = (math.ceil(((width + horizontal) / horizontal)) - 1) * horizontal;

        # determine where to put the vertical gridlines
        i = 0.0
        while (i <= (width + vertical)):
            overlay.append({
                'px': i,
                'py': 0,
                'width': lineThickness,
                'height': gridLineLengthForHeight,
                'className': 'gridline'
            })
            i += vertical

        # determine where to put the horizontal gridlines
        j = 0.0
        while (j <= (height + horizontal)):
            overlay.append({
                'px': 0,
                'py': j,
                'width': gridLineLengthForWidth,
                'height': lineThickness,
                'className': 'gridline'
            })
            j += horizontal

    currentNumber = 0
    yy = 0
    while (yy < (height)): # loop through the rows
        currentLetterCount = 1
        currentLetter = getCurrentLetter(currentLetterCount)
        i=0
        while (i < (width)): # loop through the columns
            overlayLabel.append(currentLetter + str(currentNumber))
            overlay.append({
                'id': 'labelOverlay-' + currentLetter + str(currentNumber),
                'px': 0 + (i/vertical * vertical + lineThickness),
                'py': 0 + (yy/horizontal * horizontal + lineThickness),
            })
            i+= vertical
            currentLetterCount += 1
            currentLetter = getCurrentLetter(currentLetterCount)
        yy += vertical
        currentNumber += 1
    metadata['overlay'] = overlay
    metadata['overlayLabel'] = overlayLabel



svsfile = sys.argv[1]
metadata_out = sys.argv[2]
slide = openslide.OpenSlide(svsfile)

metadata = {}
for properties in slide.properties:
    if '.' in properties:
        subJson = properties.split('.')
        mainKey = subJson[0]
        subkey = subJson[1].replace('-', '_')

        if mainKey in metadata:
            metadata[mainKey][subkey] = slide.properties[properties]
        else:
            metadata[mainKey] = {subkey: slide.properties[properties]}
            
calculateGrids(metadata)
with open(metadata_out, 'w') as metadata_file:
    metadata_file.write(json.dumps(metadata))

slide.close();


