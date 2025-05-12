const elements = {
  frequentChart: document.querySelector("#frequent-chart"),
  ctrChart: document.querySelector("#ctr-chart"),
  pieChart: document.querySelector("#pie-chart-container"),
  heatmapChart: document.querySelector("#heatmap-chart"),
  frequentSelect: document.querySelector("#frequent-column-select"),
  ctrSelect: document.getElementById("ctr-column-select"),
  pieSelect: document.getElementById("pie-column-select"),
  boxplotSelect: document.getElementById("boxplot-select"),
  mixedChartSelect: document.getElementById("column-select"),
  analyticsReport: document.getElementById("analytics-report"),
  dataSummaryTableBody: document.getElementById("data-summary-table-body"),
  boxplotChart: document.getElementById("boxplot-chart"),
  barChart1: document.getElementById("bar-chart-1"),
  scatterXSelect: document.getElementById("scatter-x-select"),
  scatterYSelect: document.getElementById("scatter-y-select"),
};

// Kiểm tra sự tồn tại của các phần tử DOM
Object.entries(elements).forEach(([key, element]) => {
  if (!element && key !== 'dataSummaryTableBody') console.error(`${key} element not found.`);
});

const charts = {};

// Tùy chọn biểu đồ tĩnh để tái sử dụng
const chartOptions = {
  frequent: {
    chart: { type: "bar", height: 450 },
    colors: ['#1890ff', '#13c2c2'],
    tooltip: { y: { formatter: val => `${val} record${val !== 1 ? 's' : ''}` } }
  },
  ctr: {
    chart: { type: 'area', height: 300 },
    colors: ['#fa541c', '#13c2c2'],
    tooltip: { shared: true, y: { formatter: val => (val * 100).toFixed(2) + '%' } }
  },
  pie: {
    chart: { type: 'pie', height: 300 },
    colors: ['#1890ff', '#13c2c2', '#fa541c', '#52c41a', '#fa8c16'],
    tooltip: { y: { formatter: val => `${val} records` } }
  },
  heatmap: {
    chart: { height: 700, type: 'heatmap' },
    title: { text: 'Heatmap' },
    dataLabels: { enabled: true },
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
  }
};

// Hàm debounce để giới hạn tần suất gọi
function debounce(fn, delay) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn.apply(this, args), delay);
  };
}

// Hàm xử lý lỗi chung
function handleError(error, containerId) {
  console.error(error);
  const container = document.getElementById(containerId);
  if (container) {
    container.innerHTML = `<p style="color: red;">Failed to load chart data. Please try again later.</p>`;
  }
}

// Hàm fetch chung
function fetchChartData(endpoint, renderFn, containerId) {
  fetch(endpoint)
    .then(res => {
      if (!res.ok) throw new Error("Network error");
      return res.json();
    })
    .then(data => renderFn(data))
    .catch(err => handleError(err, containerId));
}

// Hàm lazy loading với IntersectionObserver
function observeAndRender(container, renderFn) {
  if (!container) return;
  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        renderFn();
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  observer.observe(container);
}

// Render Frequent Chart
function renderFrequentChart(column) {
  if (!elements.frequentChart) return;
  fetchChartData(`/api/frequent-chart/?column=${column}`, (data) => {
    const options = {
      ...chartOptions.frequent,
      series: [{ name: column.charAt(0).toUpperCase() + column.slice(1), data: data.values }],
      xaxis: { categories: data.labels }
    };
    if (charts.visitorChart) {
      charts.visitorChart.updateOptions(options);
    } else {
      charts.visitorChart = new ApexCharts(elements.frequentChart, options);
      charts.visitorChart.render();
    }
  }, 'frequent-chart');
}

// Render CTR Chart
function renderCTRChart(column) {
  if (!elements.ctrChart) return;
  fetchChartData(`/api/ctr-chart/?column=${column}`, (data) => {
    const options = {
      ...chartOptions.ctr,
      series: [
        { name: "CTR", data: data.ctr },
        { name: "Frequency", data: data.frequency }
      ],
      xaxis: { categories: data.labels }
    };
    if (charts.ctrChart) {
      charts.ctrChart.updateOptions(options);
    } else {
      charts.ctrChart = new ApexCharts(elements.ctrChart, options);
      charts.ctrChart.render();
    }
  }, 'ctr-chart');
}

