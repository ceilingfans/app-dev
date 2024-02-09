/* globals Chart:false */

(() => {
  "use strict";

  const labels = {
    overview: ["2021", "2022", "2023", "2024"],
    quarterly: ["Q1", "Q2", "Q3", "Q4"],
    weekly: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  };

  const rawData = {
    siteTraffic: {
      datasets: {
        overview: [12938, 42918, 132001, 170923],
        quarterly: [59202, 25102, 32952, 53667],
        weekly: [2901, 1820, 2242, 2312, 2692, 2840, 3092],
      },
    },
    transactions: {
      datasets: {
        overview: [201, 192, 552, 1034],
        quarterly: [323, 192, 242, 272],
        weekly: [15, 7, 11, 10, 12, 20, 30]
      }
    },
    customers: {
      datasets: {
        overview: [10, 299, 500, 1249],
        quarterly: [378, 240, 299, 332],
        weekly: [21, 11, 16, 13, 20, 31, 42]
      }
    }
  };

  const filter = document.getElementById("dashboard-filter");
  filter.addEventListener("change", () => {
    const value = filter.value;

    traffic.config.data.labels = labels[value];
    traffic.config.data.datasets[0].data = rawData.siteTraffic.datasets[value];
    traffic.update();

    transactions.config.data.labels = labels[value];
    transactions.config.data.datasets[0].data =
      rawData.transactions.datasets[value];
    transactions.update();

    customers.config.data.labels = labels[value];
    customers.config.data.datasets[0].data = rawData.customers.datasets[value];
    customers.update();
  });

  // Graphs
  // eslint-disable-next-line no-unused-vars
  const traffic = new Chart(document.getElementById("traffic-graph"), {
    type: "line",
    data: {
      labels: labels.overview,
      datasets: [
        {
          data: rawData.siteTraffic.datasets.overview,
          lineTension: 0.35,
          backgroundColor: "transparent",
          borderColor: "#007bff",
          borderWidth: 4,
          pointBackgroundColor: "#007bff",
        },
      ],
    },
    options: {
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          boxPadding: 3,
        },
      },
    },
  });
  const transactions = new Chart(document.getElementById("transaction-graph"), {
    type: "line",
    data: {
      labels: labels.overview,
      datasets: [
        {
          data: rawData.transactions.datasets.overview,
          lineTension: 0.35,
          backgroundColor: "transparent",
          borderColor: "#007bff",
          borderWidth: 4,
          pointBackgroundColor: "#007bff",
        },
      ],
    },
    options: {
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          boxPadding: 3,
        },
      },
    },
  });
  const customers = new Chart(document.getElementById("customer-graph"), {
    type: "line",
    data: {
      labels: labels.overview,
      datasets: [
        {
          data: rawData.customers.datasets.overview,
          lineTension: 0.35,
          backgroundColor: "transparent",
          borderColor: "#007bff",
          borderWidth: 4,
          pointBackgroundColor: "#007bff",
        },
      ],
    },
    options: {
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          boxPadding: 3,
        },
      },
    },
  });
  const plans = new Chart(document.getElementById("plan-graph"), {
    type: "doughnut",
    data: {
      labels: ["Bronze", "Silver", "Gold"],
      datasets: [
        {
          data: [60, 37, 13],
          backgroundColor: [
            "rgb(205, 127, 50)",
            "rgb(192, 192, 192)",
            "rgb(255, 215, 0)",
          ],
          hoverOffset: 4,
        },
      ],
    },
    options: {
      plugins: {
        legend: {
          display: true,
        },
        tooltip: {
          boxPadding: 3,
        },
      },
    },
  });
  const topCustomers = new Chart(
    document.getElementById("top-customer-graph"),
    {
      type: "bar",
      data: {
        labels: [
          "John Doe",
          "Jane Doe",
          "John Smith",
          "Jane Smith",
          "John Johnson",
        ],
        datasets: [
          {
            data: [2420, 2102, 1520, 1240, 929],
            backgroundColor: "rgba(0, 0, 255, 0.5)",
            borderColor: "rgb(0, 0, 255)",
            borderWidth: 2,
          },
        ],
      },
      options: {
        plugins: {
          legend: {
            display: false,
          },
          tooltip: {
            boxPadding: 3,
          },
        },
      },
    }
  );
})();
