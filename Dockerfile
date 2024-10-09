FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY namecheap_operator.py .

CMD ["kopf", "run", "--standalone", "namecheap_operator.py"]
