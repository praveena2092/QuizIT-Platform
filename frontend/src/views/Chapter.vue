<template>
    <div class="row border">
          <div class="border " style="background-color: rgba(33,37,41, 0.03);width:1250px ;display: flex; align-items: center; justify-content: space-between;">
                 <div class="col-8 text-start">
                    <h4 class="my-2"> Chapter!</h4>
                </div>
                <div class="col text-end">
                     <input type="text" v-model="search" class="form-control my-2 border" placeholder="Search Chapters"  >
                </div>
            </div>
        <div class="col-8 border mx-2 main"style="height:400px; width:800px;overflow-y:scroll">
        <p>{{message}}</p>
        <div v-for="c in filteredChapters"  :key="c.id" class="card mt-2" >
            <div class="card-body">
                <h5 class="card-header" style="background-color: rgba(33,37,41, 0.03);width:700px ;padding:8px; justify-content: space-between;">Chapter name : {{c.name}}</h5>
                <p> Description : {{c.description}}</p>
                <button @click="openUpdateModal(c)" v-show="userRole!== 'user'" class="btn mx-2" data-bs-toggle="modal" :data-bs-target="'#modal-' + c.id"  style="background-color: white; color: purple; border: 2px solid purple;">
                Update
                </button>
                <button v-show="userRole!== 'user'" class="btn btn-secondary mx-2" @click=" chapDelete(c.id)">Delete</button>
                <router-link :to="{name :'addQuiz',params:{cid :c.id}}" class="btn mx-2" style="background-color: purple; color: white;"  v-show="userRole!== 'user'" >{{QuizButton }}</router-link>
                  <router-link class="btn" style="background-color: purple; color: white;" :to="{name :'UserQuiz',params:{id :c.id}}"  v-show="userRole=== 'user'">View Quiz123</router-link>
            </div>
            <div class="modal fade" :id="'modal-' + c.id" tabindex="-1">
            <div class="modal-dialog modal-fullscreen-lg-down">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Update the Chapter!.....</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p class="text-danger">{{message}}</p>
                        <div class="mb-3">
                            <label for="chapName" class="form-label">Enter Chapter</label>
                            <input type="email" class="form-control" v-model="upChapData[c.id].name" :placeholder="c.name ? c.name : 'Enter chapter name'" id="subName" >
                        </div>
                        <div class="mb-3">
                            <label for="description" class="form-label">Enter Description</label>
                            <input type="email" class="form-control" v-model="upChapData[c.id].description" id="description" :placeholder="c.description ? c.description : 'Enter description'"  >
                        </div>
                        <div class="mb-3">
                            <button class="btn btn-primary" @click="updateChapter(c.id,c.s_id)" style="background-color: purple; color: white;" >Update</button>
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
        <div class="col-4 border" v-show="userRole!== 'user'">
            <h2>Add Chapter</h2>
            <div class="mb-3">
                <label for="chapName" class="form-label">Chapter Name</label>
                <input type="email" class="form-control" id="chapName" v-model="chapForm.name" >
            </div>
            <div class="mb-3">
                <label for="chapDescription" class="form-label">Description</label>
                <textarea class="form-control" id="chapDescription" rows="3" v-model="chapForm.description"></textarea>
            </div>
            <div class="mb-3">
                <button class="btn link" style="background-color: purple; color: white;" @click="addChapters">Add Chapter</button>
            </div>

        </div>
        
       

   </div>
    </template>
<script>
    export default{
    data :function(){
    return {
        userRole: localStorage.getItem("roles"),
        QuizButton : "Add Quiz",
        
        search: '',
        chapForm :{
            name:"",
            description :" "
        } ,
        chapters :[],
        cmessage :'',
        message:'',
        upChapData: {},
        sub_id:"",
        

    }
    },
    computed: {
         filteredChapters() {
            return this.chapters.filter(c =>
            (c.name?.toLowerCase() || '').includes(
                this.search?.toLowerCase() || ''
            )
            );
        }
    },

    mounted(){
        this.userRole = localStorage.getItem("roles");
         this.loadChapter()
        if(this.userRole === "user") {
            this.QuizButton = "View Quiz";
            
            document.querySelector(".main").style.width = "1220px";
            
        }
    },

    methods :{
        loadChapter: function (){
            const sub_id = this.$route.params.sid;
                           
            console.log(`http://127.0.0.1:5000/api/chapter/get/${sub_id}` )
            fetch(`http://127.0.0.1:5000/api/chapter/get/${sub_id}`,{ 
                method:"GET",
                headers :{
                    "Content-Type": "application/json",
                    "Authentication-Token" : localStorage.getItem("auth_token")
                }
            })
            .then(response => response.json())
            .then(data => {this.chapters=data
                console.log(data)
                if (!Array.isArray(data)) {
                    this.chapters = [];
                    this.message = "No chapters found.";
                    return;
                }
                this.chapters = data;
                this.chapters.forEach(c => {
                    this.upChapData[c.id] = {
                        name: c.name,
                        description: c.description
                    };
        });}
            )
        },
           openUpdateModal(chapter) {
                if (!this.upChapData[chapter.id]) {
                    this.upChapData[chapter.id] = {
                    name: chapter.name,
                    description: chapter.description
                    };
                }
                },
        addChapters : function(){
            console.log(this.chapForm,123456)
            const sub_id = this.$route.params.sid;

            console.log(`http://127.0.0.1:5000/api/chapter/get/${sub_id}` )/
            fetch(`http://127.0.0.1:5000/api/chapter/create/${sub_id}`,  {
                method:"POST",
                headers :{
                    "Content-Type": "application/json",
                    "Authentication-Token" : localStorage.getItem("auth_token")
                },
                
                body : JSON.stringify(this.chapForm)
            })
            .then(response => response.json())
            .then(data =>{
                this.cmessage=data.message
                console.log(data)
                this.loadChapter()
              
            })
            

        },
        chapDelete: function(id){
            fetch(`http://127.0.0.1:5000/api/chapter/delete/${id}`,{
                method:"DELETE",
                headers:{
                    "Content-Type":"application/json",
                    "Authentication-Token" : localStorage.getItem("auth_token")
                },
            })
            .then(response=> response.json())
            .then(data=> {this.message=data.message
                console.log(data.message)
                this.loadChapter()

            })
        },
        updateChapter: function(cid,sid){
            const sub_id =sid
            const chap_id =cid
            console.log(this.sub_id,123456)
            console.log(`http://127.0.0.1:5000/api/chapter/update/${chap_id}` )
            fetch(`http://127.0.0.1:5000/api/chapter/update/${chap_id}`, {
                method: "PUT",
                headers: {
                "Content-Type": "application/json",
                "Authentication-Token" : localStorage.getItem("auth_token")},
                
                 body: JSON.stringify(this.upChapData[cid]) 
            })
            .then(response => response.json())
            .then(data => {this.message=data.message
               console.log(data)
               this.loadChapter()
            }
            )
        }


    }

}
</script>

