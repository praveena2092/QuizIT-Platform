<template>
  <h1>Summary of the user and Quiz</h1>
  <div>
    <canvas id="myChart"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'ChartAdmin',
  mounted() {
    const ctx = document.getElementById('myChart')?.getContext('2d');
    if (!ctx) {
      console.error('Failed to get 2D context of canvas');
      return;
    }

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
          label: '# of Votes',
          data: [12, 19, 3, 5, 2, 3],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  }
}


</script>
