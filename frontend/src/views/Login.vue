
    <template >
    <div class="row border">
    <div class="col-6" style="height:450px">
    <img src="../assets/p5.jpg" style = "width: 100%; height: 100%;"/>
    </div>
        <div class="col-6" style = "height: 430px ;">
            <div class="border mx-auto mt-5 " style="height: 300px ;border-radius:10px ; width: 330px">
                <div >
                    
                    <h2 class="text-center" style="font-weight:bold"> Login Form</h2>
                    <p class="mx-3 mt-2 text-danger">{{message}}</p>
                    <div class="mx-3 mb-3">
                        <label for="email" class="form-label">Enter Email address</label>
                        <input type="email" class="form-control" id="email" v-model="formData.email" placeholder="name@example.com">
                    </div>
                    <div class="mx-3 mb-3">
                        <label for="password" class="form-label">Enter Password</label>
                        <input type="password" class="form-control" id="password" v-model="formData.password">
                    </div>
                    
                   
                    <div class="text-center" >
                        <button class="btn"  style="background-color: purple; color: white;" @click="loginUser">Login</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
     <script>
     export default{
    data : function (){
        return {
            formData : {
                email :"",
                password :""
            },
            message:""
        }
    } ,
    methods:{
        
        loginUser : function(){
            console.log(this.formData)
            fetch("http://127.0.0.1:5000/api/login",{
                method:'POST',
                headers :{
                    "Content-Type": "application/json"
                },
                body : JSON.stringify(this.formData)
            })
            .then(response => response.json())
            .then(data => {
                console.log("Roles from backend:", data.roles, typeof data.roles);
                if(Object.keys(data).includes("auth_token")){
                    localStorage.setItem('auth_token',data["auth_token"])
                    localStorage.setItem("id",data["id"])
                    localStorage.setItem("username",data["username"])
                    localStorage.setItem("roles",data["roles"])
                    console.log(data.roles)
                    if (data.roles.includes("admin")){
                        this.$router.push("/admin")
                    }else{
                        this.$router.push("/user")
                    }
                    
                }
                else{
                    this.message=data.message
                }
            }) 
        }
    }
}

</script>