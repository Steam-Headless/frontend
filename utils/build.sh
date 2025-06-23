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

# Build shui-vue
pushd "${project_root:?}/shui2/shui-vue" &>/dev/null || {
    print_error "Failed to push directory to '${project_root:?}/shui2/shui-vue'"
    exit 1
}
npm ci
npm run build
popd &>/dev/null || {
    print_error "Failed to pop directory out of '${project_root:?}/shui2/shui-vue'"
    exit 1
}

# Build shui server
pushd "${project_root:?}/shui2/server" &>/dev/null || {
    print_error "Failed to push directory to '${project_root:?}/shui2/server'"
    exit 1
}
npm ci
popd &>/dev/null || {
    print_error "Failed to pop directory out of '${project_root:?}/shui2/server'"
    exit 1
}
