<template>
    <div class="row border">
        <div class="border" style="background-color: rgba(33,37,41, 0.03);width:1240px ;display: flex; align-items: center; justify-content: space-between;">
                 <div class="col-8 text-start">
                    <h4 class="my-2"> Quiz!</h4>
                </div>
                <div class="col text-end">
                    <input type="date" class="form-control" v-model="search" placeholder="Search Quiz">
                </div>
            </div>
        
        <div class="col-8 border main" style="height:400px; width:800px;overflow-y:scroll">
            <div v-for="q in filteredQuiz" :key="q.id"  class="card my-2">
                <div class="card-body">
                    <p class="card-title">date_of_quiz : {{q.date_of_quiz}}</p>
                    <p class="card-title"> time_duration :{{q.time_duration}}</p>
                    <p class="card-title"> remarks :{{q.remarks}}</p>
                    <button @click="openUpdateModal(q)" v-show="userRole!== 'user'" class="btn mx-2" data-bs-toggle="modal" :data-bs-target="'#modal-' + q.id"   style="background-color: white; color: purple; border: 2px solid purple;">
                    Update
                    </button>
                    <button v-show="userRole!== 'user'" class="btn btn-secondary mx-2" @click=" quizDelete(q.id)" >Delete</button>
                    <router-link :to="{name :'addQuestion',params:{qid :q.id}}" class="btn mx-2" style="background-color: purple; color: white;" v-show="userRole!== 'user'" >Add Question</router-link>
                     <router-link class="btn" style="background-color: purple; color: white;" :to="{name :'UserQuiz',params:{id :q.id}}"  v-show="userRole=== 'user'">View Quiz</router-link>

                </div>
            <!-- Modal definition -->
                <div class="modal fade" :id="'modal-' + q.id"  tabindex="-1">
                <div class="modal-dialog modal-fullscreen-lg-down">
                    <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Update Quiz!...</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                   <p class="text-danger">{{message}}</p>
                    <div class="mb-3">
                        <label for="date_of_quiz" class="form-label">Enter quiz</label>
                        <input type="date" class="form-control" v-model="upquizData[q.id].date_of_quiz" id="date_of_quiz" :placeholder="q.date_of_quiz ? q.date_of_quiz: 'Enter quiz date'"  >
                    </div>
                    <div class="mb-3">
                        <label for="time_duration" class="form-label">Enter time duration</label>
                        <input type="time" class="form-control" v-model="upquizData[q.id].time_duration" id="time_duration" :placeholder="q.time_duration ? q.time_duration : 'Enter quiz duration'"  >
                    </div>
                     <div class="mb-3">
                        <label for="remarks" class="form-label">Enter remarks</label>
                        <input type="tect" class="form-control" v-model="upquizData[q.id].remarks" id="remarks"  :placeholder="q.remarks ? q.remarks : 'Enter remarks'" >
                    </div>
                    <div class="mb-3">
                        <button class="btn btn-primary" @click="updateQuiz(q.id)" style="background-color: purple; color: white;" >Update</button>
                    </div>
                    <div class="mb-3">
                         <router-link class="btn btn-close" data-bs-dismiss="modal" to="/subject" style="background-color: white; color: purple; border: 2px solid purple;">Go back</router-link>
                    </div>
                    </div>
                    </div>
                </div>
                </div>


            </div>
        </div>
       <div class="col-4 border" v-show="userRole!== 'user'">
           <h4> Add Quiz!</h4>
            <div class="mb-3">
                <label for="date_of_quiz" class="form-label">Date of quiz</label>
                <input class="form-control" id="date_of_quiz" type="date" v-model="quizForm.date_of_quiz">
            </div>
            <div class="mb-3">
                <label for="time_duration" class="form-label">Time duartion</label>
                <input class="form-control" id="time_duration" rows="3" type="time" v-model="quizForm.time_duration"></input>
            </div>
            <div class="mb-3">
                <label for="remark" class="form-label">Remarks</label>
                <textarea class="form-control" id="remark" rows="3" v-model="quizForm.remarks"></textarea>
            </div>
            <div class="mb-3">
                <button class="btn link" style="background-color: purple; color: white;"  @click="addQuiz">Add Quiz</button>
            </div>
            </div>
    </div>
