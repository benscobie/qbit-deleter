FROM python:3

ADD requirements.txt /
ADD *.py /

RUN pip install -r requirements.txt

CMD [ "python", "./script.py" ]