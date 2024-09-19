FROM perl:latest AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 jail.pl /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
ENV JAIL_MEM=20M JAIL_ENV_NUM=5 JAIL_TIME=35 JAIL_CONNS_PER_IP=2
