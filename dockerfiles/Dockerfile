FROM python:3.7-alpine

COPY . /
WORKDIR /tests
RUN pip install -r requirements.txt
CMD [ "python", "python_tests.py" ]
