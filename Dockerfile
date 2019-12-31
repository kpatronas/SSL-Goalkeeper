FROM python:3.7-alpine
RUN pip install pipenv

COPY / /app
WORKDIR /app
RUN ls -la
#RUN pip install -r ./tests/requirements.txt

#CMD [ "python", "python_tests.py" ]
