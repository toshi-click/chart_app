import {useRouter} from 'next/router';

const Stock =()=>{
  //routerオブジェクトを用意
  const router = useRouter();

  console.log(router.query);

  return (
    <div>
      {/*routerオブジェクトでクエリストリングを取り出す */}
      show {router.query.stock} !
    </div>
  );
}

export default Stock
