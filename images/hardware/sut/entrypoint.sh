#!/bin/sh
# Regenerate SSH host keys (absent in a freshly built image), start the
# sockperf server pool in the background, then start sshd in the foreground.
set -e
ssh-keygen -A

######################## Start sockperf server pool ########################
# One UDP and one TCP server per port, so run_sockperf.sh can pick either
# protocol without needing two separate port ranges. Backgrounded with '&';
# sshd (started below) remains the container's foreground/PID-1 process.
mkdir -p /var/log/sockperf
i=0
while [ "$i" -lt "$SOCKPERF_NUM_SERVERS" ]; do
    port=$((SOCKPERF_BASE_PORT + i))
    sockperf server -p "$port" >"/var/log/sockperf/${port}-udp.log" 2>&1 &
    sockperf server -p "$port" --tcp >"/var/log/sockperf/${port}-tcp.log" 2>&1 &
    i=$((i + 1))
done

######################## Start netserver ########################
# One instance is enough: netserver forks a child per incoming test session, so it
# already serves many concurrent netperf clients (each pinned to its own data port
# by run_netperf.sh) without needing a per-connection server pool.
mkdir -p /var/log/netperf
netserver -D -p "$NETPERF_CONTROL_PORT" >/var/log/netperf/netserver.log 2>&1 &

exec /usr/sbin/sshd -D -e
