#! /bin/bash

export HOME="/opt"
export AUGUSTUS_BIN_PATH="/opt/augustus/bin"
export AUGUSTUS_SCRIPTS_PATH="/opt/augustus/scripts"
export AUGUSTUS_CONFIG_PATH="/opt/augustus/config"

mkdir augustus

cp -rf $AUGUSTUS_CONFIG_PATH $PWD/augustus
export AUGUSTUS_CONFIG_PATH=$PWD/augustus/config

braker.raw.pl --AUGUSTUS_BIN_PATH $AUGUSTUS_BIN_PATH --AUGUSTUS_SCRIPTS_PATH $AUGUSTUS_SCRIPTS_PATH --AUGUSTUS_CONFIG_PATH $AUGUSTUS_CONFIG_PATH $*

rm -rf $PWD/augustus