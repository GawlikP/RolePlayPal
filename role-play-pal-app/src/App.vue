<template>
  <div class="min-w-screen min-h-screen">
          <router-view/>
  </div>
</template>

<script>


export default({

  setup() {
    
  },
  beforeCreate(){
    this.$store.commit({type:'initializeStore'})
  }

})
</script>


<style lang="scss">
body {

}
</style>
