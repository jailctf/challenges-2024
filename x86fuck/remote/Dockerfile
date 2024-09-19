FROM python@sha256:4d440b214e447deddc0a94de23a3d97d28dfafdf125a8b4bb8073381510c9ee2 AS app
RUN pip install --no-cache-dir unicorn

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 chal.py /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
ENV JAIL_MEM=40M JAIL_PIDS=7 JAIL_ENV_NUM=5 JAIL_TIME=15 JAIL_CONNS_PER_IP=2
