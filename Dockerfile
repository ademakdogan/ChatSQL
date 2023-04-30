


#-----------------------
FROM python:3.8-slim-buster
RUN apt-get update && apt-get install make
RUN apt-get install gcc -y
WORKDIR /opt/ChatSql
COPY . .
RUN make install
EXPOSE 9001
CMD ["python","src/main.py"]
