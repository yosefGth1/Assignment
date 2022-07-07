FROM ubuntu
RUN apt-get update 

RUN apt-get install -y python3 
RUN apt-get install -y pip
RUN apt-get install -y git

CMD [“echo”,”Image created”] 
RUN git clone https://github.com/yosefGth1/Assignment.git
RUN python3 Assignment/solution.py
RUN touch requirements
RUN pip install opencv-python  
RUN pip install imutils 
RUN pip install numpy 
RUN pip install matplotlib 
RUN pip install sklearn 