## djangoの生成
```bash
docker-compose build
docker-compose run web django-admin startproject config .
```

## データベースの作成
```bash
docker-compose run web python3 manage.py migrate
```

## 全部をきちんと整理しておくため、プロジェクトの中に別のアプリケーションを作ります。
```bash
docker exec -it web python3 manage.py startapp restapi
```
rest_frameworkとrestapiというアプリを使うことをDjangoに知らせるためにsettings.pyのINSTALLED_APPSに追記します。
```
INSTALLED_APPS = (
    ...
    'rest_framework',
    'restapi.apps.RestapiConfig',
)
```

### モデルを作ったあとに
```
docker exec -it web python3 manage.py makemigrations
docker exec -it web python3 manage.py migrate
```

# 管理画面のスーパーユーザーの作成
```
docker exec -it web python3 manage.py createsuperuser
```

### Django Shell
```
docker exec -it web python3 manage.py shell
```

### サーバー上の静的ファイルの更新
```
docker exec -it web python3 manage.py collectstatic
```

### モデル追加後にテーブル作成
```bash
docker exec -it web python3 manage.py makemigrations restapi
docker exec -it web python3 manage.py migrate restapi
```

## django系パッケージの更新
```bash
docker exec -it web pipenv install
docker exec -it web pipenv update
```
