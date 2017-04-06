FROM gtviples/verne-dependencies
MAINTAINER Cem Gokmen <cgokmen@gatech.edu>

COPY . /verne
WORKDIR /verne

RUN pip install -r requirements.txt

VOLUME /data

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["python", "./main.py"]
