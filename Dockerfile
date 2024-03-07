# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app
COPY ./data_in /code/data_in

# 
ENV PYTHONPATH /code/app

#
RUN apt-get update && apt-get -y install postgresql-client

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

