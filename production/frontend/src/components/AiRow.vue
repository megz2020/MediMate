<template>
  <span class="loader" v-if="getData"></span>
  <div class="user-message" v-else>
    <v-row>
      <v-avatar :image="require(`@/assets/images/ai.png`)" size="35">
      </v-avatar>
      <div class="ml-2">
        <p class="font-weight-bold">MediMetAI</p>
        <p>{{ props.respond }}</p>
      </div>
    </v-row>
  </div>
</template>
<script setup>
import {ref, defineProps } from "vue";
const props = defineProps({
  respond: {
    type: String,
    required: true,
  },
  show: {
    type: Boolean,
    required: true,
  },
});
const getData = ref(true)
setTimeout(function () {
  getData.value = false;
}, 2000);
</script>