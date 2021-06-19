import Head from "next/head";
import fetch from "node-fetch";
import {useRouter} from "next/router";
import Stock from '../../components/stock'
import MainLayout from "../../layouts/index";
import styles from "../../styles/Home.module.scss";

function Chart(props) {
  const router = useRouter();
  if (router.isFallback) {
    return <div>Loading...</div>;
  }

  return (
    <MainLayout>
      <Head>
        <title>Simple Chart</title>
      </Head>
      <div className={styles.contents}>
        <div className={styles.blank}/>
        <div className={styles.main} style={{marginRight: "10%"}}>
          <Stock title="1306" stocks={props.stocks}/>
        </div>
      </div>
    </MainLayout>
  );
}

export async function getStaticPaths() {
  return {
    paths: [],
    fallback: true,
  };
}

export async function getStaticProps({params}) {
  const stockRes = await fetch(
    `http://localhost:8000/stocks/`
  );
  const stockJson = await stockRes.json();
  const stockArticles = await stockJson.stocks;

  const title = 'test1306'

  return {
    props: {stockArticles, title},
    revalidate: 60,
  };
}

export default Chart;
