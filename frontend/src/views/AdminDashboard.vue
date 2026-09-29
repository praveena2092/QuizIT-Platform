
    <template>

    <div style="height:450px">
        <div class="row border">
            <div class="text-end my-2 " style="width:1230px">
                <button class="btn btn-secondary" @click="csvExport">Download CSV</button>
            </div>
        </div>
        <div class="card my-2 mx-4 mx-auto"  style="width:1000px">
            <div class="card-header">
               <h5>View Subjects</h5>
            </div>
            <div class="card-body">
                <h5 class="card-title">Subjects </h5>
                <p class="card-text">Add, View, Delete, Update Subjects and Create a new Chapter</p>
                <router-link class="btn" style="background-color: purple; color: white;" to="/subject">View Subject</router-link>
            </div>
        </div>
        <div class="card my-2 mx-4 mx-auto" style="width:1000px">
            <div class="card-header">
               <h5> Summary</h5>
            </div>
            <div class="card-body">
                <h5 class="card-title">View Summary</h5>
                <p class="card-text">View and Explore the dashboard and visualize</p>
                <router-link class="btn" style="background-color: purple; color: white;" to="/admin/chart">View Summary</router-link>
            </div>
        </div>
    </div>
    </template>
<script>
 export default{
 methods:{
    csvExport(){
        fetch("http://127.0.0.1:5000/api/export")
        .then(resopnse=>resopnse.json())
        .then(data=>{
            window.location.href=`http://127.0.0.1:5000/api/csv_result/${data.id}`
            
        })}
 }

}
</script>
