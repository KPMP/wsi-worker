# WSI Worker

This worker script handls SVS and DZI operations for the DPR.  This repository can be used to store further image processing workers.

## scripts/run-wsi-worker.sh

This script converts an SVS to DZI and links the converted assets into the DPR's file structure.

*TODO: Also update the database.  This worker does not touch delphinus-data yet.*

### Example Run

Once an SVS file is dropped into the directory indicated by `ENV_JOB_IN_DIR`, this command will convert the SVS to DZI and link it in the file system.

`wsi-worker/scripts/run-wsi-worker.sh KPMP-Ex1 KPMP-Ex1_PAS_1of1 abc123`

### Inputs
This script accepts 3 arguments and a `.env` file.

#### Arguments
1. KPMP ID
2. SVS filename without the `.svs` extension
3. Package File ID from the Data Lake

#### .env File
1. `ENV_IMAGE`: defaults to `kingstonduo/wsi-worker`
2. `ENV_LINK_SRC_DIR`: container KE data directory, defaults to `/data/knowledgeEnvironment/deepZoom`
3. `ENV_LINK_DST_DIR`: container DPR data directory, defaults to `/data/deepZoomImages`
4. `ENV_LINK_SRC_DIR_HOST`: Host KE data directory, maps to `ENV_LINK_SRC_DIR`
5. `ENV_LINK_DST_DIR_HOST`: Host DPR data directory, maps to `ENV_LINK_DST_DIR`
6. `ENV_JOB_IN_DIR`: the host directory holding the source SVS files to be handled by the job
7. `ENV_JOB_OUT_DIR`: the host directory to hold `link.sh` and `error.txt` if errors are logged

### Outputs
1. `ENV_JOB_OUT_DIR` receives byproduct files used in the job
2. `ENV_LINK_SRC_DIR` receives the DZI assets from the SVS conversion
2. `ENV_LINK_DST_DIR` gets symlinks to DZI assets stored in the `ENV_LINK_SRC_DIR`

### First-Time Set-Up

- `git clone https://github.com/kpmp/wsi-worker`
- `cd wsi-worker/scripts`
- `cp .env.example .env`
- Update environment configs
