<template>
    <div>
     <h4>Welcome, {{userData.username}} !</h4>
        <div class="row border ">
            <div class="col" style = " height: 410px ; overflow-y:scroll;width: 1000px;">
                <h2>Subjects</h2>
                <p class="text-danger">{{message}}</p>
                <div v-for="q in quiz" class="card mt-2" style="width: 1200px;">
                    <div class="card-body">
                        <h5 class="card-title">{{q.date_of_quiz}}</h5>
                        <p>Time duartion: {{q.time_duration}}</p>
                        <p>Remarks: {{q.remarks}}</p>
                        <p>Chapter :{{q.chapter}}</p>
                        <p>Chapter :{{q.chap_description}}</p>
                        <p>sub_name :{{q.sub_name}}</p>
                        <p>sub_description :{{q.sub_description}}</p>
                        
                        <!-- <router-link :to="{name :'quiztime',params:{qid :q.id}}" class="btn btn-secondary" >Start quiz</router-link>  -->
                        <router-link :to="{name :'quiz123',params:{qid :q.id}}" class="btn btn-secondary" >Start Quiz</router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template> 
<script>
    export default{
    data:function(){
        return {
            userData : " ",
            quiz:null ,
            message:""
        }
    },
    methods :{

    },
    mounted(){
        fetch("http://127.0.0.1:5000/api/home", {
            method:"GET",
            headers :{
                "Content-Type": "application/json",
                "Authentication-Token" : localStorage.getItem("auth_token")
            }
        })
        .then(response => response.json())
            .then(data => this.userData=data)
        const id = this.$route.params.id;       
        fetch(`http://127.0.0.1:5000/api/user/quiz/get/${id}`,  {
            method:"GET",
            headers :{
                "Content-Type": "application/json",
                "Authentication-Token" : localStorage.getItem("auth_token")
            }
        })
        .then(response => response.json())
        .then(data => this.quiz=data)
               
            
         
    }
}
</script>