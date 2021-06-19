import styles from "./index.module.scss";
import moment from "moment";
import Props from "../types";
import { useLayoutEffect } from 'react'
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";

am4core.useTheme(am4themes_animated);
const stock: React.FC<Props> = ({ stocks, title}) => {
  let chart = am4core.create("chartdiv", am4charts.XYChart);

  return (
    <section className={styles.stock}>
      <div className={styles.stock__heading}>
        <h1>{title.charAt(0).toUpperCase() + title.slice(1).toLowerCase()}</h1>
      </div>
    </section>
  );
};

export default stock;
