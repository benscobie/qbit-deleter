FROM python:3-slim

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

COPY *.py /

CMD [ "python", "-u", "./script.py" ]