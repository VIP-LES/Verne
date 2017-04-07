FROM gtviples/verne-deps
MAINTAINER Cem Gokmen <cgokmen@gatech.edu>

COPY . /verne
WORKDIR /verne

RUN pip install -r requirements.txt

VOLUME /data

CMD ["python", "./main.py"]
