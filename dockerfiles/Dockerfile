FROM python:3.7-alpine

COPY . /
RUN ls -la
RUN pip install -r requirements.txt
CMD [ "python", "python_tests.py" ]
