FROM python@sha256:4d440b214e447deddc0a94de23a3d97d28dfafdf125a8b4bb8073381510c9ee2 AS app

RUN pip install --no-cache-dir flask_limiter flask

RUN useradd ctf
COPY ./server.py /home/ctf/server.py
COPY ./flag.txt /home/ctf/flag.txt
COPY ./templates/ /home/ctf/templates/
USER ctf
WORKDIR /home/ctf
RUN export "KEY=$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 64)"

CMD ["/usr/local/bin/python3", "server.py"]
#ENTRYPOINT ["/bin/sh"]
