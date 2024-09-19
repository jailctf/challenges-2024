FROM ubuntu:22.04 AS app

# install main languages + curl for crystal
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3 \
    ruby \
    perl \
    lua5.3 \
    gcc \
    g++ \
    php \
    curl

# install crystal
RUN curl -fsSL https://crystal-lang.org/install.sh | bash

# remove curl to make any possible exfils a bit more annoying
RUN apt-get remove curl -y

# build chal
COPY chal.cr chal.cr
RUN mkdir /app && \
    crystal build --no-debug --release --static --stats --progress -o /app/run chal.cr && \
    rm chal.cr && \
    chmod 711 /app/run

# clean
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# jail!!!!!
FROM pwn.red/jail
COPY --from=app / /srv

ENV JAIL_MEM=20M JAIL_TMP_SIZE=5M