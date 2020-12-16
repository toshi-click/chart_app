import { useEffect, useMemo } from 'react'

// recoilでの状態保存系
import { CompanyArticles } from 'types/data/company_articles'
import { PriceArticles } from 'types/data/price_articles'
import { useRecoilState } from 'recoil'
import { CompanyState } from 'atoms/company'
import { PriceState } from 'atoms/price'

import {useRouter} from 'next/router';
import Link from 'next/link'

export const codeChart = () => {
  // 生成したStateの呼び出し
  const [company, set_company] = useRecoilState(CompanyState)
  const companyArticles = useMemo(() => company.CompanyArticles, [company.CompanyArticles])
  const [price, set_price] = useRecoilState(PriceState)
  const priceArticles = useMemo(() => price.PriceArticles, [price.PriceArticles])

  useEffect(() => {
    const getter = async () => {
      const res = await fetch('/api/chart').catch((err) => {
        console.error(err)
        throw new Error(err)
      })
      const data: PriceArticles = await res.json()
      set_price((state) => ({
        ...state,
        priceArticles: data
      }))
    }

    // 未取得だったらgetter関数を呼び出す
    if (!priceArticles) {
      getter()
    }
  }, [set_price, priceArticles])

  return {
    priceArticles
  }
}
