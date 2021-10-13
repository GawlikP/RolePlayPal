<template>
    <div id="PostViewComponent" >
        <div class="container fluid mx-3 min-w-full min-h-10 px-2 py-2 shadow-md   border border-gray-600 rounded-xl ">
            <p> ID: {{id}} </p>
            <p class="font-bold break-all min-w-full text-purple-900" > <i class="fas fa-user"></i> {{author_username}} </p>
            <p class="break-all text-center font-bold text-xl text-gray-100 min-w-full bg-black rounded-xl "> T: {{title}}  </p>
            <p class="break-all mx-1 py-2"> {{content}}  </p>
                <p class="text-center font-bold text-xl"  > <i class="fas fa-minus-square hover:text-red-700"></i> <i class="fas fa-plus-square hover:text-green-700"></i> {{pluses - minuses}} </p>
        </div>
    </div>
</template>

<script>
export default {
  name: 'PostViewComponent',
  props: {
    id: Number,
    title: String,
    content: String,
    minuses: Number,
    pluses: Number,
    author: Number,
    author_username: String,
    absolute_url: String,
  }
}
</script>