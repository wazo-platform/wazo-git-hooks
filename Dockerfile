FROM debian:bullseye-slim
RUN apt-get update -q \
        && apt-get install -y git dh-make locales locales-all \
        && rm -rf /var/lib/apt/lists/* \
        && locale-gen en_US.UTF-8

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

COPY wazo_hook_utils.py /wazo_hook_utils.py
COPY changelog_check.py /changelog_check.py
