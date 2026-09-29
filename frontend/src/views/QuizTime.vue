<template>
    <div class="row border">
        <div class="col-8 border " style="height:430px; overflow-y:scroll; width :1230px">
        <h2>Question</h2>
        <p>{{message}}</p>
        <div v-for="q in question" :key="q.id" class="card mt-2">
            <div class="card-body">
                <p class="card-title">Question: {{q.question_statement}}</p>
                <select v-model="un" @change="recordAnswer(q)">
                <option :value="q.option_1">Option 1: {{ q.option_1 }}</option>
                <option :value="q.option_2">Option 2: {{ q.option_2 }}</option>
                <option :value="q.option_3">Option 3: {{ q.option_3 }}</option>
                <option :value="q.option_4">Option 4: {{ q.option_4 }}</option>
                </select> 
            </div>
            
        </div>
        <button class="btn btn-secondary" @click="endQuiz" >Delete</button> 
        </div>

       
   </div>
    
 </template>    
<script>
    export default{
    data :function(){
    return {
        questionForm :{
            question_statement:"",
            option_1 :"",
            option_2 :"",
            option_3 :"",
            option_4 :"",
            user_answer:""
        } ,
        
        user_answers : [],
        question :null,
        cmessage :'',
        message:'',
        un:""

    } 
    },

    mounted(){
         this.loadQuestion()
    },

    methods :{
       loadQuestion: function (){
            const quiz_id = this.$route.params.qid;
            
                           
            console.log(`/api/question/get/${quiz_id}` )
            fetch(`http://127.0.0.1:5000/api/question/get/${quiz_id}`,{ 
                method:"GET",
                headers :{
                    "Content-Type": "application/json",
                    "Authentication-Token" : localStorage.getItem("auth_token")
                }
            })
            .then(response => response.json())
            .then(data => {this.question=data
                
                console.log(data,"#########################")}
            )
        },
        endQuiz: function (){
            const quiz_id = this.$route.params.qid  
            console.log(localStorage.getItem("auth_token"))             
            console.log(`http://127.0.0.1:5000/api/up/${quiz_id}`)
            fetch(`http://127.0.0.1:5000/api/up/${quiz_id}`,{ 
                method:"POST",
                headers :{
                    "Content-Type": "application/json",
                    "Authentication-Token" : localStorage.getItem("auth_token")
                },
                body :JSON.stringify(this.user_answers)    
            })
            .then(response => response.json())
            .then(data => {this.question=data
                
                console.log(data)}
            )
        },
        
       
        recordAnswer(question) {
            
              const existing = this.user_answers.find(a => a.id === question.id);
              if (existing) {
                existing.answer = this.un;
              } else {
                this.user_answers.push({
                  id: question.id,
                  answer: this.un
                });
              }
             
            }
          
    


    }

}
</script>