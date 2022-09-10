FROM python:3.6.9

COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
RUN pip3 install --upgrade pip
# RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install -r requirements.txt

# running migrations
RUN python3 manage.py migrate

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]

