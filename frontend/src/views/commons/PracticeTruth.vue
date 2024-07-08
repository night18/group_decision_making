<template>
  <b-jumbotron header-level='5'>
    <template v-slot:lead>
      Practice example ({{displayed_id}}/{{$store.state.practice_task.length}})
    </template>
    <div class="content-area">
      <p>Please review the profile below and predict whether the defendant would reoffend in the next two years.</p>
      <TaskInfo :defendant="$store.state.practice_task[get_id]"/>
      <!-- <TaskInfo /> -->
      <div class="suggestion-area" v-if="$store.state.condition !== -2">
        <p>
          <b>Machine learning Prediction:</b>
        </p>
        Our machine learning model predicts that this defendant <span class="highlight">{{ml_suggestion}}</span> reoffend in 2 years.
      </div>
      <div class="answer-area">
        <p>
          <b>Make Your Prediction</b>
        </p>
        <p>Do you think this defendant will reoffend within 2 years?</p>
        <b-form-group v-slot="{ ariaDescribedby }">
         <b-form-radio v-model="estimation" :aria-describedby="ariaDescribedby" value="True" disabled>The defendant <b>will</b> reoffend within 2 years</b-form-radio>
         <b-form-radio v-model="estimation" :aria-describedby="ariaDescribedby" value="False" disabled>The defendant <b>will not</b> reoffend within 2 years</b-form-radio>
       </b-form-group>
      </div>
      <div class="truth-area">
        <p>
          <b>What happened after 2 years?</b>
        </p>
        <p>The defendant <span class="highlight">did {{ground_truth}}</span> reoffend within 2 years.</p>
      </div>
    </div>
    <div class="button-area">
       <b-button variant="primary" name="next" v-on:click="next">Next</b-button>
    </div>
  </b-jumbotron>
</template>
<script>
import TaskInfo from '@/components/TaskInfo.vue'
export default {
  data: function () {
    return {
    }
  },
  components: {
    TaskInfo
  },
  props: ['taskid'],
  methods: {
    next: function () {
      if (this.displayed_id !== this.$store.state.practice_task.length) {
        this.$router.push('/PracticeTask/' + this.displayed_id)
      } else {
        this.$router.push('/PracticeSummary')
      }
    }
  },
  mounted () {
  },
  computed: {
    displayed_id: function () {
      return parseInt(this.taskid) + 1
    },
    get_id: function () {
      return parseInt(this.taskid)
    },
    ml_suggestion: function () {
      if (this.$store.state.practice_task[this.get_id].model_suggestion === 'True') {
        return 'will'
      } else {
        return 'will not'
      }
    },
    ground_truth: function () {
      if (this.$store.state.practice_task[this.get_id].ground_truth === 'True') {
        return ''
      } else {
        return 'not'
      }
    },
    estimation: function () {
      return this.$store.state.practice_task[this.get_id].user_prediction
    }
  }
}
</script>
<style>

</style>
