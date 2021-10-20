<template>
    <div id="PostReactionsComponent">
        <div v-if="my_reaction.id">
          <p class="text-center font-bold text-xl"  > 
            <i v-bind:class="{'text-red-700': !my_reaction.state,  'hover:text-red-700': my_reaction.state}"  class="fas fa-minus-square hover:text-red-700"></i>
            <i  v-bind:class="{'text-green-700': my_reaction.state,  'hover:text-green-700': !my_reaction.state}"   class="fas fa-plus-square hover:text-green-700"></i> 
           {{pluses - minuses}} </p>
        </div>
        <div v-else>
             <p class="text-center font-bold text-xl"  > <i v-on:click="addReaction(false)" class="fas fa-minus-square hover:text-red-700"></i> <i v-on:click="addReaction(true)" class="fas fa-plus-square hover:text-green-700"></i> {{pluses - minuses}} </p>
        </div>
    </div>
</template>

<script>
export default {
  name: 'PostReactionsComponent',
  props: {
      absolute_url: String,
      pluses: Number,
      minuses: Number
  },
  data() {
      return {
        reacted: -1,
        reactions: [],
        error: "",
        data: [],
        my_reaction: {},
      }
  },
  mounted(){
      this.getMyReaction()
  },
  methods: {
      getMyReaction(){
          const requestOptions = {
              method: "GET",
              headers: {"Content-Type":"application/json",
                        "Authorization": `Token ${this.$store.state.user.token}`}
          }
          fetch(`http://localhost:8000/api/posts${this.absolute_url}reactions/me/`, requestOptions)
          .then((res=>{
              if(res.status == 200) return res.json()
              else throw res
          }))
          .then((response =>{
     
              this.my_reaction = response;
              
          }))
          .catch(err=> {
              console.log(err)
          })
      },
      addReaction(type){
          const requestOptions = {
                method: "POST",
                headers: {
                    "Content-Type":"application/json",
                    "Authorization": `Token ${this.$store.state.user.token}`, 
                    },
                body: JSON.stringify({state: type})
              }
              fetch(`http://localhost:8000/api/posts${this.absolute_url}reactions/`, requestOptions)
              .then((res => {
                  if(res.status == 201) return res.json();
                  else throw res
              }))
              .then((res =>{
                 
                    this.my_reaction = res;
              }))
              .catch(err =>{
                  console.log(err)
              })
          }
      }
}

</script>