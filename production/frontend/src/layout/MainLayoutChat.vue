<template>
    <v-layout class="rounded rounded-md">
      <RightMenu />
      <v-main>
        <router-view />
      </v-main>
    </v-layout>
</template>
<script setup>
import RightMenu from "@/components/rightMenu.vue"
</script>