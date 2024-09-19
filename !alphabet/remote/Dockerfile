FROM python:3.12.3-bookworm as app

COPY --chmod=644 flag.txt /flag.txt
RUN mv /flag.txt "/flag-$(cat /dev/urandom | tr -dc '0-9a-f' | fold -w 24 | head -n 1).txt"

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 chal.py /srv/app/run

ENV JAIL_MEM=20M JAIL_POW=2500 JAIL_TMP_SIZE=10M JAIL_TIME=40
