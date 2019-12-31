FROM python:3.7-alpine

COPY . /
WORKDIR test-python
RUN ls -la
RUN pip install -r requirements.txt
CMD [ "python", "python_tests.py" ]
