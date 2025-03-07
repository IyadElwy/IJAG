FROM debian:latest


COPY ./certs/certificate.crt /etc/ssl/certs/ca-certificates.crt

RUN apt update -y \
    && apt upgrade -y \
    && apt install irssi -y \
    && apt install ca-certificates -y \
    && update-ca-certificates \
    && useradd -m wa11y && adduser wa11y sudo

USER wa11y

RUN mkdir -p /home/wa11y/.irssi


COPY ./config/irssi.config /home/wa11y/.irssi/config
COPY ./config/elite.theme /home/wa11y/.irssi/elite.theme
COPY ./config/default.theme /home/wa11y/.irssi/default.theme

WORKDIR /home/wa11y

CMD [ "tail", "-f", "/dev/null" ]