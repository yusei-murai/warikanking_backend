FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt ./
#RUN rm -rf /var/lib/mysql
#RUN rm -rf mysql_data
RUN python3 -m pip install --upgrade pip setuptools
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt

COPY . ./

EXPOSE 8000