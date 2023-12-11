<template>
  <div>
    <v-row style="height: 100vh">
      <v-col class="chat">
        <v-sheet color="white" elevation="0" style="flex: 1">
          <div>
            <p class="text-h3 text-center mb-2 mt-2">All Prescription Information </p>
            <v-data-table
              :headers="headers"
              :items="desserts"
              :group-by="groupBy"
              item-value="name"
            >
              <template
                v-slot:group-header="{
                  item,
                  columns,
                  toggleGroup,
                  isGroupOpen,
                }"
              >
                <tr>
                  <td :colspan="columns.length">
                    <VBtn
                      size="small"
                      variant="text"
                      :icon="isGroupOpen(item) ? '$expand' : '$next'"
                      @click="toggleGroup(item)"
                    ></VBtn>
                    {{ item.value }}
                  </td>
                </tr>
              </template>
            </v-data-table>
          </div>
        </v-sheet>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { VDataTable } from "vuetify/labs/VDataTable";
export default {

    components: {
        VDataTable,
    },
    data () {
      return {
        groupBy: [
          {
            key: 'prescription',
            order: 'asc',
          },
        ],
        headers: [
          
          { title: 'Medical Name', key: 'medicalName' },
          { title: 'Duration', key: 'duration' },
          { title: 'Instructions', key: 'instructions' },
          { title: 'Side Effects', key: 'side_effects' },
        ],
        desserts: [
          {
            medicalName: 'doxycycline',
            duration: '1 week',
            instructions: '2 times after brakfast and dinner',
            side_effects:"(hives, difficulty breathing, swelling in your face or throat)",
            prescription: "prescription1",
          },
          {
            medicalName: 'spironolactone',
            duration: '3 week',
            instructions: '2 times after brakfast and dinner',
            side_effects:"hives ; difficulty breathing; swelling of your face, lips, tongue, or throat.",
            prescription: "prescription1",
          },
          {
            medicalName: 'clindamycin',
            duration: '4 week',
            instructions: '2 times after brakfast and dinner',
            side_effects:"hives ; difficult breathing; swelling of your face, lips, tongue, or throat",
            prescription: "prescription1",
          },
          {
            medicalName: 'doxycycline',
            duration: '1 week',
            instructions: '2 times after brakfast and dinner',
            side_effects:"(hives, difficulty breathing, swelling in your face or throat)",
            prescription: "prescription2",
          },
          {
            medicalName: 'spironolactone',
            duration: '3 week',
            instructions: '2 times after brakfast and dinner',
            side_effects:"hives ; difficulty breathing; swelling of your face, lips, tongue, or throat.",
            prescription: "prescription2",
          },
          {
            medicalName: 'clindamycin',
            duration: '4 week',
            instructions: '2 times after brakfast and dinner',
            side_effects:"hives ; difficult breathing; swelling of your face, lips, tongue, or throat",
            prescription: "prescription2",
          }
        ],
      }
    },
  }
</script>

<style>
</style>