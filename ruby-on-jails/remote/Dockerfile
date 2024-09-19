FROM ruby:3.3.4@sha256:0bf712ba12549864ccbc3fe092c2684ed1542138727a219729052942725c1498 AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 chal.rb /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt

RUN mv /srv/app/flag.txt /srv/app/flag-$(head -c16 /dev/urandom | xxd -c32 -p).txt

ENV JAIL_MEM=30M JAIL_TIME=30 JAIL_CONNS_PER_IP=2