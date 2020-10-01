# set base image (host OS)
FROM python:3.8-slim

# set the working directory in the container
WORKDIR /app


# copy the dependencies file to the app directory
COPY requirements.txt .

#RUN apt-get update
RUN pip install gunicorn
# install dependencies
RUN pip install -r requirements.txt

# Copy rest of the contents to /app
COPY . .

# command to run on container start
# ENTRYPOINT [ "python" ]

#CMD ["flask", "run"]
CMD exec gunicorn -b :$PORT app:app