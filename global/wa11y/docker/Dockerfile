FROM debian:latest


COPY ./certs/certificate.crt /etc/ssl/certs/ca-certificates.crt

RUN apt update -y \
    && apt upgrade -y \
    && apt install irssi -y \
    && apt install python3 -y \
    && apt install python3-venv -y \
    && apt install python3-pip -y \
    && apt install ca-certificates -y \
    && update-ca-certificates \
    && useradd -m wa11y && adduser wa11y sudo

COPY --chmod=755 ./notes/notes.sh /bin/notes
RUN mkdir /scripts
RUN chmod 755 /scripts
COPY --chmod=755 ./notes/notes.py /scripts/notes.py

USER wa11y

RUN mkdir -p /home/wa11y/.irssi
COPY ./config/irssi.config /home/wa11y/.irssi/config
COPY ./config/elite.theme /home/wa11y/.irssi/elite.theme
COPY ./config/default.theme /home/wa11y/.irssi/default.theme

WORKDIR /home/wa11y
COPY ./config/.bashrc .bashrc

RUN python3 -m venv env \
    && /home/wa11y/env/bin/pip install requests 
ENV PATH="/home/wa11y/env/bin:$PATH"

CMD [ "tail", "-f", "/dev/null" ]