
FROM python:3.9-alpine AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


FROM gcr.io/distroless/python3

WORKDIR /app

COPY --from=builder /app /app

EXPOSE 5000

CMD ["app.py"]
