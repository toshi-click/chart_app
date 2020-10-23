# https://github.com/jwilder/nginx-proxy
FROM nginx:latest

# Debian set Locale
# tzdataのapt-get時にtimezoneの選択で止まってしまう対策でDEBIAN_FRONTENDを定義する
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get -y install locales task-japanese && \
    locale-gen ja_JP.UTF-8 && \
    rm -rf /var/lib/apt/lists/*
ENV LC_ALL=ja_JP.UTF-8 \
    LC_CTYPE=ja_JP.UTF-8 \
    LANGUAGE=ja_JP:jp
RUN localedef -f UTF-8 -i ja_JP ja_JP.utf8

# Debian set TimeZone
ENV TZ=Asia/Tokyo
RUN echo "${TZ}" > /etc/timezone && \
    rm /etc/localtime && \
    ln -s /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# コンテナのデバッグ等で便利なソフト導入しておく
RUN apt-get update \
    && apt-get -y install vim git curl wget zip unzip net-tools iproute2 iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# カスタム設定ファイルを設置
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf
