<template>
  <div class="p-4" style="width:1200px;height: 450px;  overflow-y: scroll;">
    <h2 class="text-xl font-bold mb-4">Past Quiz Scores</h2>
    <div v-if="loading">Loading...</div>
    <table v-if="!loading && pastScores.length" class="min-w-full border" style="height: 350px; overflow-y: scroll;" >
      <thead class="bg-gray-200">
        <tr>
          <th class="px-4 py-2">Quiz Date</th>
          <th class="px-4 py-2">Subject</th>
          <th class="px-4 py-2">Chapter</th>
          <th class="px-4 py-2">Score</th>
          <th class="px-4 py-2">Remarks</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="quiz in pastScores" :key="quiz.quiz_id">
          <td class="border px-4 py-2">{{ quiz.quiz_date }}</td>
          <td class="border px-4 py-2">{{ quiz.subject }}</td>
          <td class="border px-4 py-2">{{ quiz.chapter }}</td>
          <td class="border px-4 py-2">{{ quiz.score }}</td>
          <td class="border px-4 py-2">{{ quiz.remarks }}</td>
        </tr>
      </tbody>
    </table>

    <div v-else-if="!loading" class="text-gray-500">No scores found.</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      pastScores: [],
      loading: true,
    };
  },
  mounted() {
    const userId = localStorage.getItem("id");
    if (!userId) {
      console.error("User ID not found in localStorage.");
      this.loading = false;
      return;
    }

    fetch(`http://127.0.0.1:5000/api/user/${userId}/past-scores`)
      .then(res => {
        if (!res.ok) {
          throw new Error("Failed to fetch");
        }
        return res.json();  // ✅ Important
      })
      .then(data => {
        this.pastScores = data;
      })
      .catch(err => {
        console.error("Failed to fetch scores:", err);
      })
      .finally(() => {
        this.loading = false;
      });
  }
};
</script>

<style scoped>
table {
  border-collapse: collapse;
}
</style>
