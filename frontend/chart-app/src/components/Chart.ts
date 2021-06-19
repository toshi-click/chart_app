import { useLayoutEffect } from 'react'

// chart ライブラリ
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";

am4core.useTheme(am4themes_animated);
const candleData = [{
  "date": "2018-08-01",
  "open": "136.65",
  "high": "136.96",
  "low": "134.15",
  "close": "136.49"
}, {
  "date": "2018-08-02",
  "open": "135.26",
  "high": "135.95",
  "low": "131.50",
  "close": "131.85"
}, {
  "date": "2018-10-16",
  "open": "172.69",
  "high": "173.04",
  "low": "169.18",
  "close": "172.75"
}];


function Chart() {
  useLayoutEffect(() => {
    let chart = am4core.create("chartdiv", am4charts.XYChart);

    // ... chart code goes here ...
    chart.dateFormatter.inputDateFormat = 'yyyy-MM-dd';
    chart.paddingRight = 20;

    const dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.location = 0;
    dateAxis.renderer.minGridDistance = 60;
    // INFO: dateAxis.skipEmptyPeriods を true にしておくと、休日の位置に無駄な余白が表示されずに済む
    // dateAxis.skipEmptyPeriods = true;

    const valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.renderer.minWidth = 35;

    let series = chart.series.push(new am4charts.CandlestickSeries());

    series.dataFields.dateX = "date";
    series.dataFields.valueY = "close";
    series.dataFields.openValueY = "open";
    series.dataFields.lowValueY = "low";
    series.dataFields.highValueY = "high";
    // ${変数} を "" や '' で囲むとwarningメッセージが表示されるので`$`を削除した
    series.tooltipText = "Open: [bold]{openValueY.value}[/]\nLow: [bold]{lowValueY.value}[/]\nHigh: [bold]{highValueY.value}[/]\nClose: [bold]{valueY.value}[/]";

    chart.cursor = new am4charts.XYCursor();

    const scrollbarX = new am4charts.XYChartScrollbar();
    scrollbarX.series.push(series);
    chart.scrollbarX = scrollbarX;

    // amChartsのCodePenはこっちのスクロールバーを使っていたけれど、上のやつの方がきれいじゃない？お好みで
    // chart.scrollbarX = new am4core.Scrollbar();

    chart.data = candleData;

    return () => {
      chart.dispose();
    };
  }, []);
}

export default Chart;
