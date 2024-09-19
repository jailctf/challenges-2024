FROM ubuntu@sha256:25895062172a2f39ae36da530f3db244b507d7ffb1c4dd42a3a487b5b446e996 AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=444 LICENSE /srv/app/LICENSE
COPY --chmod=444 README.md /srv/app/README.md
COPY --chmod=444 flag.txt /srv/app/flag.txt
COPY --chmod=755 src/ /srv/app/src/
COPY --chmod=755 run.sh /srv/app/run
RUN mv /srv/app/flag.txt /srv/flag-$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32).txt
ENV JAIL_MEM=10M JAIL_PIDS=6 JAIL_ENV_NUM=5 JAIL_TIME=60 JAIL_CONNS_PER_IP=2
