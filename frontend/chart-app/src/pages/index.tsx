import Head from 'next/head'
import MainLayout from "../layouts";
import styles from "../styles/Home.module.scss";

import Link from 'next/link'

export default function Home(props) {
  return (
    <MainLayout>
      <Head>
        <title>Simple Chart</title>
        <link rel="icon" href="/favicon.ico"/>
      </Head>
      <div className={styles.contents}>
        <h1 className={styles.title}>
          Read <Link href="/chart/1306"><a>chart page!</a></Link>
        </h1>
      </div>
    </MainLayout>
  );
}
