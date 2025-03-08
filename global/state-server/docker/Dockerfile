FROM debian:latest


RUN apt update -y \
    && apt upgrade -y \
    && apt install python3 -y \
    && apt install python3-venv -y \
    && apt install python3-pip -y


RUN mkdir /state-server
WORKDIR /state-server
COPY . .

RUN python3 -m venv env \
    && /state-server/env/bin/pip install fastapi[standard] pydantic kubernetes   

ENV PATH="/state-server/env/bin:$PATH"
ENTRYPOINT ["python3", "/state-server/src/run.py"]

