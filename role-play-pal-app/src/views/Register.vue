<template>

  <div id="Register">
        <div class="container  min-h-screen min-w-full items-center justify-center" >
            <NavigationBar/>
                <div class="grid grid-cols-3 gap-4 flex min-w-full my-8">
                <div></div>
                <div class="grid grid-cols-1 gap-4 flex min-w-full my-8 md:col-span-3 lg:col-span-1 col-span-3">
                <form @submit.prevent>
                    <div>  </div>
                    <div class="bg-5 rounded-2xl text-center items-center justify-center">
                        <p class="mt-2 text-center text-3xl font-bold text-gray">
                          Stwój nowe konto na naszym portalu
                        </p>
                    </div>
                    <div>
                        <div class="my-4 mx-2  rounded-xl bg-purple-900 items-center justify-center">
                        <div class="rounded-md shadow-md -space-y-px">    
                            <input type="text" name="username" autocomplete="username" v-model="username" v-bind:class="{'border-4 border-red-600 ': error['username'] !== undefined, ' border-1 border-purple-800 ': error['username'] === undefined }" class="appearance-none text-center rounded relative block w-full px-2 py-2  border  placeholder-gray-600 text-gray-900 focus:text-left focus:outline-none focus:ring-green-600 focus:border-green-600 focus:z-10 lg:text-3xl md:text-2xl sm:text-xl" placeholder="Nazwa użytkownika" /> 
                        </div>
                        </div>
                    </div>
                    <div>
                        <div class="my-4 mx-2  rounded-xl bg-purple-900 items-center justify-center">
                        <div class="rounded-md shadow-md -space-y-px">    
                            <input type="email" name="email" autocomplete="email" v-model="email" v-bind:class="{'border-4 border-red-600 ': error['email'] !== undefined, ' border-1 border-purple-800 ': error['email'] === undefined }" class="appearance-none text-center rounded relative block w-full px-2 py-2 border  placeholder-gray-600 text-gray-900 focus:text-left focus:outline-none focus:ring-green-600 focus:border-green-600 focus:z-10 lg:text-3xl md:text-2xl sm:text-xl" placeholder="Email" /> 
                        </div>
                        </div>
                    </div>
                    <div>
                        <div class="my-4 mx-2  rounded-xl bg-purple-900 items-center justify-center">
                        <div class="rounded-md shadow-md -space-y-px">    
                            <input type="password" name="password" autocomplete="password" v-model="password" v-bind:class="{'border-4 border-red-600 ': error['password'] !== undefined, ' border-1 border-purple-800 ': error['password'] === undefined }" class="appearance-none text-center rounded relative block w-full px-2 py-2 border  placeholder-gray-600 text-gray-900 focus:text-left  focus:outline-none focus:ring-green-600 focus:text-centered focus:border-green-600 focus:z-10 lg:text-3xl md:text-2xl sm:text-xl" placeholder="Hasło" /> 
                        </div>
                        </div>
                    </div>
                     <div>
                        <div class="my-4 mx-2  rounded-xl bg-purple-900 items-center justify-center">
                        <div class="rounded-md shadow-md -space-y-px">    
                            <input type="password" name="re-password" autocomplete="password" v-model="re_password" v-bind:class="{'border-4 border-red-600 ': error['re_password'] !== undefined, ' border-1 border-purple-800 ': error['re_password'] === undefined }" class="appearance-none text-center rounded relative block w-full px-2 py-2 border placeholder-gray-600 text-gray-900 focus:text-left  focus:outline-none focus:ring-green-600 focus:text-centered focus:border-green-600 focus:z-10 lg:text-3xl md:text-2xl sm:text-xl" placeholder="Powtórz hasło" /> 
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
                                <p class="text-bold text-3xl text-center ">   <i class="fas fa-id-badge"></i> </p>
                            </div>
                            <div>
                                <p class="text-bold text-3xl text-center "> <i class="fas fa-question-circle "></i>   </p>
                            </div>
                            </div>
                        </div>
                    </div>
                    <div class="flex iems-center justify-center min-w-full lg:my-1 sm:my-8">
                        <button type="submit" v-on:click="registerUser()" class="my-4 mx-4  sm:py-4  rounded-xl min-w-full bg-white border border-purple-800 boreder-1 items-center justify-center hover:bg-purple-900 hover:text-white lg:text-3xl sm:text-2xl font-bold shadow-md">  
                            <span type="text" name="email" class="" placeholder="Email" > Rejestruj </span> 
                        </button>
                    </div>
                     <div id="done" v-if="ok">
                        <div class="my-4 mx-2 bg-green-200 rounded-xl lg:my-4 sm:my-6">
                            <div class="rounded-md bg-green-200 shadow-md  -space-y-px ">
                               
                                <p class="text-bold text-4xl text-left font-bold text-center text-green-600 "><i class="fas fa-check-circle"></i> Udana rejestracja! Możesz już zalogować się do swojego konta!</p>
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
    name: 'Register',
    components: {
        NavigationBar
    },
    data(){
        return {
            username: "",
            password: "",
            email: "",
            re_password: "",
            error: {},
            errors_highlits: [],
            ok: false,
        }
    },
    methods: {
      registerUser(){
        this.error = {}
        if(this.username.length < 1) this.error['username'] = 'Proszę wypełnić to pole!';
        if(this.password.length < 1) this.error['password'] = 'Proszę wypełnić to pole!';
        if(this.re_password.length < 1) this.error['re_password'] = 'Proszę wypełnić to pole!';
        if(this.email.length < 1) this.error['email'] = 'Proszę wypełnić to pole!';
        if (Object.getOwnPropertyNames(this.error).length >0) return
        const requestOptions = {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({username: this.username, password: this.password, re_password: this.re_password, email: this.email})
            }
            fetch('http://localhost:8000/api/users/',requestOptions)
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
})


</script>