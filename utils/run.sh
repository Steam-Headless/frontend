#!/usr/bin/env bash
###
# File: run.sh
# File Created: Sunday, 17th September 2023 5:10:38 pm
# Author: Josh.5 (jsunnex@gmail.com)
# -----
# Last Modified: Saturday, 12th October 2024 11:59:26 am
# Modified By: Josh5 (jsunnex@gmail.com)
###

NAME="$(basename $0)"
REAL_NAME="$(readlink -f $0)"
UTILS_DIR="$(cd "$(dirname "$REAL_NAME")" && pwd)"
WEB_ROOT="$(cd "${UTILS_DIR}/../" && pwd)"
WEB_PORT="8083"
REMOTE_HOST="localhost"
VNC_PORT="32036"   # (VNC service port)
AUDIO_PORT="32039" # (pulseaudio stream port)
shui_pid=""
audio_proxy_pid=""

die() {
    echo "$*"
    exit 1
}

cleanup() {
    trap - TERM QUIT INT EXIT
    trap "true" CHLD # Ignore cleanup messages
    echo

    # Stop audio proxy
    if [ -n "${audio_proxy_pid}" ] && ps -p "${audio_proxy_pid}" >/dev/null; then
        echo "Terminating audio WebSockets proxy (${audio_proxy_pid})"
        kill "${audio_proxy_pid}"
        wait "${audio_proxy_pid}" 2>/dev/null
    fi

    # Stop SHUI
    if [ -n "${shui_pid}" ] && ps -p "${shui_pid}" >/dev/null; then
        echo "Terminating SHUI (${shui_pid})"
        kill "${shui_pid}"
        wait "${shui_pid}" 2>/dev/null
    fi
}

get_next_unused_port() {
    local __start_port=${1}
    local __start_port=$((__start_port + 1))
    local __netstat_report=$(netstat -atulnp 2>/dev/null)
    for __check_port in $(seq ${__start_port} 65000); do
        [[ -z $(echo "${__netstat_report}" | grep ${__check_port}) ]] && break
    done
    echo ${__check_port}
}

# Process Arguments
while [ "$*" ]; do
    param=$1
    shift
    OPTARG=$1
    case $param in
    --web-port)
        WEB_PORT="${OPTARG}"
        shift
        ;;
    --remote-host)
        REMOTE_HOST="${OPTARG}"
        shift
        ;;
    --vnc-port)
        VNC_PORT="${OPTARG}"
        shift
        ;;
    --audio-port)
        AUDIO_PORT="${OPTARG}"
        shift
        ;;
    -h | --help) usage ;;
    -*) usage "Unknown chrooter option: ${param}" ;;
    *) break ;;
    esac
done

# Sanity checks
if bash -c "exec 7<>/dev/tcp/localhost/${WEB_PORT:?}" &>/dev/null; then
    exec 7<&-
    exec 7>&-
    die "Port ${WEB_PORT:?} in use. Try --listen PORT"
else
    exec 7<&-
    exec 7>&-
fi

trap "cleanup" TERM QUIT INT EXIT

# Source venv
if [ -f "${WEB_ROOT:?}"/venv/bin/activate ]; then
    source "${WEB_ROOT:?}"/venv/bin/activate
fi

# try to find websockify (prefer local, try global, then download local)
if [[ -d ${UTILS_DIR}/websockify ]]; then
    WEBSOCKIFY=${UTILS_DIR}/websockify/run

    if [[ ! -x $WEBSOCKIFY ]]; then
        echo "The path ${UTILS_DIR}/websockify exists, but $WEBSOCKIFY either does not exist or is not executable."
        echo "If you intended to use an installed websockify package, please remove ${UTILS_DIR}/websockify."
        exit 1
    fi

    echo "Using local websockify at $WEBSOCKIFY"
