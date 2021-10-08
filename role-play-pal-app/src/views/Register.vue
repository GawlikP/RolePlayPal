<template>

  <div id="Register">
    <NavigationBar/>
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
            error: "",
        }
    }
})


</script>