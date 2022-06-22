FROM python:3.6

EXPOSE 5000

WORKDIR /app

COPY static /app/static
COPY templates /app/templates
ADD app-release.apk /app/app-release.apk

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY api.py /app
CMD python api.py