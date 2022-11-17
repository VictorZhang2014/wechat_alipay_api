FROM python:3.9.13-slim

EXPOSE 9123

RUN mkdir -p /home/api_pay
WORKDIR /home/api_pay
COPY ./ /home/api_pay

COPY requirements.txt /home/api_pay
RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "main.py"]
