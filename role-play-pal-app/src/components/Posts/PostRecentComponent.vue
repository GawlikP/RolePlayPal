<template>
<div id="PostRecent" >
    <div  v-if="error.length < 1"  >
        <div id="rows" v-for="(post, index) in posts" v-bind:key="index" class="grid grid-cols-5 gap-2 py-1 flex min-w-full my-1">
            <div div="my-1"></div> 
                <div class="min-w-full col-span-5  my-1 xl:col-span-3 lg:col-span-3 md:col-span-5 sm:col-span-5">
                <PostViewComponent v-bind:id="post.id" v-bind:title="post.title" v-bind:content="post.content" v-bind:pluses="post.pluses" v-bind:minuses="post.minuses" v-bind:author="post.author" v-bind:author_username="post.author_username" v-bind:absolute_url="post.get_absolute_url"/>
                </div>
            <div class="my-1" ></div>
        </div>
    </div>
    <div v-if="error.length > 0">
        <div class="min-w-full my-1  xl:col-span-3 lg:col-span-3 md:col-span-5 sm:col-span-5 ">
             <div class="container fluid mx-3 min-w-full min-h-10 px-2 py-2 items-center justify-center shadow-md text-3xl font-bold  border border-gray-600 rounded-xl ">
                <p class="text-center">COS POSZLO NIE TAK </p>
            </div>
        </div>
    </div>
</div>
</template>
<script>

import PostViewComponent from '@/components/Posts/PostViewComponent.vue'
export default {
  name: 'PostRecentComponent',
  data(){
        return {
            posts_ids:[2,3,4,7],
            posts: [
                ],
            ok: false, 
            error: "",
        }
    },
    mounted(){
        this.getPosts()
    },
    methods :{
            getPosts: function(){
                this.error = "";
                this.ok = false;
                const requestOptions = {
                    method: "GET",
                    headers: {"Content-Type": "application/json", "Authorization": `Token ${this.$store.state.user.token}`},
                }
                console.log(requestOptions)
            fetch('http://localhost:8000/api/posts/',requestOptions)
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
                    this.posts = response;
            }))
            .catch(err => {
                err.json().then(json => {
                    this.error = json
                });
            })
            }
    },
  components: {
    PostViewComponent, 
  }
}

</script>