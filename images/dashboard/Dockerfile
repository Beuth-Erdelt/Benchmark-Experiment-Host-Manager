FROM python:3

WORKDIR /usr/src/app

RUN apt update
RUN apt install default-jre -y

RUN apt install zip -y

RUN pip uninstall dbmsbenchmarker -y
RUN pip install dbmsbenchmarker

RUN pip install jupyter
RUN pip install jupyter_contrib_nbextensions
RUN jupyter contrib nbextension install --user
RUN jupyter nbextensions_configurator enable --user
RUN jupyter nbextension enable toc2/main

RUN git clone https://github.com/Beuth-Erdelt/DBMS-Benchmarker

WORKDIR /usr/src/app/DBMS-Benchmarker

RUN git pull

RUN apt install nano -y

RUN mkdir /results

CMD [ "python", "./dashboard.py", "-r", "/results"]
