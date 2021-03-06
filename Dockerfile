FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN mkdir /code/media
ADD requirements/prod.txt /code/
RUN pip install -r prod.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
ADD . /code/
RUN python manage.py collectstatic --noinput

