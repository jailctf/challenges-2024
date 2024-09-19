FROM python@sha256:83f5f8714b6881d3e0e91023d9fe9e43aa6ad5a04e9f9a94ee180b18b021c72a AS app

FROM pwn.red/jail
COPY --from=app / /srv

COPY --chmod=755 chal.py /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt

ENV JAIL_MEM=20M
ENV JAIL_TIME=60
