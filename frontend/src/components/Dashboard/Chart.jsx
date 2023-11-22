import React from "react";
import Chart from "react-apexcharts";

const SpendingChart = ({ data }) => {
  // Transform data keys to Date objects and values to the required format

  const getDataWithLabels = () => {
    if (!data) {
      return [];
    }
    let chartData = Object.entries(data).map(([key, value]) => {
      const year = key.substring(0, 4);
      const month = key.substring(4) - 1;
      const date = new Date(year, month).getTime();
      return [date, value];
    });
    chartData.sort((a, b) => a[0] - b[0]);
    return chartData;
  };

  const chartOptions = {
    colors: ["#86b1b4"],
    chart: {
      type: "area",
      fontFamily: "Inter, sans-serif",
      toolbar: {
        show: false,
      },
    },
    tooltip: {
      enabled: true,
      x: {
        format: "MM/yyyy",
      },
    },
    fill: {
      type: "gradient",
      gradient: {
        opacityFrom: 0.55,
        opacityTo: 0,
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: "smooth",
      width: 3,
    },
    xaxis: {
      type: "datetime",
    },
    yaxis: {
      labels: {
        formatter: (value) => `$${value.toFixed(2)}`,
      },
    },
  };

  const series = [
    {
      name: "Monthly Spending",
      data: getDataWithLabels(),
    },
  ];

  return (
    <div className="chart bg-white rounded shadow-md h-full">
      {data ? (
        <Chart options={chartOptions} series={series} type="area" height="100%" />
      ) : (
        <div className="flex  h-full">
        <h1 className="m-auto text-6xl font-thin text-gray-400">Loading...</h1>
      </div>
      )}
    </div>
  );
};

export default SpendingChart;
