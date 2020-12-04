// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
// レスポンスの型を追加
type Response = {
  statusCode: number
  json({ name: string }): void
}

// 型を指定＆使用していない引数にアンダースコア接頭詞を追加
export default (_req: void, res: Response): void => {
  res.statusCode = 200
  res.json({ name: 'John Doe' })
}
