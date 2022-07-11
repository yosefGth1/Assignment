FROM ubuntu
WORKDIR /home
RUN apt-get update 

RUN apt-get install -y python3 
RUN apt-get install -y pip
RUN apt-get install -y git
RUN apt-get install bash

RUN git clone https://github.com/yosefGth1/Assignment.git
WORKDIR Assignment

RUN pip3 install -r requirements.txt

RUN python3 solution.py 
RUN python3 tests.py
