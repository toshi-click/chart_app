Next.js

環境構築
# Next.js をセットアップ
# （現在のディレクトリで作成しますが必要に応じて変更）
docker run --rm -it -v $PWD:/tmp/next -w /tmp/next node:latest npx create-react-native-app -t with-nextjs

# start
cd frontend/containers
docker-compose build && docker-compose up -d

docker exec -it node yarn upgrade
yarn next dev

# pages を src ディレクトリへ移動
$ mkdir src ; mv pages/ src/pages

# Next.js の設定ファイルを作成
$ touch next.config.js
