<template>
  <div id="Home" class="min-h-screen">
    <NavigationBar/>

      <div class="container   min-w-full my-1 py-1 justify-center grid grid-cols-1">
        <div class="grid grid-cols-5 gap-2 py-1 flex min-w-full my-1">
          <div></div>
          <div class="min-w-full my-1 col-span-5 xl:col-span-3 lg:col-span-3 md:col-span-5 sm:col-span-5"> 
            <PostFormComponent />
          </div>
          <div> </div>
        </div>
        
        <PostRecentComponent/>

      </div>
  </div>
</template>

<script>
// @ is an alias to /src
import PostFormComponent from '@/components/Posts/PostFormComponent.vue'
import PostRecentComponent from '@/components/Posts/PostRecentComponent.vue'
import NavigationBar from '@/components/NavigationBar.vue'
export default {
  name: 'Home',
  data(){
        return {
            posts_ids:[2,3,4,7],
            posts: [
                {
                  id: 32,
                  title: "Some random title", 
                  content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec id odio id mauris commodo blandit vitae id metus. Sed sit amet ipsum ut est porttitor varius id vitae sem. Aenean velit nibh, tincidunt sit amet neque ut, elementum sodales erat. Proin erat risus, faucibus a nunc sit amet, malesuada viverra odio. Sed malesuada felis dui, quis aliquam mi ullamcorper eget. Donec suscipit, felis ut ultrices iaculis, ex velit ultricies nunc, ac sollicitudin justo ligula nec quam. Vivamus commodo, lectus eu auctor maximus, nibh tellus tincidunt erat, vitae volutpat libero orci at mauris. Nunc nec felis iaculis justo sagittis viverra. Donec lobortis convallis finibus.",
                  pluses: 3213,
                  minuses: 42342,
                  author: "Jacob",

                },
                {
                  id: 3,
                  title: "Some random title", 
                  content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec id odio id mauris commodo blandit vitae id metus. Sed sit amet ipsum ut est porttitor varius id vitae sem. Aenean velit nibh, tincidunt sit amet neque ut, elementum sodales erat. Proin erat risus, faucibus a nunc sit amet, malesuada viverra odio. Sed malesuada felis dui, quis aliquam mi ullamcorper eget. Donec suscipit, felis ut ultrices iaculis, ex velit ultricies nunc, ac sollicitudin justo ligula nec quam. Vivamus commodo, lectus eu auctor maximus, nibh tellus tincidunt erat, vitae volutpat libero orci at mauris. Nunc nec felis iaculis justo sagittis viverra. Donec lobortis convallis finibus.",
                  pluses: 32,
                  minuses: 4,
                  author: "Tom",

                },
            ],
            ok: false, 
        }
    },
  components: {
    PostFormComponent,
    PostRecentComponent,
    NavigationBar
    
  }
}
</script>
