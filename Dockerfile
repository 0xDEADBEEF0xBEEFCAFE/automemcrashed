FROM alpine:latest

RUN apk add --update python3 py3-pip git tcpdump

RUN git clone https://github.com/0xDEADBEEF0xBEEFCAFE/automemcrashed.git memcrashed
WORKDIR automemcrashed
COPY bots.txt .
COPY requirements.txt .
RUN pip3 install -r requirements.txt

ENTRYPOINT ["/bin/sh"]
