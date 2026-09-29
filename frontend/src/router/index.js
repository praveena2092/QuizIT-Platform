import { createRouter, createWebHistory } from 'vue-router'
import Home from "../views/Home.vue"
import Login from "../views/Login.vue"
import Register from "../views/Register.vue"
import Subject from '@/views/Subject.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'
import User from '@/views/User.vue'
import Chapter from '@/views/Chapter.vue'
import Quiz from '@/views/Quiz.vue'
import Question from '@/views/Question.vue'
import UserQuiz from '@/views/UserQuiz.vue'
import QuizTime from '@/views/QuizTime.vue'
import Chart_Admin from '@/views/Chart_Admin.vue'
import AdminChart from '@/views/AdminChart.vue'
import Q1 from '@/views/Q1.vue'
import Score from '@/views/Score.vue'
const routes= [
  {
    path :"/",
    name :"Home",
    component: Home
  },
  {
    path : "/login",
    name : "Login",
    component: Login
  },
  {
    path : "/register",
    name : "Register",
    component: Register
  },
  {
    path :"/subject",
    name:"Subject",
    component:Subject
  },
  {
    path:"/admin",
    name:"Admin",
    component:AdminDashboard
  },{
    path :"/user",
    name : "User",
    component : User
  },
  {
    path :"/chapter/:sid",
    name:"addChapter",
     component:Chapter

    },
    {
      path :"/quiz/:cid",
      name:"addQuiz",
      component:Quiz
    },
    {
      path :"/question/:qid",
      name:"addQuestion",
      component:Question
    },
    {
      path:"/user/quiz/:id",
      name : "UserQuiz",
      component : UserQuiz},
    {
      path :"/userQuizs/:qid",
      name:"quiztime",
      component:QuizTime
    },{
      path:"/admin/summary",
      name:"summaryAdmin",
      component:Chart_Admin

    },
    {
      path:"/admin/chart",
      name:"adminChart",
      component:AdminChart
    },
    {
      path : '/quiz123/:qid',
      name:"quiz123",
      component:Q1
    },{
      path : '/score',
      name:"score",
      component:Score
    }

  ]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  
})

export default router
