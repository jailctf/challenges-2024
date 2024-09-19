#!/bin/sh

mv /srv/flag /srv/flag-$(head -c32 /dev/urandom | xxd -c64 -p)
