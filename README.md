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

1. `cd wsi-pipeline`
2. `docker build .`
3. Get created image ID
4. `docker run -it <image ID> /bin/bash -v /data:/data`
5. `vips dzsave /data/big-file.svs /data/big-file-deepzoom`
6. Wait
7. Generated DZI and image folder will be created with `big-file-deepzoom` prefix
