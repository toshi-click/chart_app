import styles from "./index.module.scss";
import moment from "moment";
import Props from "../types";

const stock: React.FC<Props> = ({ stocks, title}) => {
  return (
    <section className={styles.stock}>
      <div className={styles.stock__heading}>
        <h1>{title.charAt(0).toUpperCase() + title.slice(1).toLowerCase()}</h1>
      </div>
      {stocks.map((stock, index) => {
        const time = moment(stock.publishedAt || moment.now())
        .fromNow()
        .slice(0, 1) == "a"
        ? 1
        : moment(stock.publishedAt || moment.now())
            .fromNow()
            .slice(0, 1);
        return (
          <a href={stock.url} key={index} target="_blank" rel="noopener">
            <stock className={styles.stock__main}>
              <div className={styles.stock__title}>
                <p>{stock.title}</p>
                <p className={styles.stock__time}>
                  {time}
                  時間前
                </p>
              </div>
              {stock.urlToImage && (
                <img
                  key={index}
                  src={stock.urlToImage}
                  className={styles.stock__img}
                  alt={`${stock.title} image`}
                />
              )}
            </stock>
          </a>
        );
      })}
    </section>
  );
};

export default stock;
