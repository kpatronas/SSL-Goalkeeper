FROM python:3.7-alpine

COPY . /app
WORKDIR /app
RUN ls -la
RUN pip install -r requirements.txt

CMD [ "python", "python_tests.py" ]
