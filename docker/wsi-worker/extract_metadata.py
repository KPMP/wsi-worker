import openslide
import sys
import json

print("\n ".join(sys.argv))

svsfile = sys.argv[1]
metadata_out = sys.argv[2]
slide = openslide.OpenSlide(svsfile)


metadata = {}
for properties in slide.properties:
    if '.' in properties:
        subJson = properties.split('.')
        mainKey = subJson[0]
        subkey = subJson[1]
        if mainKey in metadata:
            metadata[mainKey][subkey] = slide.properties[properties]
        else:
            metadata[mainKey] = {subkey: slide.properties[properties]}

print('metadata_out', metadata_out)
with open(metadata_out, 'w') as metadata_file:
    metadata_file.write(json.dumps(metadata))

slide.close()
