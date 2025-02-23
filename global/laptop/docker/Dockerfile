FROM debian:latest


COPY ./certs/certificate.crt /etc/ssl/certs/ca-certificates.crt

RUN apt update -y \
    && apt upgrade -y \
    && apt install irssi -y \
    && apt install wget -y \
    && apt install ca-certificates -y \
    && update-ca-certificates \
    && useradd -m wa11y && adduser wa11y sudo

USER wa11y

RUN mkdir -p /home/wa11y/.irssi \
    && wget -O /home/wa11y/.irssi/elite.theme \
    https://irssi-import.github.io/themes/elite.theme


COPY ./config/irssi.config /home/wa11y/.irssi/config

WORKDIR /home/wa11y

CMD [ "tail", "-f", "/dev/null" ]