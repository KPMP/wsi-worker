WSI Pipeline
------------

This repository illustrates the pipeline for generating DeepZoom images from SVS.

Run on OSX
----------

1. [Install homebrew](https://brew.sh/) if you haven't installed it already.
2. `brew up`
3. `brew install vips --with-openslide`
4. `vips dzsave data-in/my-huge-wsi.svs my-huge-slide`
5. Wait about an hour
6. The generated DZI and levels will be created with the prefix `my-huge-slide`

