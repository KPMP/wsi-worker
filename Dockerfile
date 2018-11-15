FROM ubuntu

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

# Copy over the stub runtime and SVS
COPY ./html /html
COPY data-in/LNC00044_PAS_77649.svs /wsi.svs

# Install libvips dependencies, including OpenSlide
# https://packages.debian.org/jessie/libvips-dev
RUN apt-get update
RUN apt-get install -y libopenslide-dev libvips-dev libvips

# Install node and NPM for the stub runtime
RUN apt-get install -y curl gnupg2
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get update
RUN apt-get install -y build-essential nodejs
RUN cd html && \
  npm update && \
  npm install && \
  npm install express

# Call vips to convert our SVS to deepzoom format
RUN vips dzsave /wsi.svs /html/deepzoom

# CMD ["cd html && node server.js"]

