#!/bin/bash

pip install -t lib -r requirements-gcp.txt
gcloud -q --project=$1 app deploy --version 1
