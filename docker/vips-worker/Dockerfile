FROM 2dbc0694e0ab

ARG imageName="vips-worker"
ARG imageDescription="Compiles SVS images to DeepZoom"
ARG imageType="base"
ARG imageOS="ubuntu"
ARG version="1.0"

LABEL version=$version
LABEL description=$imageDescription
LABEL ImageName=$imageName
LABEL ImageType=$imageType
LABEL ImageOS=$imageOS
LABEL Version=$version

# Copy over the bash script to process command input
COPY svs2dz /exec/svs2dz
COPY runjob /exec/runjob

# Run our job
CMD tail -f /dev/null

