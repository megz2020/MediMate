<script>
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import bootstrapPlugin from "@fullcalendar/bootstrap";

import listPlugin from "@fullcalendar/list";
import Vue from "vue";
import Swal from "sweetalert2";

import { calendarEvents, categories } from "./data-calendar";
// import { required } from "vuelidate/lib/validators";

/*
 * Calendar component
 */
export default {
  components: {
    FullCalendar,
  },
  data() {
    return {
      title: "Calendar",
      
      calendarEvents: calendarEvents,
      calendarOptions: {
        headerToolbar: {
          left: "prev,next today",
          center: "title",
          right: "dayGridMonth,timeGridWeek,timeGridDay,listWeek",
        },
        plugins: [
          dayGridPlugin,
          timeGridPlugin,
          interactionPlugin,
          // bootstrapPlugin,
          listPlugin,
        ],
        initialView: "dayGridMonth",
        themeSystem: "bootstrap",
        initialEvents: calendarEvents,
        editable: true,
        droppable: true,
        eventResizableFromStart: true,
        dateClick: this.dateClicked,
        eventClick: this.editEvent,
        eventsSet: this.handleEvents,
        weekends: true,
        selectable: true,
        selectMirror: true,
        dayMaxEvents: true,
        slotDuration: "00:15:00",
      },
      currentEvents: [],
      showModal: false,
      eventModal: false,
      categories: categories,
      submitted: false,
      submit: false,
      newEventData: {},
      edit: {},
      deleteId: {},
      event: {
        title: "",
        category: "",
      },
      editevent: {
        editTitle: "",
        editcategory: "",
      },
    };
  },
  validations: {
    event: {
      title: {},
      category: {},
    },
  },
  methods: {
    /**
     * Modal form submit
     */
    // eslint-disable-next-line no-unused-vars
    // eslint-disable-next-line no-unused-vars
    hideModal(e) {
      this.submitted = false;
      this.showModal = false;
      this.event = {};
    },
    /**
     * Edit event modal submit
     */
    // eslint-disable-next-line no-unused-vars
    editSubmit(e) {
      this.submit = true;
      const editTitle = this.editevent.editTitle;
      const editcategory = this.editevent.editcategory;
      this.edit.setProp("title", editTitle);
      this.edit.setProp("classNames", editcategory);
      this.successmsg();
      this.eventModal = false;
    },

    /**
     * Delete event
     */
    deleteEvent() {
      this.edit.remove();
      this.eventModal = false;
    },
    /**
     * Modal open for add event
     */
    dateClicked(info) {
      this.newEventData = info;
      this.showModal = true;
    },
    /**
     * Modal open for edit event
     */
    editEvent(info) {
      this.edit = info.event;
      this.editevent.editTitle = this.edit.title;
      this.editevent.editcategory = this.edit.category;
      this.eventModal = true;
    },

    closeModal() {
      this.eventModal = false;
    },   
  },
  middleware: "router-auth",
};
</script>

<template>
  <div class="text-black">
    <v-row>
      <v-col>
        <FullCalendar
        ref="fullCalendar"
        :options="calendarOptions"
      ></FullCalendar>
      </v-col>
     
    </v-row>
  </div>
</template>
<style>
.fc-direction-ltr .fc-button-group > .fc-button:not(:first-child) {
  padding-bottom: 7px;
}
.fc-direction-ltr .fc-button-group > .fc-button:not(:last-child) {
  padding-bottom: 7px;
}
</style>