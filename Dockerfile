FROM python:3.6
COPY . /project/
WORKDIR /project
RUN pip install -r requirements.txt
CMD ["python", "src/server.py"]
