WSI Pipeline
------------

This repository illustrates the pipeline for generating DeepZoom images from SVS.  Try it one of two ways: on OSX or with the provided Dockerfile.

Run on OSX
----------

1. [Install homebrew](https://brew.sh/) if you haven't installed it already.
2. `brew up`
3. `brew install vips --with-openslide`
4. `vips dzsave data/big-file.svs big-file-deepzoom`
5. Wait about an hour
6. Generated DZI and image folder will be created with `big-file-deepzoom` prefix

Run on Docker
-------------

These instructions apply to the current Dockerfile, which assumes at `docker build .` -time that a file named `data-in/LNC00044_PAS_77649.svs` exists and is copyable into the image.  You can modify the Dockerfile to copy in a different source SVS to make your testing life easier.

1. `cd wsi-pipeline`
2. `docker build .`
3. Get created image ID
4. `docker run -v 8000:8000 -it <image ID> /bin/bash`
5. `vips dzsave /data/wsi.svs /html/deepzoom`
6. Wait
7. Generated DZI and image folder will be created with `deepzoom` prefix
8. `cd html`
9. `node server.js`
10. In your host's browser, `http://localhost:8000`
11. OpenSeadragon will show your deepzoom WSI

