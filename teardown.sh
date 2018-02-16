#!/usr/bin/env bash

set -e -x

tf_args="--var-file devel.tfvars tf"

terraform destroy $tf_args

