FROM python:2.7
MAINTAINER Cem Gokmen <cgokmen@gatech.edu>

COPY app /app
WORKDIR /app

RUN install_git.sh
RUN install_rtimulib.sh
RUN pip install -r requirements.txt

VOLUME /data
EXPOSE 9000

CMD twistd -n -l - -y nobelgt.tac