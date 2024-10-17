# WSI Worker

This script converts one SVS to a DZI pyramid, links the converted assets into the DPR's file structure, and updates the DPR database.

## Building the Docker Image
1. Build the base image in `docker/wsi-worker-base`
2. Tag with `kingstonduo/wsi-worker-base` (plus version) and push
3. Build the worker image in `docker/wsi-worker`
4. Tag with `kingstonduo/wsi-worker` (plus version) and push

### First Time Set-Up
To get started quickly, create a `.env` file in `wsi-worker/scripts` and then call `./run-wsi-worker.sh`.
To initialize the `.env` file, copy `wsi-worker/scripts/.env.example` and modify it to suit your environment (see ".env File" below).

### Example Run
1. Put an SVS file into the host's "SVS file drop zone" directory indicated by `ENV_JOB_IN_DIR`
2. `cd wsi-worker/scripts` to make that your working directory with your `.env` file
3. Start up your environment's docker-compose under `heavens-docker/delphinus`, otherwise the DB update will fail
4. Run the below command to convert the SVS to DZI and link it in the file system and to the DPR database

`./run-wsi-worker.sh KPMP-Ex1 KPMP-Ex1_PAS_1of1 abc123 pas`

#### Arguments
1. KPMP ID
2. SVS filename without the `.svs` extension
3. Package File ID from the Data Lake
4. Slide type. Values are 'LM', 'EM', 'IF'.
5. [Optional] stain type.  Values are 'he', 'pas', 'silver', 'tri', 'frz', 'tol' and 'cr'.  Defaults to 'pas'

#### .env File
1. `ENV_IMAGE`: defaults to `kingstonduo/wsi-worker`
2. `ENV_LINK_SRC_DIR`: container KE data directory, defaults to `/data/knowledgeEnvironment/deepZoom`
3. `ENV_LINK_DST_DIR`: container DPR data directory, defaults to `/data/deepZoomImages`
4. `ENV_LINK_SRC_DIR_HOST`: Host KE data directory, maps to `ENV_LINK_SRC_DIR`
5. `ENV_LINK_DST_DIR_HOST`: Host DPR data directory, maps to `ENV_LINK_DST_DIR`
6. `ENV_JOB_IN_DIR`: the host directory holding the source files (.jpg/.jpeg, .svs, .tif) to be handled by the job
7. `ENV_JOB_OUT_DIR`: the host directory to hold `link.sh` and `error.txt` if errors are logged

### Outputs
1. `ENV_JOB_OUT_DIR` receives byproduct files used in the job
2. `ENV_LINK_SRC_DIR` receives the DZI assets from the SVS conversion
3. `ENV_LINK_DST_DIR` gets symlinks to DZI assets stored in the `ENV_LINK_SRC_DIR`
4. `delphinus-mongodb` container gets updated participant and slide records in the "patients" collection
