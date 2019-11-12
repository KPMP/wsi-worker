WSI Pipeline
------------

This repository illustrates the pipeline for generating DeepZoom images from SVS.

Run on Docker: .env File
------------------------

Before starting, make sure you have configured `.env` in the `docker` folder.
That means setting the following:
1. `ENV_IMAGE`: the image ID of the vips-worker.  You will build this and get an image ID in the Build and Run section.
1. `ENV_WSI_ORIG_FILES_DIR`: mounted by the container, this is an absolute path on the host system where the created DeepZoom assets will be stored.
2. `ENV_JOB_IN_DIR`: mounted by the container, this is an absolute path on the host system where input SVS files will be found.
3. `ENV_JOB_OUT_DIR`: mounted by the container, this is an absolute path on the host where job-related output will be created.  Today, the only file created here is `svs2dz/link.sh`, a runnable bash script to create symlinks into the DZ files in `ENV_WSI_ORIG_FILES_DIR`.

Run on Docker: Build and Run
----------------------------

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

An enterprising contributor could easily modify the vips-worker `Dockerfile` and `runjob` scripts to do some more intelligent logging, input parameter-handling, and maybe even file-watching in the container's `/data/job/in` folder.

For now, this is but a humble container showing that our DeepZoom pipeline is within reach.
