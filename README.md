WSI Pipeline
------------

This repository illustrates the pipeline for generating DeepZoom images from SVS.

Run on Docker
-------------

Before starting, make sure you have configured `.env` in the `docker` folder.

1. `cd wsi-pipeline/docker/vips-worker-base`
2. `docker build .`
3. Get created image ID
4. `cd ../vips-worker`
5. Edit `Dockerfile` and set FROM to the vips-worker-base image ID
6. `docker build .`
7. Get created image ID
8. `cd ..`
9. Edit `.env` and set `ENV_WORKER_IMAGE_ID` to the vips-worker image ID
10. `docker-compose up -d`
11. `docker exec -it <created container ID> /bin/bash`
12. In the Docker shell, `/exec/svs2dz <KPMP ID> <file name> <file ID>`

An enterprising contributor could easily modify the vips-worker `Dockerfile` and `runjob` scripts to do some more intelligent logging, input parameter-handling, and maybe even file-watching in the `/data/job/in` folder.

For now, this is but a humble container showing that our DeepZoom pipeline is within reach.
