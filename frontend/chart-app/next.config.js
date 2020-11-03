// ファイルの先頭に eslint-disable を追加
/* eslint-disable
    @typescript-eslint/no-var-requires,
    @typescript-eslint/explicit-function-return-type
*/
const { resolve } = require('path')
// withOffline を読み込む
const withOffline = require('next-offline')

const nextConfig = {
  webpack: (config) => {
    // src ディレクトリをエイリアスのルートに設定
    config.resolve.alias['~'] = resolve(__dirname, 'src')
    return config
  }
}

module.exports = nextConfig

// nextConfig を withOffline に渡す
module.exports = withOffline(nextConfig)
