<template>
  <div style="padding: 20px; width:1220px; height: 480px;" class="d-flex flex-column h-98"  >
   <h5>
  Time Left: {{ hours }}:{{ minutes.toString().padStart(2, '0') }}:{{ seconds.toString().padStart(2, '0') }}
</h5>

    <div v-for="q in questions" :key="q.id" style="overflow-y: scroll; width:800px;height:100px" class="card my-2 mx-4 mx-auto border " >
      <h5 class="card-header">{{ q.question_statement }}</h5>
      <select class="card-title mx-2 my-3" v-model="userAnswers[q.id]">
        <option disabled value="">Choose</option>
        <option :value="q.option_1">{{ q.option_1 }}</option>
        <option :value="q.option_2">{{ q.option_2 }}</option>
        <option :value="q.option_3">{{ q.option_3 }}</option>
        <option :value="q.option_4">{{ q.option_4 }}</option>
      </select>
    </div>
   <button class="btn btn-secondary mt-auto"  @click="submitQuiz">Submit</button>
  </div>
   
</template>

<script>
export default {
  data() {
    return {
      quizId: this.$route.params.qid,
      questions: [],
      userAnswers: {},
      timer: null,
      totalSeconds: 0,
      minutes: 0,
      seconds: 0,
      hours: 0
    };
  },
  mounted() {
    fetch(`http://127.0.0.1:5000/api/quiz/${this.quizId}/questions`, {
      headers: {
        "Authentication-Token": localStorage.getItem("auth_token")
      }
    })
      .then(res => res.json())
      .then(data => {
        this.questions = data.questions;
        this.totalSeconds = data.duration_seconds;
        this.minutes = Math.floor(this.totalSeconds / 60);
        this.seconds = this.totalSeconds % 60;
        this.startTimer();
      });
  },
  methods: {
    startTimer() {
      this.timer = setInterval(() => {
        if (this.totalSeconds > 0) {
          this.totalSeconds--;
          this.hours = Math.floor(this.totalSeconds / 3600);
            this.minutes = Math.floor((this.totalSeconds % 3600) / 60);
            this.seconds = this.totalSeconds % 60;
        } else {
          clearInterval(this.timer);
          this.submitQuiz();
        }
      }, 1000);
    },
    submitQuiz() {
      clearInterval(this.timer);
      const payload = Object.entries(this.userAnswers).map(([id, answer]) => ({
        id: Number(id),
        answer
      }));
      fetch(`http://127.0.0.1:5000/api/quiz/${this.quizId}/submit`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth_token")
        },
        body: JSON.stringify(payload)
      })
        .then(res => res.json())
        .then(data => {
          alert(`Your score: ${data.score}`);

          this.$router.push("/user");
        });
    }
  }
};
</script>
