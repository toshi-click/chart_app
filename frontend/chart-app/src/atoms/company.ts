import { atom } from 'recoil'

import { CompanyArticles } from 'types/data/company_articles'

export type CompanyState = {
  CompanyArticles: CompanyArticles
}

const initialState: CompanyState = {
  CompanyArticles: null
}

export const CompanyState = atom({
  key: 'Company',
  default: initialState
})
