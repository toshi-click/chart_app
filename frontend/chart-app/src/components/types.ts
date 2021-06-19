type Props = {
  stocks?: [
    stock: {
      code: number;
      date: string;
      open_price: number;
      close_price: number;
      high_price: number;
      low_price: number;
      volume: bigint;
      moving_averages5?: string;
      moving_averages25?: string;
      moving_averages75?: string;
      moving_averages100?: string;
      moving_averages200?: string;
      created: string;
      updated: string;
    }
  ];
};

export default Props
