FROM ruby:latest AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 chal.rb /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
ENV JAIL_MEM=10M JAIL_ENV_NUM=5 JAIL_TIME=50 JAIL_CONNS_PER_IP=2
