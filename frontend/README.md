# Frontend
Next.js + TypeScript

[参考](https://zenn.dev/higa/articles/d7bf3460dafb1734ef43)


- フレームワーク： Next.js v10.0.2 (React v17.0.1)
- 静的型付け： TypeScript v4.0.5
- PWA： next-pwa v3.1.5
- スタイリング： CSS Modules + SASS v1.29.0
- 状態管理： Recoil v0.1.2
- 静的解析＆整形： EditorConfig + ESLint v7.14.0 + Prettier v2.2.0
- テスト： Jest v26.6.3 + React Testing Library v11.2.2 + Cypress v6.0.1
- コンポーネントカタログ: Stroybook v6.1.9 (StoryShots v6.1.9 を含む)
- フックスクリプト： lint-staged v10.5.2 + husky v4.3.0


環境構築
# Next.js をセットアップ
# （現在のディレクトリで作成しますが必要に応じて変更）
docker run --rm -it -v $PWD:/tmp/next -w /tmp/next node:latest yarn create next-app .

# pages を src ディレクトリへ移動
# Next.js で v9.1 から src に pages を入れること可能になったので、src に入れる形で進めます。
sudo mkdir -p src && sudo mv pages/ src/pages & sudo mv styles/ src/styles
  
# nodeコンテナを起動しておく
cd ../containers/
docker-compose up -d
cd ../chart-app

# TypeScript に対応
# Next.jsで作った環境でTypeScriptを使えるようにする
docker exec -it node yarn add -D typescript @types/react @types/react-dom @types/node

### Next.js を開発モードで起動することで必要なファイルを自動生成
docker exec -it node yarn dev

### src ディレクトリ配下の js と jsx のファイルを ts と tsx に変換
find src/pages -name "_app.js" -or -name "index.js" | sed 'p;s/.js$/.tsx/' | xargs -n2 mv & find src/pages/api -name "*.js" | sed 'p;s/.js$/.ts/' | xargs -n2 mv

### App コンポーネントを変更
App コンポーネントを TypeScript に対応します。
```src/pages/_app.jsx
// React と AppProps を読み込む
import React from 'react'
import { AppProps } from 'next/app'

// 引数に型を追加する
function MyApp({ Component, pageProps }: AppProps): JSX.Element {
  // 関数の内容はそのまま
}
```

### ページコンポーネントを変更
ページコンポーネントを TypeScript に対応します。
```src/pages/index.jsx
// React と NextPage を読み込む
import React from 'react'
import { NextPage } from 'next'

// 型を追加
const Home: NextPage = () => {
  // 関数の内容はそのまま
}

// export を分離
export default Home
```

### API を変更
API を TypeScript に対応します。
```src/pages/api/hello.ts
// レスポンスの型を追加
type Response = {
  statusCode: number
  json({ name: string }): void
}

// 型を指定＆使用していない引数にアンダースコア接頭詞を追加
export default (_req: void, res: Response): void => {
  // 関数の内容はそのまま
}
```

## Document コンポーネントを追加
[Document コンポーネント](https://nextjs.org/docs/advanced-features/custom-document) を使うと、初期状態だと自動で追加される <html> や <body> に変更を加えることができます。

### Document コンポーネントを作成
```
touch src/pages/_document.jsx
```

### 作成した Document コンポーネントに以下を記述します。
```
import React from 'react'
import Document, { Html, Head, Main, NextScript } from 'next/document'

interface MyDocumentInterface {
  url: string
  title: string
  description: string
}

class MyDocument extends Document implements MyDocumentInterface {
  url = 'https://example.com'
  title = 'Demo Next.js'
  description = 'Demo of Next.js'

  render(): JSX.Element {
    return (
      <Html lang="ja-JP">
        <Head>
          {/* `<Head>` の内容は必要に応じて変更 */}
          <meta name="description" content={this.description} />
          <meta name="theme-color" content="#333" />
          <meta property="og:type" content="website" />
          <meta property="og:title" content={this.title} />
          <meta property="og:url" content={this.url} />
          <meta property="og:description" content={this.description} />
          <meta property="og:site_name" content={this.title} />
          <meta property="og:image" content={`${this.url}/ogp.png`} />
          <meta name="format-detection" content="telephone=no" />
          <meta name="twitter:card" content="summary_large_image" />
          <meta name="twitter:title" content={this.title} />
          <meta name="twitter:description" content={this.description} />
          <meta name="twitter:image" content={`${this.url}/ogp.png`} />
          <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    )
  }
}

export default MyDocument
```

## ベース URL を設定
### TypeScript の設定を変更
TypeScript の設定にモジュールインポートのベース URL を追記します。
```tsconfig.json
{
  "compilerOptions": {
    // ベース URL を追加
    "baseUrl": "src"
  }
}
```

### 各コンポーネントを変更
各コンポーネントのモジュールインポートの指定を、ベース URL 指定に変更します。
```
sed -i '' -e 's/..\/styles/styles/' src/pages/_app.tsx & sed -i '' -e 's/..\/styles/styles/' src/pages/index.tsx
```

## PWA に対応
### インストール
PWA のモジュールをインストールします。
```
docker exec -it node yarn add next-pwa
```

### 設定ファイルの追加
touch next.config.js
```next.config.js
const withPWA = require('next-pwa')

module.exports = withPWA({
  pwa: {
    dest: 'public'
  }
})
```

### ウェブアプリマニフェストを追加
1. [Web App Manifest Generator ](https://app-manifest.firebaseapp.com/) でウェブアプリマニフェスト関連のファイルを作成します
1. 作成した manifest.json と images フォルダを public 直下に設置します

### Document コンポーネントを変更
Document コンポーネントにマニュフェストへのリンクを追記します。
```src/pages/_document.tsx
<Head>
  <link rel="manifest" href="/manifest.json" />
</Head>
```

### 無視ファイルを追加
```.gitignore
**/public/precache.*.*.js
**/public/sw.js
**/public/workbox-*.js
**/public/worker-*.js
**/public/precache.*.*.js.map
**/public/sw.js.map
**/public/workbox-*.js.map
**/public/worker-*.js.map
```

## 状態管理ライブラリを追加
### Recoil のインストール
```
docker exec -it node yarn add recoil
```
使い方は[ドキュメント](https://recoiljs.org/docs/basic-tutorial/intro/) を確認してください。

## スタイルの設定
### SASS のインストール
```
docker exec -it node yarn add -D sass
```

### SASS ファイルに変換
src/styles ディレクトリ内の CSS ファイルを SASS ファイルに変換します
```
find src/styles -name "*.css" | sed 'p;s/.css$/.scss/' | xargs -n2 mv
```

### SASS ファイルを読み込むように変更
CSS ファイルを SASS ファイルに変換しましたので、正しく読み込めるようにコンポーネントを変更します。
```
sed -i '' -e 's/\.css/\.scss/' src/pages/_app.tsx && sed -i '' -e 's/\.css/\.scss/' src/pages/index.tsx
```

## デフォルト CSS の追加
### インストール
sanitize.css をインストールします
```
docker exec -it node yarn add -D sanitize.css
```
### App コンポーネントを変更
デフォルト CSS を全体に適応する為に、App コンポーネントで sanitize.css を読み込みます。
```src/pages/_app.tsx
// sanitize.css を読み込む
import 'sanitize.css'
```

## 静的解析と整形のツールを追加
### EditorConfig の追加
```.editorconfig
# editorconfig.org
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false
```

### Prettier の追加
インストール
```
docker exec -it node yarn add -D prettier
```
### 設定ファイルの追加
```.prettierrc.js
module.exports = {
  semi: false,
  arrowParens: 'always',
  singleQuote: true,
}
```

### ESLint の追加
ESLint の関連モジュールをインストールします。
```
docker exec -it node yarn add -D eslint eslint-plugin-react \
                                 eslint-config-prettier eslint-plugin-prettier \
                                 @typescript-eslint/parser @typescript-eslint/eslint-plugin
```
### 設定ファイルの追加
```.eslintrc.js
module.exports = {
  ignorePatterns: ['!.eslintrc.js', '!.prettierrc.js'],
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/eslint-recommended',
    'plugin:prettier/recommended',
    'prettier/@typescript-eslint'
  ],
  plugins: ['@typescript-eslint', 'react'],
  parser: '@typescript-eslint/parser',
  env: {
    browser: true,
    node: true,
    es6: true,
    jest: true
  },
  parserOptions: {
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true
    }
  },
  settings: {
    react: {
      version: 'detect'
    }
  },
  rules: {
    // 必要に応じてルールを追加
    'react/prop-types': 'off',
    'react/react-in-jsx-scope': 'off',
    '@typescript-eslint/no-explicit-any': 'off'
  }
}
```

### Next.js の設定ファイルを修正
Next.js の設定ファイルの先頭に eslint-disable を設定する。
```next.config.js
/* eslint-disable
   @typescript-eslint/no-var-requires
*/
```

### NPM スクリプトの追加
ESLint を実行する NPM スクリプトを追記します。
```package.json
{
  "scripts": {
    "lint": "eslint --ext .js,.jsx,.ts,.tsx --ignore-path .gitignore ."
  }
}
```
Lint実行テスト
```
docker exec -it node yarn lint
# 自動整形
docker exec -it node yarn lint --fix
```

### VSCode の設定
```.vscode/settings.json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ]
}
```

### 無視ファイルを追加
```.gitignore
# ESLint のキャッシュファイルを追加
.eslintcache
```

## テストの追加
### Jest を追加
```
# Jest 関連モジュールをインストール
docker exec -it node yarn add -D jest identity-obj-proxy

# Jest の TypeScript に関するモジュールをインストール
docker exec -it node yarn add -D ts-jest @types/jest
```
### 設定ファイルの追加
```jest.config.js
module.exports = {
  preset: 'ts-jest',
  roots: ['<rootDir>/src'],
  moduleNameMapper: {
    // CSS モックをモックする設定
    '\\.(css|scss)$': 'identity-obj-proxy',
    // pages と components ディレクトリのエイリアスを設定（必要であれば他のディレクトリも追加）
    '^(pages|components)/(.+)': '<rootDir>/src/$1/$2',
  },
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],
  globals: {
    'ts-jest': {
      tsconfig: {
        jsx: 'react',
      },
    },
  },
}
```

### NPM スクリプトの追加
```package.json
{
  "scripts": {
    "test": "jest src/__tests__/.*/*.test.tsx?$",
  }
}
```
### テストの追加
テストファイルを置くフォルダと、サンプルのテストファイルを作成します。
```
mkdir src/__tests__ && touch src/__tests__/Sample.test.tsx
```

```src/__tests__/Smaple.test.tsx
/// <reference types="jest" />

import React from 'react'
import Home from 'pages/index'

it('Home ページコンポーネントが存在している', () => {
  expect(Home).toBeTruthy()
})
```

### テストのテスト
```
docker exec -it node yarn test
```

### React Testing Library を追加
React Testing Library をインストールします。
```
docker exec -it node yarn add -D @testing-library/react
```
適当なテストを追記してみます。
```src/__tests__/Smaple.test.tsx
// React と React Testing Library を読み込みます
import React from 'react'
import { cleanup, render, screen } from '@testing-library/react'

// 各テスト実行後にレンダーしたコンポーネントをアンマウントする
afterEach(cleanup)

it('「Next.js!」のリンクが Next.js の公式サイトのトップページである', () => {
  render(<Home />)
  expect(screen.getByText('Next.js!').getAttribute('href')).toBe(
    'https://nextjs.org'
  )
})
```
