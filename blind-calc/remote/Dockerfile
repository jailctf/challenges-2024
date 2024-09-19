FROM ubuntu AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 run.sh /srv/app/run
COPY --chmod=755 blind.sh /srv/app/blind.sh
COPY --chmod=444 flag.txt /srv/app/flag.txt
ENV JAIL_TIME=90 JAIL_CONNS_PER_IP=2
