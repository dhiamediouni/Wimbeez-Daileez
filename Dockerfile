FROM python:3.9

WORKDIR /code

ENV TRANSFORMERS_CACHE=/tmp/huggingface/transformers
ENV HF_HOME=/tmp/huggingface
ENV TF_ENABLE_ONEDNN_OPTS=0
ENV MPLCONFIGDIR=/tmp/.config/matplotlib

RUN mkdir -p /tmp/huggingface/transformers /tmp/.config/matplotlib
RUN chmod -R 777 /tmp/huggingface /tmp/.config/matplotlib

COPY ./requirements.txt /code/requirements.txt
COPY ./HR_consultant_inputs.csv /code/HR_consultant_inputs.csv
COPY ./response.mp3 /code/response.mp3

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

# Set permissions for response.mp3
RUN chmod 666 /code/response.mp3
RUN chmod 666 /code/response.wav

RUN apt-get update \
    && mkdir -p /code/data \
    && rm -rf /code/temp_data \
    && apt-get purge -y --auto-remove unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 7860

CMD ["python", "app.py"]
