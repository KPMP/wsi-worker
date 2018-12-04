FROM ubuntu

ARG imageName="vips-worker-base"
ARG imageDescription="OpenSlide VIPS worker base image"
ARG imageType="base"
ARG imageOS="ubuntu"
ARG version="1.0"

LABEL version=$version
LABEL description=$imageDescription
LABEL ImageName=$imageName
LABEL ImageType=$imageType
LABEL ImageOS=$imageOS
LABEL Version=$version

# Install libvips dependencies, including OpenSlide
# https://packages.debian.org/jessie/libvips-dev
RUN apt-get update
RUN apt-get install -y libopenslide-dev libvips-dev libvips

