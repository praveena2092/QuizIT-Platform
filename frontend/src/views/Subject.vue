<template>
  <div>
    <div class="row border" style="width:1220px">
      
      <div
        class="border"
        style="background-color: rgba(33,37,41, 0.03);width:1220px ;display: flex; align-items: center; justify-content: space-between;"
      >
        <div class="col-8 text-start">
          <h5 class="my-2">Welcome, {{ userData.username }} !</h5>
        </div>
        <div class="col text-end">
          <input
            type="text"
            v-model="search"
            class="form-control my-2"
            placeholder="Search Subjects"
          />
        </div>
      </div>

        
      <div
        class="col-8 border main"
        :style="{ height: '400px', overflowY: 'scroll', width: isUser ? '1220px' : '800px' }"
      >
        <h4 style="padding: 5px; display: block;">Subjects</h4>
        <p class="text-danger">{{ message }}</p>

        <div
          v-for="s in filteredSubjects"
          :key="s.id"
          class="card mt-2 mx-2"
        >
          <div class="card-body">
            <h5
              class="card-header title_sub"
              style="background-color: rgba(33,37,41, 0.03);width:700px ;padding:8px; justify-content: space-between;"
            >
              Subject name : {{ s.name }}
            </h5>
            <p>Description : {{ s.description }}</p>

           
            <button
              v-if="!isUser"
              @click="openUpdateModal(s)"
              class="btn user"
              data-bs-toggle="modal"
              :data-bs-target="'#modal-' + s.id"
              style="background-color: white; color: purple; border: 2px solid purple;"
            >
              Update
            </button>
            <button
              v-if="!isUser"
              class="btn btn-secondary mx-2 user"
              @click="subDelete(s.id)"
            >
              Delete
            </button>

            <router-link
              :to="{ name: 'addChapter', params: { sid: s.id } }"
              class="btn mx-2 lk"
              style="background-color: purple; color: white;"
            >
              {{ chapterButtonText }}
            </router-link>

            
            <div
              class="modal fade user"
              :id="'modal-' + s.id"
              tabindex="-1"
            >
              <div class="modal-dialog modal-fullscreen-lg-down">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title">Update Subject!....</h5>
                    <button
                      type="button"
                      class="btn-close"
                      data-bs-dismiss="modal"
                    ></button>
                  </div>
                  <div class="modal-body user">
                    <p class="text-danger">{{ message }}</p>
                    <div class="mb-3">
                      <label class="form-label">Enter Subject</label>
                      <input
                        type="text"
                        class="form-control"
                        v-model="upsubData[s.id].name"
                        :placeholder="s.name || 'Enter subject name'"
                      />
                    </div>
                    <div class="mb-3">
                      <label class="form-label">Enter Description</label>
                      <input
                        type="text"
                        class="form-control"
                        v-model="upsubData[s.id].description"
                        :placeholder="s.description || 'Enter description'"
                      />
                    </div>
                    <div class="mb-3">
                      <button
                        class="btn btn-primary"
                        @click="updateSubject(s.id)"
                        style="background-color: purple; color: white;"
                      >
                        Update
                      </button>
                    </div>
                    <div class="mb-3">
                      <router-link
                        class="btn"
                        to="/subject"
                        style="background-color: white; color: purple; border: 2px solid purple;"
                        >Go back</router-link
                      >
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
          </div>
        </div>
      </div>

      
      <div
        v-if="!isUser"
        class="col-4 border user"
        style="height:400px ;"
      >
        <div
          class="border user"
          style="background-color: rgba(33,37,41, 0.03) ;display: flex; align-items: center; justify-content: space-between;"
        >
          <h5 class="my-3">Create Subjects</h5>
        </div>
        <p class="text-danger">{{ cmessage }}</p>
        <div class="mb-3">
          <label class="form-label">Enter Subject</label>
          <input
            type="text"
            class="form-control"
            v-model="subData.name"
          />
        </div>
        <div class="mb-3">
          <label class="form-label">Enter Description</label>
          <input
            type="text"
            class="form-control"
            v-model="subData.description"
          />
        </div>
        <div class="mb-3">
          <button
            class="btn"
            @click="addSubject"
            style="background-color: white; color: purple; border: 2px solid purple;"
          >
            Add Subject
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      chapterButtonText: "Add Chapter",
      search: "",
      userData: {}, 
      isUser: false,
      subData: {
        name: "",
        description: ""
      },
      message: "",
      cmessage: "",
      subjects: [],
      upsubData: {}
    };
  },

  computed: {
    filteredSubjects() {
      return this.subjects.filter(s =>
        (s.name?.toLowerCase() || "").includes(
          this.search?.toLowerCase() || ""
        )
      );
    }
  },

  async mounted() {
    await this.loadUser();
    await this.loadSubjects();

    
    if (this.userData.roles?.[0] === "user") {
      this.isUser = true;
      this.chapterButtonText = "View Chapter";
    }
  },

  methods: {
    async loadUser() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/home", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.getItem("auth_token")
          }
        });
        this.userData = await response.json();
      } catch (error) {
        console.error("Error fetching user:", error);
      }
    },

    async loadSubjects() {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/api/subject/get",
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("auth_token")
            }
          }
        );
        const data = await response.json();
        if(!Array.isArray(data)) {
          this.subjects = [];
          this.message = "No subjects found.";
          return;
        }
        this.subjects = data;
        this.subjects.forEach(s => {
          this.upsubData[s.id] = {
            name: s.name,
            description: s.description

          };
        });
      } catch (error) {
        console.error("Error loading subjects:", error);
      }
    },

    openUpdateModal(subject) {
      if (!this.upsubData[subject.id]) {
        this.upsubData[subject.id] = {
          name: subject.name,
          description: subject.description
        };
      }
    },

    async addSubject() {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/api/subject/create",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("auth_token")
            },
            body: JSON.stringify(this.subData)
          }
        );
        const data = await response.json();
        this.cmessage = data.message;
        await this.loadSubjects();
      } catch (error) {
        console.error("Error adding subject:", error);
      }
    },

    async subDelete(id) {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/subject/delete/${id}`,
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("auth_token")
            }
          }
        );
        const data = await response.json();
        this.message = data.message;
        await this.loadSubjects();
      } catch (error) {
        console.error("Error deleting subject:", error);
      }
    },

    async updateSubject(id) {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/subject/update/${id}`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("auth_token")
            },
            body: JSON.stringify(this.upsubData[id]) 
          }
        );
        const data = await response.json();
        this.message = data.message;
        await this.loadSubjects();
      } catch (error) {
        console.error("Error updating subject:", error);
      }
    }
  }
};
</script>
