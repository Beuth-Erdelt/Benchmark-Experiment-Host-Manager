FROM python:3

WORKDIR /usr/src/app

ENV DBMSBENCHMARKER_SLEEP 30

RUN apt update
RUN apt install default-jre -y

RUN pip uninstall dbmsbenchmarker -y
RUN pip install dbmsbenchmarker

RUN git clone https://github.com/Beuth-Erdelt/DBMS-Benchmarker

WORKDIR /usr/src/app/DBMS-Benchmarker

COPY . .

RUN apt install nano -y

RUN mkdir -p /results
RUN mkdir -p /results/$DBMSBENCHMARKER_CODE

CMD python ./benchmark.py run -b -d -w connection -mps -f /results/$DBMSBENCHMARKER_CODE -r /results/$DBMSBENCHMARKER_CODE -sf $DBMSBENCHMARKER_CONNECTION -cs -sl $DBMSBENCHMARKER_SLEEP -c "$DBMSBENCHMARKER_CONNECTION" -ca "$DBMSBENCHMARKER_ALIAS" -cf ${DBMSBENCHMARKER_CONNECTION}.config -ms $DBMSBENCHMARKER_CLIENT -st "$DBMSBENCHMARKER_START" -vr

