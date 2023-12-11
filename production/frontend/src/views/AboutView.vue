<template>
  <div>
    <v-row style="height: 100vh">
      <v-col class="chat">
        <v-sheet color="white" elevation="0" style="flex: 1">
          <div>
            <h2 class="ml-2">MediMetAI</h2>
            <div class="chat-details chat-details-style">
              <!-- Your other components go here -->
              <div v-for="(item, index) in messages" :key="index" class="mt-10">
                <UserRow class="mt-5" :imageUrl="item.imagesUrl" />

                <AiRow class="mt-5" :respond="item.respond" :show="getData" />
              </div>
            </div>
          </div>
        </v-sheet>
        <v-sheet
          color="white"
          elevation="0"
          class="chat-details chat-details-style"
        >
          <v-row>
            <v-file-input
              label="upload "
              v-model="selectedFile"
              accept=".jpg, .jpeg, .png"
            ></v-file-input>
            <v-btn
              @click="uploadImage"
              class="ml-3 upload-btn"
              color="black"
              :disabled="setSend"
            >
              Send
              <v-icon size="20">mdi-navigation</v-icon>
            </v-btn>
          </v-row>
        </v-sheet>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import UserRow from "@/components/UserRow.vue";
import AiRow from "@/components/AiRow.vue";
const selectedFile = ref("");
const setSend = ref(true);

const imageUrl = ref("");
const setImage = ref(null);
watch(selectedFile, () => {
  if (selectedFile.value != "") {
    setSend.value = false;
  }
});
const messages = ref([]);
const getData = ref(true);
const uploadImage = () => {
  if (selectedFile.value && selectedFile.value.length > 0) {
    const reader = new FileReader();
    reader.onload = async () => {
      imageUrl.value = reader.result;
      messages.value.push({
        imagesUrl: imageUrl.value,
      });
      setTimeout(function () {
        getData.value = false;
      }, 2000);
      getData.value = true;
      let newLen = messages.value.length - 1;
      // console.log(newLen,messages.value[newLen])
      messages.value[newLen].respond = "message";
    };
    reader.readAsDataURL(selectedFile.value[0]);

    setImage.value = "ok";
    selectedFile.value = "";
    setSend.value = true;
  } else {
    imageUrl.value = "";
  }
};
</script>
<style>
.chat {
  display: flex;
  flex-direction: column;
}
.chat-details-style {
  margin-left: 100px;
  margin-right: 100px;
}
.chat-details {
  max-height: 80vh;
  overflow-y: auto;
}
.chat-history {
  height: 100vh;
  flex: 1;
  padding-left: 10px;
  padding-right: 10px;
}
.chat-details::-webkit-scrollbar {
  width: 6px; /* Adjust the width as needed */
}

.chat-details::-webkit-scrollbar-thumb {
  background-color: transparent; /* Hide the scrollbar thumb */
}
.upload-btn {
  height: 55px !important;
}
.loader,
.loader:before,
.loader:after {
  border-radius: 50%;
  width: 2.5em;
  height: 2.5em;
  animation-fill-mode: both;
  animation: bblFadInOut 1.8s infinite ease-in-out;
}
.loader {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: block;
  margin: 15px auto;
  position: relative;
  background: #000000;
  box-shadow: -24px 0 #000000, 24px 0 #000000;
  box-sizing: border-box;
  animation: shadowPulse 2s linear infinite;
}

@keyframes shadowPulse {
  33% {
    background: #000000;
    box-shadow: -24px 0 #ffffff, 24px 0 #000000;
  }
  66% {
    background: #ffffff;
    box-shadow: -24px 0 #000000, 24px 0 #0d0d0d;
  }
  100% {
    background: #000000;
    box-shadow: -24px 0 #070707, 24px 0 #ffffff;
  }
}
</style>
