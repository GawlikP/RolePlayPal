<template>
    <div id="Login">
        <div class="container  min-h-screen min-w-full items-center justify-center" >
            <NavigationBar/>
                <div class="grid grid-cols-3 gap-4 flex min-w-full my-8">
                <div></div>
                <div class="grid grid-cols-1 gap-4 flex min-w-full my-8 md:col-span-3 lg:col-span-1 col-span-3">
                    <div>  </div>
                    <div class="bg-5 rounded-2xl text-center items-center justify-center">
                        <p class="mt-2 text-center text-3xl font-bold text-gray">
                            Login 
                        </p>
                    </div>
                    <div>
                        <div class="my-4 mx-2  rounded-xl bg-purple-900 items-center justify-center">
                        <div class="rounded-md shadow-md -space-y-px">    
                            <input type="text" name="email" autocomplete="email" class="appearance-none text-center rounded relative block w-full px-2 py-2 border border-purple-800 placeholder-gray-600 text-gray-900 focus:text-left focus:outline-none focus:ring-green-600 focus:border-green-600 focus:z-10 lg:text-3xl md:text-2xl sm:text-xl" placeholder="Email" /> 
                        </div>
                        </div>
                    </div>
                    <div>
                        <div class="my-4 mx-2  rounded-xl bg-purple-900 items-center justify-center">
                        <div class="rounded-md shadow-md -space-y-px">    
                            <input type="password" name="password" autocomplete="password" class="appearance-none text-center rounded relative block w-full px-2 py-2 border border-purple-800 placeholder-gray-600 text-gray-900 focus:text-left  focus:outline-none focus:ring-green-600 focus:text-centered focus:border-green-600 focus:z-10 lg:text-3xl md:text-2xl sm:text-xl" placeholder="Passoword" /> 
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
                    <div class="flex iems-center justify-center min-w-full lg:my-1 sm:my-8">
                        <button class="my-4 mx-4  sm:py-4  rounded-xl min-w-full bg-white border border-purple-800 boreder-1 items-center justify-center hover:bg-purple-900 hover:text-white lg:text-3xl sm:text-2xl font-bold shadow-md">  
                            <span type="text" name="email" class="" placeholder="Email" > Login </span> 
                        </button>
                    </div>
                        
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
            username: "",
            password: "",
            error: "",
        }
    }
})

</script>