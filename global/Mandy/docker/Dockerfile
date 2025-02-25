FROM debian:latest


COPY ./certs/certificate.crt /etc/ssl/certs/ca-certificates.crt

RUN apt update -y \
    && apt upgrade -y \
    && apt install python3 -y \
    && apt install python3-venv -y \
    && apt install python3-pip -y \
    && apt install ca-certificates -y \
    && update-ca-certificates \
    && groupadd -g 1000 mandy \
    && useradd mandy -u 1000 -g 1000 -m

USER mandy

WORKDIR /home/mandy
COPY --chown=mandy ./config/default.cfg /home/mandy/.sopel/default.cfg
COPY --chown=mandy ./plugins/talk.py /home/mandy/.sopel/plugins/talk.py

RUN python3 -m venv env \
    && /home/mandy/env/bin/pip install sopel

ENV PATH="/home/mandy/env/bin:$PATH"
ENTRYPOINT ["sopel", "start"]
