<template>

    <div id="CommentViewComponent">
        <p class="font-bold"> AUTHOR</p>
        <p class=" text-gray-700 text-xs font-bold"> Date: dsafsdafdsafdsaf </p>
        <p class="text-xl font-bold"> content </p>
    </div>

</template>

<script>

export default{
    name: 'CommentViewComponent',
    props: {
        post_absolute_url: String
    },
}


</script>