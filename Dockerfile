FROM python:3.9.6-slim-buster

# Install gcc.
RUN apt-get update \
&& apt-get install libpq-dev gcc -y \
&& apt-get clean

# Set working directory.
WORKDIR /src

# Installing dependencies.
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy `app/`
ADD ./app ./app
CMD bash -c "uvicorn app.main:app --host 0.0.0.0 --port 3000"
