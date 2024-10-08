FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /

RUN apt-get update \
 && apt-get upgrade \
 && apt-get install -y tini \
 && pip install --no-cache-dir -r /requirements.txt \
 && rm -rf /requirements.txt /var/cache/apt/* /var/lib/apt/lists/*

COPY *.py /

ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "python", "-u", "script.py" ]