FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gcc \
    libssl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

# TODO Before submitting remove --reload + add workers?
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
