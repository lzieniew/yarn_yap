FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-runtime


# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Update PATH to include Rust
ENV PATH="/root/.cargo/bin:${PATH}"

RUN apt-get update && apt-get install -y git

WORKDIR /app

COPY text_to_speech/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY shared_components /app/shared_components
RUN pip install /app/shared_components

CMD ["uvicorn", "text_to_speech.app.main:app", "--host", "0.0.0.0", "--reload"]

