import React from 'react';
import Chart from 'react-apexcharts';

const SpendingChart = ({ data, labels }) => {
  const chartOptions = {
    colors: ['#86b1b4'],
    chart: {
      type: 'area',
      fontFamily: 'Inter, sans-serif',
      toolbar: {
        show: false,
      },
    },
    tooltip: {
      enabled: true,
      x: {
        format: 'MM/yyyy',
      },
    },
    fill: {
      type: 'gradient',
      gradient: {
        opacityFrom: 0.55,
        opacityTo: 0,
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: 'smooth',
      width: 3,
    },
    xaxis: {
      type: 'datetime',
      categories: labels,
    },
    yaxis: {
      labels: {
        formatter: (value) => `$${value.toFixed(2)}`,
      },
    },
  };

  const series = [{
    name: 'Monthly Spending',
    data: data,
  }];

  return (
    <div className="chart bg-white rounded shadow-md h-full">
      <Chart options={chartOptions} series={series} type="area" height="100%" />
    </div>
  );
};

export default SpendingChart;
