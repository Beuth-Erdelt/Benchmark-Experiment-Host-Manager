# Image of the Evaluator Container

This image contains
* Dashboard of [DBMSBenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker) at port 8050
* A Jupyter Notebook Server at port 8888

## Build Commands

```
docker build -t perdelt/bexhoma:dashboard --no-cache .
docker push perdelt/bexhoma:dashboard
```
