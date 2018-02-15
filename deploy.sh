#!/usr/bin/env bash

set -e -x

tf_args="--var-file devel.tfvars tf"
terraform plan $tf_args
terraform apply $tf_args