// Render Pie Chart
function renderPieChart(column) {
  if (!elements.pieChart) return;
  fetchChartData(`/api/pie-chart/?column=${column}`, (data) => {
    const options = {
      ...chartOptions.pie,
      series: data.values,
      labels: data.labels
    };
    if (charts.pieChart) {
      charts.pieChart.updateOptions(options);
    } else {
      charts.pieChart = new ApexCharts(elements.pieChart, options);
      charts.pieChart.render();
    }
  }, 'pie-chart-container');
}

// Render Heatmap
function renderHeatmap() {
  if (!elements.heatmapChart) return;
  fetchChartData("/api/heatmap-chart/", (data) => {
    const options = {
      ...chartOptions.heatmap,
      series: data.series,
      xaxis: { categories: data.categories }
    };
    if (charts.heatmapChart) {
      charts.heatmapChart.updateOptions(options);
    } else {
      charts.heatmapChart = new ApexCharts(elements.heatmapChart, options);
      charts.heatmapChart.render();
    }
  }, 'heatmap-chart');
}

// Render Boxplot
function fetchAndRenderBoxplot(column) {
  if (!elements.boxplotChart) return;
  fetchChartData(`/api/boxplot-data/?column=${column}`, (data) => {
    const trace = { y: data.values, type: 'box', name: column, boxpoints: 'outliers', marker: { color: '#6366f1' } };
    const layout = { title: `Boxplot of ${column}`, margin: { t: 40 } };
    if (elements.boxplotChart.data) {
      Plotly.restyle('boxplot-chart', { y: [data.values], name: column }, [0]);
      Plotly.relayout('boxplot-chart', { title: `Boxplot of ${column}` });
    } else {
      Plotly.newPlot('boxplot-chart', [trace], layout, { responsive: true });
    }
  }, 'boxplot-chart');
}

// Render Mixed Chart
function fetchAndRenderMixedChart(column) {
  if (!elements.barChart1) return;
  fetchChartData(`/api/click-vs-non-click-ctr/?column=${column}`, (data) => {
    const barTrace = { x: data.index, y: data.click, name: 'Click', type: 'bar', marker: { color: '#4caf50' } };
    const barTraceNonClick = { x: data.index, y: data.nonClick, name: 'Non-Click', type: 'bar', marker: { color: '#f44336' } };
    const lineTrace = { x: data.index, y: data.ctr, name: 'CTR', type: 'line', marker: { color: '#3b82f6' }, yaxis: 'y2' };
    const layout = {
      title: `Click vs Non-Click with CTR for ${column}`,
      barmode: 'group',
      xaxis: { title: column, tickangle: -45 },
      yaxis: { title: 'Count', rangemode: 'tozero' },
      yaxis2: { title: 'CTR', overlaying: 'y', side: 'right', rangemode: 'tozero' },
      transition: { duration: 500, easing: 'cubic-in-out' },
      responsive: true
    };
    if (elements.barChart1.data) {
      Plotly.restyle('bar-chart-1', { x: [data.index, data.index, data.index], y: [data.click, data.nonClick, data.ctr] }, [0, 1, 2]);
      Plotly.relayout('bar-chart-1', { title: `Click vs Non-Click with CTR for ${column}`, xaxis: { title: column } });
    } else {
      Plotly.newPlot('bar-chart-1', [barTrace, barTraceNonClick, lineTrace], layout);
    }
  }, 'bar-chart-1');
}

// Load Analytics Info
function loadAnalyticsInfo() {
  if (!elements.analyticsReport) return;
  fetch('/api/analytics-info/')
    .then(response => response.json())
    .then(data => {
      elements.analyticsReport.innerHTML = data.info_html;
    })
    .catch(error => handleError(error, 'analytics-report'));
}

