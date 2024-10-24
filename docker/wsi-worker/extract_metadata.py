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

def getWidthAndHeight(metadata):
    width = 0;
    height = 0;
    if ('aperio' in metadata and 'OriginalHeight' in metadata['aperio'] and 'OriginalWidth' in metadata['aperio']):
        width = int(metadata['aperio']['OriginalWidth']);
        height = int(metadata['aperio']['OriginalHeight']);
    else:
        width, height = slide.dimensions;
    return width, height;

def calculateGrids(metadata):
    verticalMicronSpacing = 500
    horizontaMicronSpacing = 500
    lineThickness = 13
    verticalSpacing = verticalMicronSpacing / float(metadata['openslide']['mpp_y']);
    horizontalSpacing = horizontaMicronSpacing / float(metadata['openslide']['mpp_y']);
    overlay = []
    overlayLabel = []
    # Make sure we have the necessary information for the slide before we calculate
    if metadata != None:
        imageWidth, imageHeight = getWidthAndHeight(metadata);
        
        gridLineLengthForHeight = (math.ceil(((imageHeight + horizontalSpacing) / horizontalSpacing)) - 1) * horizontalSpacing;
        gridLineLengthForWidth = (math.ceil(((imageWidth + horizontalSpacing) / horizontalSpacing)) - 1) * horizontalSpacing;

        # determine where to put the vertical gridlines
        i = 0.0
        while (i <= (imageWidth + verticalSpacing)):
            overlay.append({
                'px': i,
                'py': 0,
                'width': lineThickness,
                'height': gridLineLengthForHeight,
                'className': 'gridline'
            })
            i += verticalSpacing

        # determine where to put the horizontal gridlines
        j = 0.0
        while (j <= (imageHeight + horizontalSpacing)):
            overlay.append({
                'px': 0,
                'py': j,
                'width': gridLineLengthForWidth,
                'height': lineThickness,
                'className': 'gridline'
            })
            j += horizontalSpacing

    currentNumber = 0
    yy = 0
    while (yy < (imageHeight)): # loop through the rows
        currentLetterCount = 1
        currentLetter = getCurrentLetter(currentLetterCount)
        i=0
        while (i < (imageWidth)): # loop through the columns
            overlayLabel.append(currentLetter + str(currentNumber))
            overlay.append({
                'id': 'labelOverlay-' + currentLetter + str(currentNumber),
                'px': 0 + (i/verticalSpacing * verticalSpacing + lineThickness),
                'py': 0 + (yy/horizontalSpacing * horizontalSpacing + lineThickness),
            })
            i+= verticalSpacing
            currentLetterCount += 1
            currentLetter = getCurrentLetter(currentLetterCount)
        yy += verticalSpacing
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


