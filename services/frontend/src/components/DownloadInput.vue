<template>
    <form class="w-3/4 mx-auto" @submit.prevent="submitForm">   
        <div class="relative">
            <input v-model="videoUrl" type="text" id="default-download" class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Enter Video URL here..." required>
            <button type="submit" class="text-white absolute end-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Download</button>
        </div>
    </form>
</template>



<script setup>
import { ref } from 'vue';
import axios from 'axios';

let videoUrl = ref('');

const submitForm = async () => {
    try {
        await axios.post(`${process.env.VUE_APP_API_BASE_URL}/download`, { url: videoUrl.value });
    } catch (error) {
        console.error('Error while sending video URL:', error);
    }
};
</script>