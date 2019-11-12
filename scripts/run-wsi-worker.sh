#!/bin/bash
set -a
. ./.env
set +a

mkdir -p ${ENV_LINK_SRC_DIR_HOST}
mkdir -p ${ENV_LINK_DST_DIR_HOST}

# arg $1 must be KPMP ID
# arg $2 must be input file name (no extension) directly inside $JOB_IN_DIR
# arg $3 must be file ID

docker run \
  --env-file .env \
  -v ${ENV_LINK_SRC_DIR_HOST}:${ENV_LINK_SRC_DIR} \
  -v ${ENV_LINK_DST_DIR_HOST}:${ENV_LINK_DST_DIR} \
  -v ${ENV_JOB_IN_DIR}:/data/job/in \
  -v ${ENV_JOB_OUT_DIR}:/data/job/out \
  ${ENV_IMAGE} $1 $2 $3
