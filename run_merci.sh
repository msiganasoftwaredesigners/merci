#!/bin/bash
set -o allexport
source .env.msigana
set +o allexport
docker-compose up -d
