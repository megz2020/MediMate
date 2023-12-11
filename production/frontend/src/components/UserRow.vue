<template>
  <div class="user-message">
    <v-row>
      <v-avatar :image="require(`@/assets/images/john-smirk.png`)" size="35">
      </v-avatar>
      <div class="ml-2">
        <p class="font-weight-bold">you</p>
        <!-- <p>message</p> -->
        <v-img :src="props.imageUrl " width="200" height="200"></v-img>
      </div>
    </v-row>
  </div>
</template>
<script setup>
import { defineProps } from "vue";
const props = defineProps({
  imageUrl: {
    type: String,
    required: true,
  },
});

</script>