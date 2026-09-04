/* GramBiz AI - Chart.js Helper Functions & Theme Configurations */

const GramBizCharts = {
  themeColors: {
    primary: '#10B981',
    primaryDark: '#065F46',
    primaryLight: 'rgba(16, 185, 129, 0.15)',
    amber: '#F59E0B',
    amberLight: 'rgba(245, 158, 11, 0.15)',
    danger: '#EF4444',
    neutralGrid: '#F3F4F6'
  },

  initRevenueVsExpenseChart(canvasId, labels, revenueData, expenseData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Monthly Revenue (₹)',
            data: revenueData,
            backgroundColor: this.themeColors.primary,
            borderRadius: 8,
            borderSkipped: false
          },
          {
            label: 'Monthly Expenses (₹)',
            data: expenseData,
            backgroundColor: this.themeColors.amber,
            borderRadius: 8,
            borderSkipped: false
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { font: { family: 'Plus Jakarta Sans', weight: '600' } } },
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.dataset.label}: ₹${ctx.parsed.y.toLocaleString('en-IN')}`
            }
          }
        },
        scales: {
          x: { grid: { display: false } },
          y: {
            grid: { color: this.themeColors.neutralGrid },
            ticks: {
              callback: (val) => '₹' + val.toLocaleString('en-IN')
            }
          }
        }
      }
    });
  },

  initProfitTrendChart(canvasId, labels, profitData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Net Profit (₹)',
            data: profitData,
            borderColor: this.themeColors.primaryDark,
            backgroundColor: this.themeColors.primaryLight,
            fill: true,
            tension: 0.4,
            pointRadius: 5,
            pointBackgroundColor: this.themeColors.primary
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => `Profit: ₹${ctx.parsed.y.toLocaleString('en-IN')}`
            }
          }
        },
        scales: {
          x: { grid: { display: false } },
          y: {
            grid: { color: this.themeColors.neutralGrid },
            ticks: {
              callback: (val) => '₹' + val.toLocaleString('en-IN')
            }
          }
        }
      }
    });
  },

  initDoughnutChart(canvasId, labels, dataValues) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [
          {
            data: dataValues,
            backgroundColor: [
              '#10B981', '#F59E0B', '#3B82F6', '#8B5CF6', '#EC4899', '#6366F1', '#64748B'
            ],
            borderWidth: 2,
            borderColor: '#ffffff'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'right', labels: { font: { family: 'Plus Jakarta Sans', size: 12 } } }
        },
        cutout: '70%'
      }
    });
  }
};
