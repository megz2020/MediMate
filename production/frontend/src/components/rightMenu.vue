<template>
  <div>
    <v-row style="height: 100%">
      <v-col cols="12" sm="12" class="chat" style="width: 250px">
        <v-sheet color="black" elevation="0" class="chat-history">
          <v-row>
            <v-col>
              <h2>MediMetAI</h2>
              <v-divider></v-divider>
              <div class="chat-details">
                

                <router-link to="/home" style="text-decoration: none; color: inherit; ">
                    <v-btn variant="tonal" class="w-100 mt-5">Chat</v-btn>
                  </router-link>
                  <router-link to="/dashboard" style="text-decoration: none; color: inherit; ">
                    <v-btn variant="tonal" class="w-100 mt-5">DashBoard View</v-btn>
                  </router-link>
                  <router-link to="/calendar" style="text-decoration: none; color: inherit; ">
                    <v-btn variant="tonal" class="w-100 mt-5">Calendar View</v-btn>
                  </router-link>
                
              </div>
            </v-col>
          </v-row>
        </v-sheet>
        <v-sheet elevation="0" color="black">
          <div class="mb-10">
            <v-divider></v-divider>
            <v-row>
              <v-avatar
                :image="require(`@/assets/images/john-smirk.png`)"
                size="35"
              >
              </v-avatar>
              <p class="mt-1 ml-1">User</p>
            </v-row>
          </div>
        </v-sheet>
      </v-col>
    </v-row>
  </div>
</template>