</template>
<script>
    export default{
    data : function(){
        return {
            userRole: localStorage.getItem("roles"),
            search: '',
            quizs  : [],
            quizForm : {
                time_of_duration  :"",
                date_of_quiz  :"",
                remarks : " "
            },
            message:"",
             upquizData:{
            }
        }
    },
    mounted(){
          this.loadQuiz()
          if(this.userRole === "user") {
            document.querySelector(".main").style.width = "1220px";
          }
    },
    computed: {
        filteredQuiz() {
             return this.quizs.filter(q =>
            (q.date_of_quiz || '').includes(
                this.search || ''
            )
            );
            return this.quiz ? this.quiz.filter(q => q.date_of_quiz.includes(this.search)) : [];
        }
    },
    methods :{
        loadQuiz: function (){
            const chap_id = this.$route.params.cid;
                           
            console.log(`http://127.0.0.1:5000/api/quiz/get/${chap_id}` )
            fetch(`http://127.0.0.1:5000/api/quiz/get/${chap_id}`,{ 
                method:"GET",
                headers :{
                    "Content-Type": "application/json",
                    "Authentication-Token" : localStorage.getItem("auth_token")
                }
            })
            .then(response => response.json())
            .then(data => {this.quiz=data
                console.log(data)
                if (Array.isArray(data)) {
                    this.quizs = data;
                    this.quizs.forEach(q => {
                        this.upquizData[q.id] = {
                            date_of_quiz: q.date_of_quiz,
                            time_duration: q.time_duration,
                            remarks: q.remarks
                        };
                    });

                } else {
                    this.quizs = [];
                    this.message = data.message || "No quizzes found";
                    
                }
            }
            )
        },
        openUpdateModal: function(q) {
            this.upquizData[q.id] = {
                date_of_quiz: q.date_of_quiz,
                time_duration: q.time_duration,
                remarks: q.remarks
            };
        },
        

        addQuiz : function(){
            console.log(this.quizForm,123456)
            const chap_id = this.$route.params.cid;
            
            fetch(`http://127.0.0.1:5000//api/quiz/create/${chap_id}`,  {
                method:"POST",
                headers :{
                    "Content-Type": "application/json",
                    "Authentication-Token" : localStorage.getItem("auth_token")
                },
                
                body : JSON.stringify(this.quizForm)
            })
            .then(response => response.json())
            .then(data =>{
                this.cmessage=data.message
                console.log(data)
                this.loadQuiz()
              
            })
            

        },
        quizDelete: function(id){
            fetch(`http://127.0.0.1:5000//api/quiz/delete/${id}`,{
                method:"DELETE",
                headers:{
                    "Content-Type":"application/json",
                    "Authentication-Token" : localStorage.getItem("auth_token")
                },
            })
            .then(response=> response.json())
            .then(data=> {this.message=data.message
                console.log(data.message)
                this.loadQuiz()

            })
        },
         updateQuiz: function(qid){
            const quiz_id = qid;
            console.log(this.upquizData[qid],123456),
           
            fetch(`http://127.0.0.1:5000/api/quiz/update/${quiz_id}`, {
                 method: "PUT",
                headers: {
                "Content-Type": "application/json",
                "Authentication-Token" : localStorage.getItem("auth_token")},
                
                 body: JSON.stringify(this.upquizData[qid]) 
            })
            .then(response => response.json())
            .then(data => {this.message=data.message
            console.log(data)
            console.log(this.upquizData,123456)
            this.loadQuiz()
            }
            )
        }

    }
}
</script>