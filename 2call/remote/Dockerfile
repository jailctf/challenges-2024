FROM node@sha256:c4856362ed3261b2e9e0d5f3113bd9feace612884f8101ca09da553f856fd0a2 AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 chal.js /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
RUN mv /srv/app/flag.txt /srv/flag-$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32).txt
ENV JAIL_MEM=40M JAIL_PIDS=10 JAIL_ENV_NUM=5 JAIL_TIME=30 JAIL_CONNS_PER_IP=2
