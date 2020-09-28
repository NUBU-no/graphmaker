# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /app


# copy the dependencies file to the app directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# Copy rest of the contents to /app
COPY . .

# command to run on container start
# ENTRYPOINT [ "python" ]

CMD [ "flask", "run", "--host=0.0.0.0" ]