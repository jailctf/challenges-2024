FROM perl:5.40.0@sha256:545d7c6a7b9d2951fab2631d5179098bd5c7e69bc00ca44b0e74e61d02b81de8 AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 chal.pl /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt

ENV JAIL_MEM=20M JAIL_TIME=30 JAIL_CONNS_PER_IP=2
