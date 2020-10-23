# 公式のpostgresイメージ
FROM postgres:12

# ロケールの設定
ARG DB_LANG=ja_JP
RUN localedef -i $DB_LANG -c -f UTF-8 -A /usr/share/locale/locale.alias $DB_LANG.UTF-8
ENV LANG $DB_LANG.utf8
# タイムゾーンの設定(UTCじゃないと動かないシステムあるのでコメントアウト。JST必要ならdocker-compose側などで設定する)
#RUN cp /usr/share/zoneinfo/Japan /etc/localtime

## DB構築用のシェルとSQLを転送
#COPY *.sh /docker-entrypoint-initdb.d/
#COPY *.sql /docker-entrypoint-initdb.d/
