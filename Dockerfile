FROM graphnn:test

ADD . $HOME/graph_comb_opt
RUN rm -r /graphnn

RUN apt-get update && apt-get install -y python python-pip
RUN pip install numpy networkx==2.2 tqdm matplotlib==2.0.2