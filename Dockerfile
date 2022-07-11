FROM ubuntu
RUN apt-get update 

RUN apt-get install -y python3 
RUN apt-get install -y pip
RUN apt-get install -y git
RUN apt-get install bash


RUN git clone https://github.com/yosefGth1/Assignment.git

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN python3 solution.py 
