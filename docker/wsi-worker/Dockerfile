FROM kingstonduo/wsi-worker-base

ARG imageName="wsi-worker"
ARG imageDescription="Compiles SVS images to DeepZoom and links in DPR"
ARG imageType="worker"
ARG imageOS="ubuntu"
ARG version="1.0"

LABEL version=$version
LABEL description=$imageDescription
LABEL ImageName=$imageName
LABEL ImageType=$imageType
LABEL ImageOS=$imageOS
LABEL Version=$version

COPY svs2dz /usr/sbin/svs2dz
COPY runjob /usr/sbin/runjob
COPY svs2dz-functions.sh /usr/sbin/svs2dz-functions.sh
COPY generate_mongo_records.js /usr/sbin/generate_mongo_records.js
COPY package.json /usr/sbin/package.json

ENTRYPOINT ["svs2dz"]
