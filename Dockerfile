FROM armhf/python:2.7
MAINTAINER Cem Gokmen <cgokmen@gatech.edu>

COPY . /verne
WORKDIR /verne

RUN chmod +x install_rtimulib.sh
RUN ./install_rtimulib.sh

RUN pip install -r requirements.txt

VOLUME /data

CMD python main.py
