FROM debian:latest

RUN apt update -y \
    && apt upgrade -y \
    && apt install ngircd -y

COPY ./conf/ngircd.conf /etc/ngircd/ngircd.conf
COPY ./conf/ngircd.motd /etc/ngircd/ngircd.motd

COPY ./certs/certificate.crt /etc/ssl/certs/server.crt
COPY ./certs/private.key /etc/ssl/private/server.key

ENTRYPOINT ["ngircd", "-n", "-f", "/etc/ngircd/ngircd.conf"]
