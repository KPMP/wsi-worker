#!/bin/bash

# Define some constants
DID_ERROR=0
WSI_ORIG_FILES_DIR=/data/knowledgeEnvironment/deepZoom
JOB_IN_DIR=/data/job/in
JOB_OUT_DIR=/data/job/out

print_error() {
  echo "$*" 1>&2;
  let "DID_ERROR+=1";
}

validate_args() {
  # Verify we have all correct inputs to command
  
  if   [[ -z "${ENV_WSI_LINK_FROM_DIR}" ]]; then
    print_error "ENV_WSI_LINK_FROM_DIR undefined";
  fi
  
  if [[ -z $1 ]]; then
    print_error "arg 1 must be KPMP ID";
  fi
  
  if [[ -z $2 ]]; then
    print_error "arg 2 must be input file name (no extension) directly inside $JOB_IN_DIR";
  fi
  
  if [[ -z $3 ]]; then
    print_error "arg 3 must be file ID";
  fi
  
  if (( DID_ERROR > 0 )); then
    exit $DID_ERROR;
  fi 
}

link_files() {
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
  if ! [ -L $3_files ]; then
    ln -s $ENV_WSI_LINK_FROM_DIR/files_$1/$2_files $3_files
    ln -s $ENV_WSI_LINK_FROM_DIR/files_$1/$2.dzi $3.dzi
    ln -s $ENV_WSI_LINK_FROM_DIR/files_$1/tn_$2.jpeg tn_$3.jpeg
  fi
  
EOT
}

