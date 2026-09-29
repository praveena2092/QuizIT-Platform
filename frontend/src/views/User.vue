
    <template>
    <div style="height: 450px;">

        
            <!-- <div class="text-end my-2 " style="width:1230px">
                <button class="btn btn-secondary" @click="csvExport">Download CSV</button>
            </div>
        -->

          <div class="card my-2 mx-4 mx-auto"  style="width:1000px">
            <div class="card-header">
               <h5>View Subjects</h5>
            </div>
            <div class="card-body">
                <h5 class="card-title"> View Subjects </h5>
                <p class="card-text">View Subjects , Chapters , Quizzes and Take quiz</p>
                <router-link class="btn" style="background-color: purple; color: white;" to="/subject">View Subject</router-link>
            </div>
        </div>
         <div class="card my-2 mx-4 mx-auto"  style="width:1000px">
            <div class="card-header">
               <h5>View Quiz</h5>
            </div>
            <div class="card-body">
                <h5>  View  Scores</h5>
                <p class="card-text">View your past score and improve</p>
                <router-link class="btn" style="background-color: purple; color: white;" to="/score">View Score</router-link>
                 <!-- <router-link class="btn" style="background-color: purple; color: white;" to="/user/quiz">View Quizzzes</router-link> -->
            </div>
             
        </div>







   
    
     
    </div>
    </template> 
<!-- <script>
 export default{
 methods:{
    csvExport(){
        fetch("http://127.0.0.1:5000/api/export/user")
        .then(resopnse=>resopnse.json())
        .then(data=>{
            window.location.href=`http://127.0.0.1:5000/api/csv_result/user/${data.id}`
            
        })}
 }

}
</script> -->
