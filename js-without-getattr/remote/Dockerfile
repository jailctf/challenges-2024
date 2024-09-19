FROM node@sha256:c4856362ed3261b2e9e0d5f3113bd9feace612884f8101ca09da553f856fd0a2 AS app
WORKDIR /app
RUN /usr/local/bin/npm install esprima

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 main.js /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
ENV JAIL_MEM=40M JAIL_PIDS=10 JAIL_ENV_NUM=5 JAIL_TIME=30 JAIL_CONNS_PER_IP=2

