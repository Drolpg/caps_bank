FROM python:3.12-alpine
WORKDIR /work
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . .
RUN chmod +x run.sh
CMD ["./run.sh"]
