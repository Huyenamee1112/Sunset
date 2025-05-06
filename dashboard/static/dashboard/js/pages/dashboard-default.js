document.addEventListener("DOMContentLoaded", function () {
  const charts = {};

  function fetchChartData(endpoint, renderFn) {
    fetch(endpoint)
      .then((res) => {
        if (!res.ok) throw new Error("Network error");
        return res.json();
      })
      .then((data) => renderFn(data))
      .catch((err) => {
        console.error("Chart error:", err);
        alert('Failed to load chart data. Please try again later.');
      });
  }

  // Render Frequent Chart
  function renderVisitorChart(column) {
    const chartContainer = document.querySelector("#frequent-chart");

    if (!chartContainer) {
      console.error("Frequent chart container not found.");
      return;
    }

    fetchChartData(`/api/frequent-chart/?column=${column}`, (data) => {
      const options = {
        chart: {
          type: "bar",
          height: 450
        },
        series: [{
          name: column.charAt(0).toUpperCase() + column.slice(1),
          data: data.values
        }],
        xaxis: {
          categories: data.labels
        },
        colors: ['#1890ff', '#13c2c2'],
        tooltip: {
          y: {
            formatter: val => `${val} record${val !== 1 ? 's' : ''}`
          }
        }
      };

      if (charts.visitorChart) {
        charts.visitorChart.updateOptions(options);
      } else {
        charts.visitorChart = new ApexCharts(chartContainer, options);
        charts.visitorChart.render();
      }
    });
  }

  // Render CTR Chart
  function renderCTRChart(column) {
    const chartContainer = document.querySelector("#ctr-chart");

    if (!chartContainer) {
      console.error("CTR chart container not found.");
      return;
    }

    fetchChartData(`/api/ctr-chart/?column=${column}`, (data) => {
      const options = {
        chart: { type: 'area', height: 300 },
        series: [
          { name: "CTR", data: data.ctr },
          { name: "Frequency", data: data.frequency }
        ],
        xaxis: { categories: data.labels },
        colors: ['#fa541c', '#13c2c2'],
        tooltip: {
          shared: true,
          y: {
            formatter: val => (val * 100).toFixed(2) + '%'
          }
        }
      };

      if (charts.ctrChart) {
        charts.ctrChart.updateOptions(options);
      } else {
        charts.ctrChart = new ApexCharts(chartContainer, options);
        charts.ctrChart.render();
      }
    });
  }

  // Handle frequent chart select change
  const select = document.querySelector("#frequent-column-select");
  if (select) {
    renderVisitorChart(select.value);
    select.addEventListener("change", function () {
      renderVisitorChart(this.value);
    });
  } else {
    console.error("Select element for frequent-column-select not found.");
  }

  // Handle CTR chart select change
  const ctrSelect = document.getElementById("ctr-column-select");
  if (ctrSelect) {
    renderCTRChart(ctrSelect.value);
    ctrSelect.addEventListener("change", () => {
      renderCTRChart(ctrSelect.value);
    });
  } else {
    console.error("Select element for ctr-column-select not found.");
  }


    // Render Pie Chart
  function renderPieChart(column) {
    const chartContainer = document.querySelector("#pie-chart-container");

    if (!chartContainer) {
      console.error("Pie chart container not found.");
      return;
    }

    fetchChartData(`/api/pie-chart/?column=${column}`, (data) => {
      const options = {
        chart: {
          type: 'pie',
          height: 300,
        },
        series: data.values,
        labels: data.labels,
        colors: ['#1890ff', '#13c2c2', '#fa541c', '#52c41a', '#fa8c16'],
        tooltip: {
          y: {
            formatter: (val) => `${val} records`,
          },
        },
      };

      if (charts.pieChart) {
        charts.pieChart.updateOptions(options);
      } else {
        charts.pieChart = new ApexCharts(chartContainer, options);
        charts.pieChart.render();
      }
    });
  }

  // Handle Pie chart select change
  const pieSelect = document.getElementById("pie-column-select");

  if (pieSelect) {
    // Initial render of the pie chart
    renderPieChart(pieSelect.value);

    // Event listener to handle dropdown change
    pieSelect.addEventListener("change", function () {
      renderPieChart(this.value);
    });
  } else {
    console.error("Select element for pie-column-select not found.");
  }

  function renderHeatmap() {
    const chartContainer = document.querySelector("#heatmap-chart");
  
    if (!chartContainer) {
      console.error("Heatmap container not found.");
      return;
    }
  
    fetchChartData("/api/heatmap-chart/", (data) => {
      const options = {
        chart: {
          height: 700,
          type: 'heatmap',
        },
        series: data.series,
        title: {
          text: 'Heatmap',
        },
        dataLabels: {
          enabled: true,
        },
        xaxis: {
          categories: data.categories,
        },
        plotOptions: {
          heatmap: {
            shadeIntensity: 0.5,
            colorScale: {
              ranges: [
                { from: -1, to: -0.5, name: 'Negative High', color: '#f87171' },
                { from: -0.5, to: 0, name: 'Negative Low', color: '#facc15' },
                { from: 0, to: 0.5, name: 'Positive Low', color: '#60a5fa' },
                { from: 0.5, to: 1, name: 'Positive High', color: '#2563eb' }
              ]
            }
          }
        }
      };
  
      if (charts.heatmapChart) {
        charts.heatmapChart.updateOptions(options);
      } else {
        charts.heatmapChart = new ApexCharts(chartContainer, options);
        charts.heatmapChart.render();
      }
    });
  }
  renderHeatmap();


  function loadAnalyticsInfo() {
    fetch('/api/analytics-info/')
      .then(response => response.json())
      .then(data => {
        const container = document.getElementById('analytics-report');
        container.innerHTML = data.info_html;
      })
      .catch(error => {
        console.error('Error loading analytics info:', error);
      });
  }

  loadAnalyticsInfo();



  function loadDataSummary() {
    fetch('/api/data-summary/')
      .then(response => response.json())
      .then(data => {
        const tableBody = document.getElementById("data-summary-table-body");
        const description = data.description;
        
        // Clear any existing rows
        tableBody.innerHTML = "";

        // Loop through the summary and create table rows
        for (let column in description) {
          const stats = description[column];
          const row = document.createElement("tr");
          
          row.innerHTML = `
            <td>${column}</td>
            <td>${stats.count}</td>
            <td>${stats.mean}</td>
            <td>${stats.std}</td>
            <td>${stats.min}</td>
            <td>${stats['25_percent']}</td>
            <td>${stats['50_percent']}</td>
            <td>${stats['75_percent']}</td>
            <td>${stats.max}</td>
          `;
          
          tableBody.appendChild(row);
        }
      })
      .catch(error => {
        console.error('Error loading data summary:', error);
      });
  }

  // Load the data summary when the page loads
  loadDataSummary();
});
