FROM python:3.12-slim
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install curl

RUN addgroup -gid 1001 celery && \
    useradd -g 1001 -ms /bin/bash celery

USER celery
WORKDIR /home/celery

# app
RUN mkdir example
COPY example example

# python venv
ENV VIRTUAL_ENV=/home/celery/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

#CMD ["python", "-m", "example.server"]
CMD ["python"]