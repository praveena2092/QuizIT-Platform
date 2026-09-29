 <template>
    <div class="row border" style="height: 450px" >
        <div class="col-6">
            <img src="../assets/p5.jpg" style = "width: 660px; height: 440px;"/>
        
        </div>
        <div class="col-6" style = "height: 450px ;">
            <div class="border mx-auto mt-5 " style="height: 400px ;border-radius:10px ; width: 330px;overflow-y:scroll">
                <div>
                    <h2 class="text-center" style="font-weight:bold"> Register Form</h2>
                    <p class="mx-2 mb-3 text-danger">{{message}}</p>
                    <div class="mx-2 mb-3">
                        <label for="email" class="form-label">Enter Email address</label>
                        <input type="email" class="form-control" id="email" v-model="formData.email" placeholder="name@example.com">
                    </div>
                    <div class="mx-2 mb-3">
                        <label for="username" class="form-label">Enter User name</label>
                        <input type="text" class="form-control" id="username" v-model="formData.username" >
                    </div>
                   
                    <div class="mx-2 mb-3">
                        <label for="dob" class="form-label">Enter Date of Birth</label>
                        <input type="date" class="form-control" id="dob" v-model="formData.dob" >
                    </div>
                    <div class="mx-2 mb-3">
                        <label for="password" class="form-label">Enter Password</label>
                        <input type="password" class="form-control" id="password" v-model="formData.password" >
                    </div>
                    
                    <div class="text-center">
                        <button class="btn"  style="background-color: purple; color: white;" @click="addUser" >Register</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  <script>
  export default {
      data : function (){
        return {
            formData : {
                email :"",
                password :"",
                username :"",
                dob :""
            },
            message:" "
        }
    } ,
     methods:{
        
        addUser : function(){
            console.log(this.formData)
            fetch("http://127.0.0.1:5000/api/register",{
                method:'POST',
                headers :{
                    "Content-Type": "application/json"
                },
                body : JSON.stringify(this.formData)
            })
            .then(response => response.json())
            .then(data =>{
                
                if(Object.keys(data).includes("email")){
                    this.userData=data
                    this.$router.push("/user")
                    
                }
                else{
                    this.message=data.message
                }
            })
            .catch(error=> this.message=error.message)
        
        }
    }
}
</script>