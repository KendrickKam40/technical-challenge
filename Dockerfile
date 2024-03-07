# SET IMAGE
FROM python:3.9

# SET WORKING DIRECTORY
WORKDIR /code

# COPY DEPENDENCY LIST
COPY ./requirements.txt /code/requirements.txt

# INSTALL PYTHON DEPENDENCIES
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY CODE AND DATA
COPY ./app /code/app
COPY ./data_in /code/data_in

# SETUP PYTHON PATH
ENV PYTHONPATH /code/app

# RUN FASTAPI using UVICORN web server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

