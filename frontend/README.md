Next.js

環境構築
# Next.js をセットアップ
# （現在のディレクトリで作成しますが必要に応じて変更）
docker run --rm -it -v $PWD:/tmp/next -w /tmp/next node:latest npx create-next-app

# pages を src ディレクトリへ移動
$ mkdir src ; mv pages/ src/pages

# Next.js の設定ファイルを作成
$ touch next.config.js