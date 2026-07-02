#!/bin/sh
# Regenerate SSH host keys (absent in a freshly built image), then start sshd in the foreground.
set -e
ssh-keygen -A
exec /usr/sbin/sshd -D -e
