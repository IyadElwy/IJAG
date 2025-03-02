FROM debian:latest


RUN apt update -y \
    && apt upgrade -y \
    && apt install python3 -y \
    && apt install python3-venv -y \
    && apt install python3-pip -y


RUN mkdir /app
WORKDIR /app
COPY . .

RUN python3 -m venv env \
    && /app/env/bin/pip install fastapi[standard] pydantic   

ENV PATH="/app/env/bin:$PATH"
ENTRYPOINT ["python3", "/app/src/run.py"]

