<template>
    <div id="PostFormComponent"> 
        <div class="container fluid mx-3 min-w-full min-h-5 shadow-md   border border-purple-700 rounded-xl ">
                <form @submit.prevent >
                <div v-on:click="changeFormDown()" >
                            <p  class=" font-bold lg:text-3xl md:text-xl sm:text-xl text-center   placeholder-gray-600 text-gray-900"> <i v-if="!isFormDown" class="fas fa-chevron-circle-down" ></i> <i v-if="isFormDown" class="fas fa-chevron-circle-up" ></i>  Dodaj nowy post </p>
                        </div> 
                    <div v-bind:class="{'hidden': !isFormDown, 'flex': isFormDown}"  class="grid grid-cols-1   min-w-full " >
                        
                        <div>
                            <div class=" mx-2  rounded-xl items-center justify-center">
                            <div class="rounded-md shadow-md -space-y-px my-1 lg:text-2xl md:text-xl sm:text-xl">    
                                <label for="title" class=" font-bold lg:text-2xl md:text-xl sm:text-xl text-center  block placeholder-gray-600 text-gray-900"> Tytuł</label>
                                <input type="text" name="title" autocomplete="title" v-model="post.title" class="appearance-none py-2 text-center rounded relative block w-full px-2  border border-purple-800 placeholder-gray-600 text-gray-900 focus:text-left focus:outline-none focus:ring-green-600 focus:border-green-600 focus:z-10 lg:text-2xl md:text-xl sm:text-xl" placeholder="Tytuł" /> 
                            </div>
                            </div>
                        </div>
                        <div>
                            <div class=" mx-2  rounded-xl items-center justify-center">
                            <div class="rounded-md shadow-md -space-y-px my-1">    
                                <label for="Content" class=" font-bold lg:text-3xl md:text-xl sm:text-xl text-center  block placeholder-gray-600 text-gray-900"> Tekst </label>
                                <textarea name="content" v-model="post.content" class="form-textarea mt-1 block w-full lg:text-2xl md:text-xl sm:text-md" rows="3" placeholder="Enter some long form content."></textarea>
                            </div>
                            </div>
                        </div>
                        <div class="mx-2  rounded-xl items-center justify-center py-2">
                            <select v-model="post.category" class="block appearance-none lg:text-2xl md:text-xl sm:text-xl  w-full bg-white border border-purple-400 hover:border-purple-800 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline">
                                    <option v-for="category in categories" v-bind:value="category.id" v-bind:key="category.id">
                                        {{ category.name }}
                                    </option>
                            </select>
                            
                        </div>
                        <div id="error message" v-if="error">
                        <div class="my-4 mx-2 bg-red-200 rounded-xl lg:my-4 sm:my-6">
                            <div class="rounded-md bg-red-200 shadow-md  -space-y-px ">
                               
                                <span class="text-bold lg:text-2xl md:text-xl sm:text-lg text-left font-bold text-red-600 "><div v-for="(value, name) in error" :key="name">
                                    <i class="fas fa-exclamation-circle"></i> {{name}} : {{value}}<br> 
                                    </div>
                                 
                                 </span>
                            </div>
                        </div>
                    </div>
                        <div class="flex iems-center justify-center min-w-full lg:my-1 sm:my-8">
                            <button type="submit" v-on:click="addPost()" class="my-4 mx-4  sm:py-4  rounded-xl min-w-full bg-white border border-purple-800 boreder-1 items-center justify-center bg-purple-800  text-gray-200 hover:bg-purple-600 lg:text-2xl sm:text-xl font-bold shadow-md">  
                                <span type="text"  > Dodaj Post </span> 
                            </button>
                        </div>
                        <div id="done" v-if="ok">
                        <div class="my-4 mx-2 bg-green-200 rounded-xl lg:my-4 sm:my-6">
                            <div class="rounded-md bg-green-200 shadow-md  -space-y-px ">
                               
                                <p class="text-bold lg:text-2xl md:text-xl sm:text-lg text-left font-bold text-center text-green-600 "><i class="fas fa-check-circle"></i> Dodano twój post!</p>
                            </div>
                        </div>
                    </div>
                    </div>
                </form>
        </div>
    </div>
</template>

<script>
export default {
  name: 'PostFormComponent',
  data ()  {
      return {
        isFormDown: false,
        post: {
            title: '',
            content: '',
            category: 0,
        },
        categories: [],
        error: '',
        ok: false,
      }
  },
   mounted(){
        this.getCategories()
    },
  methods: {
      changeFormDown(){
          this.isFormDown = !this.isFormDown;
      },
      getCategories(){
          const requestOptions = {
                method: "GET",
                headers: {"Content-Type": "application/json", "Authorization": `Token ${this.$store.state.user.token}`},
            }
            fetch('http://localhost:8000/api/posts/categories/',requestOptions)
            .then((res => {
                if(res.status == 200){
                    return res.json()
                }else {
                   throw res
                }
            }
            ))
            .then((response => {
                    console.log(response);
                    this.categories = response;
            }))
            .catch(err => {
                
                err.json().then(json => {
                    this.error = json
                });
            })
      },
      addPost(){
           this.error = {}
           this.ok = false
        if(this.post.title.length < 1) this.error['title'] = 'Proszę wypełnić to pole!';
        if(this.post.content.length < 1) this.error['content'] = 'Proszę wypełnić to pole!';
        if(this.post.category < 1) this.error['category'] = 'Proszę wypełnić to pole!';
         
        if (Object.getOwnPropertyNames(this.error).length >0) return

          const requestOptions = {
                method: "POST",
                headers: {"Content-Type": "application/json", "Authorization": `Token ${this.$store.state.user.token}`},
                body: JSON.stringify({title: this.post.title, content: this.post.content, category: this.post.category})
            }
            fetch('http://localhost:8000/api/posts/',requestOptions)
            .then((res => {
                if(res.status == 201){
                    return res.json()
                }else {
                   throw res
                }
            }
            ))
            .then((response => {
                    console.log(response);
                    this.ok = true;
            }))
            .catch(err => {
                
                err.json().then(json => {
                    this.error = json
                });
            })
      }
  }
}
</script>