else
    WEBSOCKIFY_FROMSYSTEM=$(which websockify 2>/dev/null)
    WEBSOCKIFY_FROMSNAP=${UTILS_DIR}/../usr/bin/python2-websockify
    [ -f $WEBSOCKIFY_FROMSYSTEM ] && WEBSOCKIFY=$WEBSOCKIFY_FROMSYSTEM
    [ -f $WEBSOCKIFY_FROMSNAP ] && WEBSOCKIFY=$WEBSOCKIFY_FROMSNAP

    if [ ! -f "$WEBSOCKIFY" ]; then
        echo "No installed websockify, attempting to clone websockify..."
        WEBSOCKIFY=${UTILS_DIR}/websockify/run
        git clone https://github.com/novnc/websockify ${UTILS_DIR}/websockify

        if [[ ! -e $WEBSOCKIFY ]]; then
            echo "Unable to locate ${UTILS_DIR}/websockify/run after downloading"
            exit 1
        fi

        echo "Using local websockify at $WEBSOCKIFY"
    else
        echo "Using installed websockify at $WEBSOCKIFY"
    fi
fi

#      _             _ _         ____             _        _
#     / \  _   _  __| (_) ___   / ___|  ___   ___| | _____| |_
#    / _ \| | | |/ _` | |/ _ \  \___ \ / _ \ / __| |/ / _ \ __|
#   / ___ \ |_| | (_| | | (_) |  ___) | (_) | (__|   <  __/ |_
#  /_/   \_\__,_|\__,_|_|\___/  |____/ \___/ \___|_|\_\___|\__|
#
#
# Configure random ports for VNC service, pulseaudio socket, noVNC service and audio transport websocket
# Note: Ports 32035-32248 are unallocated port ranges. We should be able to find something in here that we can use
#   REF: https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?&page=130
PORT_AUDIO_WEBSOCKET=$(get_next_unused_port 32040)
echo "Configure audio websocket port '${PORT_AUDIO_WEBSOCKET:?}'"

# Export config
cat <<EOF >"${WEB_ROOT:?}/web/config.js"
export default {
    REMOTE_HOST: "${REMOTE_HOST:?}",
    PORT_AUDIO_WEBSOCKET: "${PORT_AUDIO_WEBSOCKET:?}"
};
EOF

# Run audio proxy
echo "Starting audio socket proxy on port ${AUDIO_PORT:?}"
${WEBSOCKIFY} ${PORT_AUDIO_WEBSOCKET:?} ${REMOTE_HOST:?}:${AUDIO_PORT:?} &
audio_proxy_pid="$!"
sleep 1
if [ -z "$audio_proxy_pid" ] || ! ps -eo pid= | grep -w "$audio_proxy_pid" >/dev/null; then
    audio_proxy_pid=
    echo "Failed to start audio websocket"
    exit 1
fi
echo "Started audio websocket [PID ${audio_proxy_pid:?}]"

#   ____  _   _ _   _ ___   ____
#  / ___|| | | | | | |_ _| / ___|  ___ _ ____   _____ _ __
#  \___ \| |_| | | | || |  \___ \ / _ \ '__\ \ / / _ \ '__|
#   ___) |  _  | |_| || |   ___) |  __/ |   \ V /  __/ |
#  |____/|_| |_|\___/|___| |____/ \___|_|    \_/ \___|_|
#
#
# Run SHUI server
echo "Starting SHUI page on port ${WEB_PORT:?}"
pushd "${WEB_ROOT:?}/shui2/server" >/dev/null || exit 1
export WEB_PORT=${WEB_PORT:?}
export VNC_PORT=${VNC_PORT:?}
export SUNSHINE_PROXY_PORT=$(get_next_unused_port 32045)
node ./app.js &
shui_pid=$!
popd >/dev/null
sleep 1
if [ -z "$shui_pid" ] || ! ps -p "$shui_pid" >/dev/null; then
    shui_pid=
    echo "Failed to start SHUI server"
    exit 1
fi
echo "Started SHUI server [PID ${shui_pid:?}]"

echo -e "\n\nNavigate to this URL:\n"
echo -e "    http://$(hostname):${WEB_PORT:?}/\n"

echo
echo -e "Press Ctrl-C to exit\n\n"

monitor_processes() {
    while true; do
        sleep 1

        if ! ps -p "${shui_pid}" >/dev/null; then
            echo "SHUI process (${shui_pid}) has stopped"
            cleanup
            exit 1
        fi

        if ! ps -p "${audio_proxy_pid}" >/dev/null; then
            echo "Audio WebSocket process (${audio_proxy_pid}) has stopped"
            cleanup
            exit 1
        fi
    done
}

monitor_processes
