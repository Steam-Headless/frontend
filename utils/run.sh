#!/usr/bin/env bash
###
# File: run.sh
# File Created: Sunday, 17th September 2023 5:10:38 pm
# Author: Josh.5 (jsunnex@gmail.com)
# -----
# Last Modified: Monday, 18th September 2023 12:18:08 am
# Modified By: Josh.5 (jsunnex@gmail.com)
###

NAME="$(basename $0)"
REAL_NAME="$(readlink -f $0)"
HERE="$(cd "$(dirname "$REAL_NAME")" && pwd)"
WEB_PORT="8083"
WEB_ROOT=${HERE}/../
REMOTE_HOST="localhost"
VNC_PORT="32036"        # (VNC service port)
AUDIO_PORT="32039"      # (pulseaudio stream port)
main_proxy_pid=""
audio_proxy_pid=""

# TODO: Remove this override after initial development
REMOTE_HOST="192.168.1.200"

die() {
    echo "$*"
    exit 1
}

cleanup() {
    trap - TERM QUIT INT EXIT
    trap "true" CHLD   # Ignore cleanup messages
    echo
    # Stop main proxy
    if [ -n "${main_proxy_pid}" ]; then
        echo "Terminating main WebSockets proxy (${main_proxy_pid})"
        kill ${main_proxy_pid}
    fi
    # Stop audio proxy
    if [ -n "${audio_proxy_pid}" ]; then
        echo "Terminating audio WebSockets proxy (${audio_proxy_pid})"
        kill ${audio_proxy_pid}
    fi
}

get_next_unused_port() {
    local __start_port=${1}
    local __start_port=$((__start_port+1))
    local __netstat_report=$(netstat -atulnp 2> /dev/null)
    for __check_port in $(seq ${__start_port} 65000); do
        [[ -z $(echo "${__netstat_report}" | grep ${__check_port}) ]] && break;
    done
    echo ${__check_port}
}

# Process Arguments
while [ "$*" ]; do
    param=$1; shift; OPTARG=$1
    case $param in
    --listen)       WEB_PORT="${OPTARG}"; shift         ;;
    --server)       REMOTE_HOST="${OPTARG}"; shift      ;;
    --vnc-port)     VNC_PORT="${OPTARG}"; shift         ;;
    --audio-port)   AUDIO_PORT="${OPTARG}"; shift       ;;
    -h|--help) usage                              ;;
    -*) usage "Unknown chrooter option: ${param}" ;;
    *) break                                      ;;
    esac
done

# Sanity checks
if bash -c "exec 7<>/dev/tcp/localhost/${WEB_PORT:?}" &> /dev/null; then
    exec 7<&-
    exec 7>&-
    die "Port ${WEB_PORT:?} in use. Try --listen PORT"
else
    exec 7<&-
    exec 7>&-
fi

trap "cleanup" TERM QUIT INT EXIT

# try to find websockify (prefer local, try global, then download local)
if [[ -d ${HERE}/websockify ]]; then
    WEBSOCKIFY=${HERE}/websockify/run

    if [[ ! -x $WEBSOCKIFY ]]; then
        echo "The path ${HERE}/websockify exists, but $WEBSOCKIFY either does not exist or is not executable."
        echo "If you intended to use an installed websockify package, please remove ${HERE}/websockify."
        exit 1
    fi

    echo "Using local websockify at $WEBSOCKIFY"
else
    WEBSOCKIFY_FROMSYSTEM=$(which websockify 2>/dev/null)
    WEBSOCKIFY_FROMSNAP=${HERE}/../usr/bin/python2-websockify
    [ -f $WEBSOCKIFY_FROMSYSTEM ] && WEBSOCKIFY=$WEBSOCKIFY_FROMSYSTEM
    [ -f $WEBSOCKIFY_FROMSNAP ] && WEBSOCKIFY=$WEBSOCKIFY_FROMSNAP

    if [ ! -f "$WEBSOCKIFY" ]; then
        echo "No installed websockify, attempting to clone websockify..."
        WEBSOCKIFY=${HERE}/websockify/run
        git clone https://github.com/novnc/websockify ${HERE}/websockify

        if [[ ! -e $WEBSOCKIFY ]]; then
            echo "Unable to locate ${HERE}/websockify/run after downloading"
            exit 1
        fi

        echo "Using local websockify at $WEBSOCKIFY"
    else
        echo "Using installed websockify at $WEBSOCKIFY"
    fi
fi

# Configure random ports for VNC service, pulseaudio socket, noVNC service and audio transport websocket
# Note: Ports 32035-32248 are unallocated port ranges. We should be able to find something in here that we can use
#   REF: https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?&page=130
PORT_AUDIO_WEBSOCKET=$(get_next_unused_port 32040)
echo "Configure audio websocket port '${PORT_AUDIO_WEBSOCKET:?}'"

# Export config
cat << EOF > "${WEB_ROOT:?}/web/config.json"
{
    "REMOTE_HOST": "${REMOTE_HOST:?}",
    "PORT_AUDIO_WEBSOCKET": "${PORT_AUDIO_WEBSOCKET:?}"
}
EOF

# Create redirect
cat << EOF > "${WEB_ROOT:?}/index.html"
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0;url=./web/">
</head>
<body>
    <p>If you are not redirected, <a href="./web/">click here</a>.</p>
</body>
</html>
EOF

# Run main server
echo "Starting webserver and WebSockets proxy on port ${WEB_PORT:?}"
${WEBSOCKIFY} --web ${WEB_ROOT:?} ${WEB_PORT:?} ${REMOTE_HOST:?}:${VNC_PORT:?} &
main_proxy_pid="$!"
sleep 1
if [ -z "$main_proxy_pid" ] || ! ps -eo pid= | grep -w "$main_proxy_pid" > /dev/null; then
    main_proxy_pid=
    echo "Failed to start WebSockets proxy"
    exit 1
fi

# Run audio proxy
echo "Starting audio socket proxy on port ${WEB_PORT:?}"
${WEBSOCKIFY} ${PORT_AUDIO_WEBSOCKET:?} ${REMOTE_HOST:?}:${AUDIO_PORT:?} &
audio_proxy_pid="$!"
sleep 1
if [ -z "$audio_proxy_pid" ] || ! ps -eo pid= | grep -w "$audio_proxy_pid" > /dev/null; then
    audio_proxy_pid=
    echo "Failed to start WebSockets proxy"
    exit 1
fi

echo -e "\n\nNavigate to this URL:\n"
echo -e "    http://$(hostname):${WEB_PORT:?}/web/vnc.html?host=$(hostname)&port=${WEB_PORT:?}\n"

echo -e "Press Ctrl-C to exit\n\n"

wait ${main_proxy_pid}
wait ${audio_proxy_pid}
