FROM python@sha256:bd55f8eed20434cc1dfc75039f766f5890995dc6adfd509cefad95835a306575 AS builder

WORKDIR /build
COPY embedder.c .
COPY Makefile .
RUN make DEBUGLVL=0

FROM pwn.red/jail

COPY --from=python@sha256:bd55f8eed20434cc1dfc75039f766f5890995dc6adfd509cefad95835a306575 / /srv

RUN mkdir /srv/app
COPY --from=builder /build/embedder /srv/app/embedder
COPY docker/entry.py /srv/app/run
COPY docker/hook.sh /jail/hook.sh
COPY flag /srv/
ENV JAIL_TMP_SIZE=65536 JAIL_MEM=20M JAIL_PIDS=10
