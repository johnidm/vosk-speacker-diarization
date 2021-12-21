FROM python:3.10.1

WORKDIR /service

COPY /api /model run.sh ./

RUN pip install -r requiremets.txt

ENTRYPOINT ["./run.sh"]