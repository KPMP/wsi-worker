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

ENV TZ=America/Detroit
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install libvips dependencies, including OpenSlide
# https://packages.debian.org/jessie/libvips-dev
RUN apt-get update
RUN apt-get -y install libopenslide-dev libvips-dev libvips \
	&& apt-get -y install curl dirmngr apt-transport-https lsb-release ca-certificates \
	&& apt-get -y install nodejs npm
RUN update-alternatives --install /usr/bin/node node /usr/bin/nodejs 12

RUN apt-get -y install software-properties-common && add-apt-repository ppa:deadsnakes/ppa
RUN apt -y install python3.9 
RUN apt install -y python3-pip
RUN pip3 install openslide-python --break-system-packages
