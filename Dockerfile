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

# Install libvips dependencies, including OpenSlide
RUN apt-get update
RUN apt-get install -y wget build-essential make cmake g++ libglib2.0-dev libcairo2-dev libgdk-pixbuf2.0-dev libtiff5 libtiff5-dev openslide-tools

# Install OpenSlide from Github
RUN wget https://github.com/libvips/libvips/releases/download/v8.7.0-alpha2/vips-8.7.0.tar.gz
RUN tar -zxvf vips-8.7.0.tar.gz
RUN cd /vips-8.7.0 && ./configure
RUN cd /vips-8.7.0 && make
RUN cd /vips-8.7.0 && make install
RUN ldconfig

