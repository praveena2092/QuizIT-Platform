<template>
    
        <div class="row ">
             <div class="border" style="background-color: rgba(33,37,41, 0.03);width:1250px ;display: flex; align-items: center; justify-content: space-between;">
                 <div class="col-8 text-start">
                    <h4 class="my-2"> Question!</h4>
                </div>
                <div class="col text-end">
                     <input type="text" v-model="search" class="form-control mx-2 border" placeholder="Search Questions"  >
                </div>
            </div>
        <div class="col-8 border " style="height:400px; overflow-y:scroll">
       
        <p>{{message}}</p>  
        <div v-for="q in filteredQuestions" :key="q.id" class="card mt-2 mx-2">
            <div class="card-body">
                 <h5 class="card-header" style="background-color: rgba(33,37,41, 0.03);width:750px ;padding:8px; justify-content: space-between;">Question: {{q.question_statement}}</h5>
          
                <p class="card-title"> Option1 :{{q.option_1}}</p>
                <p class="card-title"> Option2 :{{q.option_2}}</p>
                <p class="card-title"> Option3 :{{q.option_3}}</p>
                <p class="card-title"> Option4 :{{q.option_4}}</p>
                <p class="card-title"> Correct_answer :{{q.correct_answer}}</p>
                <button  @click="openUpdateModal(q)" class="btn mx-2" data-bs-toggle="modal"  :data-bs-target="'#modal-' + q.id"   style="background-color: white; color: purple; border: 2px solid purple;">
                Update
                </button>
                <button class="btn btn-secondary mx-2" @click=" questionDelete(q.id)">Delete</button>
            </div>
            <!-- Modal definition -->
            <div class="modal fade" :id="'modal-' + q.id" tabindex="-1">
            <div class="modal-dialog modal-fullscreen-lg-down">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Update Question...</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                      <div class="row border"  style="height:400px; overflow-y:scroll">
        
                  <div class="col-10 text-center mt-3 my-3 " style ="width:50%; margin :auto; height: 350px ;width: 300px ; ">
                   <h4>Update the question!</h4>
                   <p class="text-danger">{{message}}</p>
                   <h2>Add Question</h2>
                    <div class="mb-3">
                        <label for="question_statement" class="form-label">Question Statement</label>
                        <input type="email" class="form-control" id="question_statement" v-model="questionForm[q.id].question_statement" :placeholder="q.question_statement ? q.question_statement : 'Enter Question'">
                    </div>
                    <div class="mb-3 d-flex">
                        <label for="op1" class="form-label">Enter option 1</label>
                        <input class="form-control" id="op1" rows="3" v-model="questionForm[q.id].option_1" :placeholder="q.option_1 ? q.option_1 : 'Enter option 1'"></input>
                    </div>
                    <div class="mb-3 d-flex">
                        <label for="op2" class="form-label">Enter Option 2</label>
                        <input class="form-control" id="op2" rows="3" v-model="questionForm[q.id].option_2" :placeholder="q.option_2 ? q.option_2 : 'Enter option 2'"></input>
                    </div>
                    <div class="mb-3 d-flex">
                        <label for="op3" class="form-label">Enter Option 3</label>
                        <input class="form-control" id="op3" rows="3" v-model="questionForm[q.id].option_3" :placeholder="q.option_3 ? q.option_3 : 'Enter option 3'"></input>
                    </div>
                    <div class="mb-3 d-flex">
                        <label for="op4" class="form-label">Enter Option 4</label>
                        <input class="form-control" id="op4" rows="3" v-model="questionForm[q.id].option_4" :placeholder="q.option_1 ? q.option_4 : 'Enter option 4'"></input>
                    </div>
                    <div class="mb-3 d-flex">
                        <label for="ca" class="form-label">Correct Answer</label>
                        <input class="form-control" id="ca" rows="3" v-model="questionForm[q.id].correct_answer" :placeholder="q.correct_answer ? q.correct_answer : 'Enter Correct answer'"/>
                    </div>
                    
                    <div class="mb-3">
                        <button class="btn btn-primary" @click="updateQuestion(q.id)" style="background-color: purple; color: white;" >Update</button>
                    </div>
                    <div class="mb-3">
                         <router-link class="btn"  to="/subject" style="background-color: white; color: purple; border: 2px solid purple;">Go back</router-link>
                    </div>
                    </div>
           
        </div>
                </div>
                </div>
            </div>
            </div>


        </div>
        </div>
        <div class="col-4 border" style = "height: 400px;width: 380px; overflow-y:scroll">
            <h2>Add Question</h2>
            <div class="mb-3">
                <label for="question_statement" class="form-label">Question Statement</label>
                <input type="email" class="form-control" id="question_statement" v-model="questionForm.question_statement" >
            </div>
            <div class="mb-3 d-flex">
                <label for="op1" class="form-label">Enter option 1</label>
                <input class="form-control" id="op1" rows="3" v-model="questionForm.option_1"></input>
            </div>
             <div class="mb-3 d-flex">
                <label for="op2" class="form-label">Enter Option 2</label>
                <input class="form-control" id="op2" rows="3" v-model="questionForm.option_2"></input>
            </div>
             <div class="mb-3 d-flex">
                <label for="op3" class="form-label">Enter Option 3</label>
                <input class="form-control" id="op3" rows="3" v-model="questionForm.option_3"></input>
            </div>
            <div class="mb-3 d-flex">
                <label for="op4" class="form-label">Enter Option 4</label>
                <input class="form-control" id="op4" rows="3" v-model="questionForm.option_4"></input>
            </div>
            <div class="mb-3 d-flex">
                <label for="ca" class="form-label">Correct Answer</label>
                <input class="form-control" id="ca" rows="3" v-model="questionForm.correct_answer"/>
            </div>
            <div class="mb-3">
                <button class="btn" style="background-color: purple; color: white;" @click="addQuestion">Add Question</button>
            </div>
        </div>
   </div>
