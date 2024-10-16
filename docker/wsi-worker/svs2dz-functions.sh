#!/bin/bash

# Define some constants
DID_ERROR=0
JOB_IN_DIR=/data/job/in
JOB_OUT_DIR=/data/job/out
filename=$2

print_help() {
  cat << EOL
--- Command help
Usage: svs2dz "KPMP_ID" "FILENAME_WITH_EXTENSION" "PKG_FILE_ID" "SLIDE_TYPE" ["STAIN_TYPE"]
All arguments should be enclosed in double-quotes to escape spaces.
Example: svs2dz "KPMP-Ex1" "KPMP-Ex1_TRI_1of1.svs" "b9f7c729-8370-4f8d-9753-4a36e8ae57a4" "IF" "TRI"
... The above example creates symlinks at <ENV_WSE_LINK_FROM_DIR>/files_KPMP-Ex1/KPMP-Ex1_TRI_1of1, slide type Immunofluorescence, stain type Trichrome
EOL
}

print_error() {
  echo "$*" 1>&2;
  let "DID_ERROR+=1";

  mkdir -p $JOB_OUT_DIR/svs2dz
  echo $(date) : $* >> $JOB_OUT_DIR/svs2dz/errors.txt
}

assert_no_errors() {
  if (( $? > 0 )); then
    echo $1
    print_help
    exit $?
  fi
}

validate_args() {
  if [[ -z "${ENV_LINK_SRC_DIR}" ]]; then
    print_error "!!! env variable ENV_LINK_SRC_DIR undefined"
  fi

  if [[ -z "${ENV_LINK_DST_DIR}" ]]; then
    print_error "!!! env variable ENV_LINK_DST_DIR undefined"
  fi
  
  if [[ -z $1 ]]; then
    print_error "!!! arg 1 must be KPMP ID"
  fi
  
  if [[ -z $2 ]]; then
    print_error "!!! arg 2 must be input full file name directly inside $JOB_IN_DIR"
  fi
  
  if [[ -z $3 ]]; then
    print_error "!!! arg 3 must be file ID"
  fi

  if [[ -z $4 ]]; then
    print_error "!!! arg 4 must be slide type"
  fi

  if [[ -z $5 ]]; then
    echo "... optional stain not passed; defaulting to type 'pas'"
    $5 = "pas"
  fi

  if (( DID_ERROR > 0 )); then
    print_help
    exit $DID_ERROR
  fi
}

call_vips() {
  mkdir -p "$ENV_LINK_SRC_DIR/files_$1/${filename%.*}"
  echo "--- vips dzsave $JOB_IN_DIR/$2 $ENV_LINK_SRC_DIR/files_$1/${filename%.*}"
  vips dzsave "$JOB_IN_DIR/$2" "$ENV_LINK_SRC_DIR/files_$1/${filename%.*}"
  
  # Copy a consistently-well-sized DZ file out as our thumbnail
  cp "$ENV_LINK_SRC_DIR/files_$1/${filename%.*}_files/8/0_0.jpeg" "$ENV_LINK_SRC_DIR/files_$1/tn_${filename%.*}.jpeg"
}

update_link_file() {
  # Append symlink creation command to output file
  mkdir -p $JOB_OUT_DIR/svs2dz
  
  if ! [ -f $JOB_OUT_DIR/svs2dz/link.sh ]; then
    cat <<EOT >> $JOB_OUT_DIR/svs2dz/link.sh
  #!/bin/bash
  ####
  # link.sh
  #### 
  #
  # Creates Deep Zoom asset symlinks into the knowledge environment, associating DZ files by the package file ID given when svs2dz job was run.
  # This command must be run in the folder where you want the links created.
  #
EOT
  fi
  
  cat <<EOT >> $JOB_OUT_DIR/svs2dz/link.sh
  if ! [ -L $ENV_LINK_DST_DIR/$3_files ]; then
    ln -s "$ENV_LINK_SRC_DIR/files_$1/${filename%.*}_files" "$ENV_LINK_DST_DIR/$3_files"
    ln -s "$ENV_LINK_SRC_DIR/files_$1/${filename%.*}.dzi" "$ENV_LINK_DST_DIR/$3.dzi"
    ln -s "$ENV_LINK_SRC_DIR/files_$1/tn_${filename%.*}.jpeg" "$ENV_LINK_DST_DIR/tn_$3.jpeg"
  fi
  
EOT
}

run_link_file() {
  cp $JOB_OUT_DIR/svs2dz/link.sh $ENV_LINK_DST_DIR/
  echo "--- $ENV_LINK_DST_DIR/link.sh"
  chmod +x $ENV_LINK_DST_DIR/link.sh
  $ENV_LINK_DST_DIR/link.sh
}

extract_metadata() {
  python3 /usr/sbin/extract_metadata.py "$JOB_IN_DIR/$2" "$JOB_OUT_DIR/metadata.json"
}

generate_mongo_records() {
  node /usr/sbin/generate_mongo_records.js $1 $2 $3 $4 $5 $JOB_OUT_DIR/metadata.json
}