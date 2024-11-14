#!/usr/bin/env bash
###
# File: run-dev.sh
# Project: frontend
# File Created: Thursday, 14th November 2024 4:01:37 pm
# Author: Josh5 (jsunnex@gmail.com)
# -----
# Last Modified: Thursday, 14th November 2024 4:04:13 pm
# Modified By: Josh5 (jsunnex@gmail.com)
###

project_root=$(cd $(dirname $BASH_SOURCE[0])/../ && pwd)
cd ${project_root:?}

if [ ! -d ./venv ]; then
    python3 -m venv venv
    source ./venv/bin/activate
    python3 -m pip install -r ./requirements.txt
fi

# Run a dev instance on a different port to the one already running in the SH container
exec ./utils/run.sh --web-port 3000
