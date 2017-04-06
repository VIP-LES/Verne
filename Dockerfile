FROM gtviples/verne-dependencies
MAINTAINER Cem Gokmen <cgokmen@gatech.edu>

COPY . /verne
WORKDIR /verne

VOLUME /data

CMD ["python", "./main.py"]
