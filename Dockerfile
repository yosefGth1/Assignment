FROM ubuntu
RUN apt-get update 

RUN apt-get install -y python3 
RUN apt-get install -y pip
RUN apt-get install -y git
RUN apt-get install bash

RUN pwd
RUN git clone https://github.com/yosefGth1/Assignment.git

CMD [“ls -al”] 

RUN cd Assignment
RUN /bin/bash -c pip install -r requ*
RUN /bin/bash -c python3 solution.py 