</template>
<script>
    export default{
    data :function(){
    return {
        search: '',
        questionForm :{} ,
        questions :[],
        cmessage :'',
        message:''

    }
    },

    mounted(){
         this.loadQuestion()
    },
    computed: {
        filteredQuestions() {
            return this.questions.filter(q =>
            (q.question_statement?.toLowerCase() || '').includes(
                this.search?.toLowerCase() || ''
            )
            );
           
        }
    },

    methods :{
        loadQuestion: function (){
            const ques_id = this.$route.params.qid;
                           
            console.log(`"http://127.0.0.1:5000//api/question/get/${ques_id}` )
            fetch(`http://127.0.0.1:5000//api/question/get/${ques_id}`,{ 
                method:"GET",
                headers :{
                    "Content-Type": "application/json",
                    "Authentication-Token" : localStorage.getItem("auth_token")
                }
            })
            .then(response => response.json())
            .then(data => {this.question=data
                console.log(data)
                if (Array.isArray(data)) {
                    this.questions = data;
                    } else {
                    this.questions = [];
                    this.message = data.message || "No questions found";
                    }
        

                this.questions.forEach(q => {
                    this.questionForm[q.id] = {
                        question_statement: q.question_statement,
                        option_1: q.option_1,
                        option_2: q.option_2,
                        option_3: q.option_3,
                        option_4: q.option_4,
                        correct_answer: q.correct_answer
                    };
                });
            }
            )
        },
        openUpdateModal(question) {
            if (!this.questionForm[question.id]) {
                this.questionForm[question.id] = {
                    question_statement: question.question_statement,
                    option_1: question.option_1,
                    option_2: question.option_2,
                    option_3: question.option_3,
                    option_4: question.option_4,
                    correct_answer: question.correct_answer
                };
            }
        },
        addQuestion : function(){
            console.log(this.questionForm,123456)
            const ques_id = this.$route.params.qid;
            
            fetch(`http://127.0.0.1:5000//api/question/create/${ques_id}`,  {
                method:"POST",
                headers :{
                    "Content-Type": "application/json",
                    "Authentication-Token" : localStorage.getItem("auth_token")
                },
                
                body : JSON.stringify(this.questionForm)
            })
            .then(response => response.json())
            .then(data =>{
                this.cmessage=data.message
                console.log(data)
                this.loadQuestion()
              
            })
            

        },
        questionDelete: function(id){
            console.log(id,77777)
            fetch(`http://127.0.0.1:5000//api/question/delete/${id}`,{
                method:"DELETE",
                headers:{
                    "Content-Type":"application/json",
                    "Authentication-Token" : localStorage.getItem("auth_token")
                },
            })
            .then(response=> response.json())
            .then(data=> {this.message=data.message
                console.log(data.message)
                this.loadQuestion()

            })
        },
        updateQuestion: function(qid){
            const ques_id = qid;
            
           
            fetch(`http://127.0.0.1:5000//api/question/update/${ques_id}`, {
                method: "PUT",
                headers: {
                "Content-Type": "application/json",
                "Authentication-Token" : localStorage.getItem("auth_token")},
                body: JSON.stringify(this.questionForm[qid])
            })
            .then(response => response.json())
            .then(data => {this.message=data.message
               console.log(data)
               this.loadQuestion()
               
            }
            )
        }


    }

}
</script>