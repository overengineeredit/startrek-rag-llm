#!/usr/bin/env bash
#   Use this script to test if a given TCP host/port are available

# The MIT License (MIT)
#
# Copyright (c) 2016-2021 vishnubob
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

set -e

TIMEOUT=15
QUIET=0
HOST=""
PORT=""

print_usage() {
    echo "Usage: $0 host:port [-t timeout] [--quiet] -- command args"
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -t|--timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        --quiet)
            QUIET=1
            shift
            ;;
        --)
            shift
            break
            ;;
        *)
            if [[ -z "$HOST" ]]; then
                HOSTPORT="$1"
                HOST="${HOSTPORT%%:*}"
                PORT="${HOSTPORT##*:}"
                shift
            else
                break
            fi
            ;;
    esac
done

if [[ -z "$HOST" || -z "$PORT" ]]; then
    print_usage
    exit 1
fi

if [[ $QUIET -eq 0 ]]; then
    echo "Waiting for $HOST:$PORT for $TIMEOUT seconds..."
fi

for ((i=0;i<TIMEOUT;i++)); do
    if nc -z "$HOST" "$PORT"; then
        if [[ $QUIET -eq 0 ]]; then
            echo "$HOST:$PORT is available!"
        fi
        exec "$@"
        exit 0
    fi
    sleep 1
done

if [[ $QUIET -eq 0 ]]; then
    echo "Timeout occurred after waiting $TIMEOUT seconds for $HOST:$PORT"
fi
exit 1 