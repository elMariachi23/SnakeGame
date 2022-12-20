FROM ubuntu
WORKDIR /usr/src/app
COPY . .
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-pygame \
    x11-apps
RUN pip install -r requirements.txt
CMD ["python3", "snake_game.py"]
