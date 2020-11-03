import * as React from 'react'
import App, { AppProps } from 'next/app'

// ThemeProvider を読み込む
import { ThemeProvider } from 'styled-components'

// 全体に適応する外部 CSS を読み込む
import '../../styles/globals.css'

// テーマを必要に応じて設定
const theme = {}

class MyApp extends App {
  render(): JSX.Element {
    const { Component, pageProps }: AppProps = this.props

    return (
        // `<React.Fragment>` を `<ThemeProvider>` に変更してテーマを渡す
        <ThemeProvider theme={theme}>
            <Component {...pageProps} />
        </ThemeProvider>
    )
  }
}

export default MyApp
