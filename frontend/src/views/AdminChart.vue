<template>
  <div class="p-6"  style="overflow-y: scroll;">
    <h1 >Popular Quizzes</h1>

    <!-- Canvas for Chart.js -->
    
    <div class="chart-wrapper">
       <canvas ref="barChart" ></canvas>
    </div>
    <div style="overflow-y: scroll;">
    <table class="mt-8 min-w-full table-auto border-collapse border border-gray-300">
      <thead>
        <tr class="bg-gray-100">
          <th class="border px-4 py-2">Quiz ID</th>
          <th class="border px-4 py-2">Date</th>
          <th class="border px-4 py-2">Chapter Name</th>
          <th class="border px-4 py-2">Attempts</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="quiz in quizzes" :key="quiz.quiz_id">
          <td class="border px-4 py-2">{{ quiz.quiz_id }}</td>
          <td class="border px-4 py-2">{{ formatDate(quiz.date_of_quiz) }}</td>
          <td class="border px-4 py-2">{{ quiz.chapter_name }}</td>
          <td class="border px-4 py-2">{{ quiz.attempts }}</td>
        </tr>
      </tbody>
    </table>
    </div>
  </div>
  
</template>

<script>
import {
  Chart,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js';

Chart.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default {
  name: 'AdminChart',
  data() {
    return {
      quizzes: [],
      chart: null,
    };
  },
  methods: {
    async fetchPopularQuizzes() {
      try {
        const response = await fetch('http://127.0.0.1:5000/admin/popular-quizzes');
        const data = await response.json();
        this.quizzes = data;

        // Prepare chart data
        const labels = this.quizzes.map(q => q.chapter_name);
        const dataset = this.quizzes.map(q => q.attempts);

        this.renderChart(labels, dataset);
      } catch (error) {
        console.error('Error fetching quizzes:', error);
      }
    },
    renderChart(labels, data) {
      const ctx = this.$refs.barChart.getContext('2d');

      if (this.chart) {
        this.chart.destroy(); // destroy old chart if exists
      }

      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: 'Quiz Attempts',
            data,
            backgroundColor: '#4f46e5',
          }],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: true,
            },
            title: {
              display: true,
              text: 'Quiz Attempts per Chapter',
            },
          },
        },
      });
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString();
    },
  },
  mounted() {
    this.fetchPopularQuizzes();
  },
};
</script>

<style scoped>
table {
  width: 100px;
 ;
  border-collapse: collapse;
}
.chart-wrapper canvas {
  width: 700px !important;
  height: 300px !important;
}

</style>
