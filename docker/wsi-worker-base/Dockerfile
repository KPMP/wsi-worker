FROM ubuntu

ARG imageName="wsi-worker-base"
ARG imageDescription="OpenSlide VIPS worker base image"
ARG imageType="base"
ARG imageOS="ubuntu"
ARG version="1.0"

LABEL version=$version
LABEL description=$imageDescription
LABEL ImageName=$imageName
LABEL ImageType=$imageType
LABEL ImageOS=$imageOS
LABEL Version=$versioni

ENV NODE_VERSION 13.1.0

# Install libvips dependencies, including OpenSlide
# https://packages.debian.org/jessie/libvips-dev
RUN apt-get update
RUN apt-get -y install libopenslide-dev libvips-dev libvips \
	&& apt-get -y install curl dirmngr apt-transport-https lsb-release ca-certificates \
	&& apt-get -y install nodejs npm
RUN update-alternatives --install /usr/bin/node node /usr/bin/nodejs 12