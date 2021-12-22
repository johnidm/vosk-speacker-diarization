FROM python:3.10.1

RUN apt update && apt install -y ffmpeg libavcodec-extra

WORKDIR /service

COPY api/ api/
COPY model/ model/

COPY run.sh requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["/service/run.sh"]