<template>
    
    <div class="w-3/4 mx-auto relative overflow-x-auto shadow-md sm:rounded-lg">
        <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                <tr>
                    <th scope="col" class="px-16 py-3">
                        <span class="sr-only">Thumbnail</span>
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Name
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Download
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Delete
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="video in videos" :key="video.id" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-600 dark:hover:bg-gray-650">
                    <td class="p-4">
                        <img :src="video.thumbnail_url" :alt="video.title" class="w-16 md:w-32 max-w-full max-h-full" />
                    </td>
                    <td class="px-6 py-4 font-semibold text-gray-900 dark:text-white">
                        <a :href="video.url" target="_blank" class="font-medium  hover:text-blue-200 dark:hover:text-blue-200 hover:underline">{{ video.title }}</a>
                    </td>
                    <td class="px-6 py-4">
                        <button @click="downloadVideo(video.id)" class="font-medium text-green-600 dark:text-green-500 hover:underline">Download</button>  
                    </td>
                    <td class="px-6 py-4">
                        <button @click="deleteVideo(video.id)" class="font-medium text-red-600 dark:text-red-500 hover:underline">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>



<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const videos = ref([]);

const fetchVideos = async () => {
    const response = await axios.get(`${process.env.VUE_APP_API_BASE_URL}/videos`);
    videos.value = response.data;
};

const deleteVideo = async (id) => {
    try {
        await axios.delete(`${process.env.VUE_APP_API_BASE_URL}/videos/${id}`);
        // After successful deletion, reload the list of videos
        await fetchVideos();
    } catch (error) {
        console.log("Error while deleting Video: " + error);
    }
};
const downloadVideo = (id) => {
    window.open(`${process.env.VUE_APP_API_BASE_URL}/videos/${id}`, '_blank');
};


onMounted(fetchVideos);
</script>