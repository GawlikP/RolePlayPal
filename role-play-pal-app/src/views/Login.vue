<template>
    <div id="Login">
        <div class="container  min-h-screen min-w-full items-center justify-center" >
            <NavigationBar/>
                <div class="grid grid-cols-3 gap-4 flex min-w-full my-8">
                <div></div>
                <div class="grid grid-cols-1 gap-4 flex min-w-full my-8 md:col-span-1 lg:col-span-1 col-span-3">
                <form @submit.prevent>
                    <div>  </div>
                    <div class="bg-5 rounded-2xl text-center items-center justify-center">
                        <p class="mt-2 text-center text-3xl font-bold text-gray">
                            Zaloguj się
                        </p>
                    </div>
                    <div>
                        <div class="my-4 mx-2  rounded-xl bg-purple-900 items-center justify-center">
                        <div class="rounded-md shadow-md -space-y-px">    
                            <input type="text" name="username" autocomplete="username" v-model="username" class="appearance-none text-center rounded relative block w-full px-2 py-2 border border-purple-800 placeholder-gray-600 text-gray-900 focus:text-left focus:outline-none focus:ring-green-600 focus:border-green-600 focus:z-10 lg:text-3xl md:text-2xl sm:text-xl" placeholder="Nazwa użytkownika" /> 
                        </div>
                        </div>
                    </div>
                    <div>
                        <div class="my-4 mx-2  rounded-xl bg-purple-900 items-center justify-center">
                        <div class="rounded-md shadow-md -space-y-px">    
                            <input type="password" name="password" autocomplete="password" v-model="password" class="appearance-none text-center rounded relative block w-full px-2 py-2 border border-purple-800 placeholder-gray-600 text-gray-900 focus:text-left  focus:outline-none focus:ring-green-600 focus:text-centered focus:border-green-600 focus:z-10 lg:text-3xl md:text-2xl sm:text-xl" placeholder="Hasło" /> 
                        </div>
                        </div>
                    </div>
                    <div id="error message" v-if="error">
                        <div class="my-4 mx-2 bg-red-200 rounded-xl lg:my-4 sm:my-6">
                            <div class="rounded-md bg-red-200 shadow-md  -space-y-px ">
                               
                                <span class="text-bold text-3xl text-left font-bold text-red-600 "><div v-for="(value, name) in error" :key="name">
                                    <i class="fas fa-exclamation-circle"></i> {{name}} : {{value}}<br> 
                                    </div>
                                 
                                 </span>
                            </div>
                        </div>
                    </div>
                    <div>
                        <div class="my-4 mx-2  rounded-xl lg:my-4 sm:my-6">
                            <div class="rounded-md grid grid-cols-2 gap-4 shadow-md text-center -space-y-px ">
                            <div>    
                                <p class="text-bold text-3xl text-center ">   <i class="far fa-user-circle"></i> </p>
                            </div>
                            <div>
                                <p class="text-bold text-3xl text-center "> <i class="fas fa-question-circle "></i>   </p>
                            </div>
                            </div>
                        </div>
                    </div>
                    <div class="flex items-center justify-center min-w-full lg:my-1 sm:my-8">
                        <button type="submit" v-on:click="logIn()" class="my-4 mx-4  sm:py-4  rounded-xl min-w-full bg-white border border-purple-800 boreder-1 items-center justify-center hover:bg-purple-900 hover:text-white lg:text-3xl sm:text-2xl font-bold shadow-md">  
                            <span type="text" name="email" class="" placeholder="Email" > Zaloguj </span> 
                        </button>
                    </div>
                     <div id="done" v-if="ok">
                        <div class="my-4 mx-2 bg-green-200 rounded-xl lg:my-4 sm:my-6">
                            <div class="rounded-md bg-green-200 shadow-md  -space-y-px ">
                               
                                <p class="text-bold text-4xl text-left font-bold text-center text-green-600 "><i class="fas fa-check-circle"></i> Udało się poprawnie zalogować</p>
                            </div>
                        </div>
                    </div>
                        </form>
                </div>
                
                <div></div>
                    
                </div>
        
        </div>
    </div>
</template>

<script>
import NavigationBar from '@/components/NavigationBar.vue'

export default({
    name: 'Login',
    components: {
        NavigationBar
    },
    data(){
        return {
            email: "",
            username: "",
            password: "",
            error: "",
            ok: false, 
        }
    },
    methods: {
        logIn: function(){
            this.error = "";
            this.ok = false;
            const requestOptions = {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({username: this.username, password: this.password})
            }
            fetch('http://localhost:8000/api/token/login',requestOptions)
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
                    this.ok = true;
                    this.$store.commit({type:'logUser', token:response['auth_token'], username:this.username})
            }))
            .catch(err => {
                
                err.json().then(json => {
                    this.error = json
                });
            })


            //this.$store.commit({type: 'logUser', token: this.token, username: this.username})
        }
    }
})

</script>