// Load Data Summary
function loadDataSummary() {
  if (!elements.dataSummaryTableBody) return;
  fetch('/api/data-summary/')
    .then(response => response.json())
    .then(data => {
      const tableBody = elements.dataSummaryTableBody;
      tableBody.innerHTML = "";
      for (let column in data.description) {
        const stats = data.description[column];
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
    .catch(error => handleError(error, 'data-summary-table-body'));
}

// Throttle sự kiện resize
function throttle(fn, limit) {
  let inThrottle;
  return function (...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}


function renderScatterPlot(axis1, axis2) {
  fetch(`/api/scatter-plot/?axis1=${encodeURIComponent(axis1)}&axis2=${encodeURIComponent(axis2)}`)
    .then(res => {
      if (!res.ok) throw new Error("Network response was not ok");
      return res.json();
    })
    .then(data => {
      const trace = {
        x: data.x,
        y: data.y,
        mode: 'markers',
        type: 'scatter',
        marker: { color: '#10b981' }
      };
      const layout = {
        title: `${data.axis1} vs ${data.axis2}`,
        xaxis: { title: data.axis1 },
        yaxis: { title: data.axis2 },
        height: 400
      };
      Plotly.newPlot('scatter-plot', [trace], layout);
    })
    .catch(error => {
      console.error("Scatter plot error:", error);
      const plotDiv = document.getElementById("scatter-plot");
      if (plotDiv) {
        plotDiv.innerHTML = `<p class="text-danger">Error loading scatter plot.</p>`;
      }
    });
}

// Khởi tạo sự kiện và render ban đầu
document.addEventListener("DOMContentLoaded", () => {
  // Frequent Chart
  if (elements.frequentSelect) {
    observeAndRender(elements.frequentChart, () => renderFrequentChart(elements.frequentSelect.value));
    elements.frequentSelect.addEventListener("change", debounce(function () {
      renderFrequentChart(this.value);
    }, 100));
  }

  // CTR Chart
  if (elements.ctrSelect) {
    observeAndRender(elements.ctrChart, () => renderCTRChart(elements.ctrSelect.value));
    elements.ctrSelect.addEventListener("change", debounce(() => {
      renderCTRChart(elements.ctrSelect.value);
    }, 100));
  }

  // Pie Chart
  if (elements.pieSelect) {
    observeAndRender(elements.pieChart, () => renderPieChart(elements.pieSelect.value));
    elements.pieSelect.addEventListener("change", debounce(function () {
      renderPieChart(this.value);
    }, 100));
  }

  // Heatmap
  observeAndRender(elements.heatmapChart, renderHeatmap);

  // Boxplot
  if (elements.boxplotSelect) {
    observeAndRender(elements.boxplotChart, () => fetchAndRenderBoxplot(elements.boxplotSelect.value));
    elements.boxplotSelect.addEventListener("change", debounce(() => {
      fetchAndRenderBoxplot(elements.boxplotSelect.value);
    }, 100));
  }

  // Mixed Chart
  if (elements.mixedChartSelect) {
    observeAndRender(elements.barChart1, () => fetchAndRenderMixedChart(elements.mixedChartSelect.value));
    elements.mixedChartSelect.addEventListener("change", debounce(() => {
      fetchAndRenderMixedChart(elements.mixedChartSelect.value);
    }, 100));
  }

  // Scatter Plot
  if (elements.scatterXSelect && elements.scatterYSelect) {
    const renderScatter = () => renderScatterPlot(elements.scatterXSelect.value, elements.scatterYSelect.value);
    observeAndRender(document.getElementById('scatter-plot'), renderScatter);
    elements.scatterXSelect.addEventListener('change', debounce(renderScatter, 100));
    elements.scatterYSelect.addEventListener('change', debounce(renderScatter, 100));
  }

  // Load Analytics and Summary
  loadAnalyticsInfo();
  loadDataSummary();

  // Resize Handler
  window.addEventListener('resize', throttle(() => {
    if (elements.boxplotChart) Plotly.Plots.resize(elements.boxplotChart);
    if (elements.barChart1) Plotly.Plots.resize(elements.barChart1);
  }, 100));
});