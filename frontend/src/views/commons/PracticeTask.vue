<template>
  <b-jumbotron header-level='5'>
    <template v-slot:lead>
      Individual Test ({{displayed_id}}/9)
    </template>
    <div class="content-area">
      <p>Please review the profile below and predict whether the defendant would reoffend in the next two years.</p>
      <TaskInfo :defendant="$store.state.practice_task[get_id]"/>
      <p v-show="$store.state.practice_task[get_id].condition === -2" style="text-align: left; color:red;">This question is an attention check question. Please select "The defendant will reoffend within 2 years" in the <b>initial prediction.</b> and select "The defendant will not reoffend within 2 years" in the <b>final prediction.</b> </p>
      <!-- <TaskInfo /> -->
      <div>
        <div class="answer-area">
          <p>
            <b>Make Your Initial Prediction</b>
          </p>
          <p>Do you think this defendant will reoffend within 2 years?</p>
          <b-form-group v-slot="{ ariaDescribedby }" :disabled="is_predicted">
           <b-form-radio v-model="initial_answer" :aria-describedby="ariaDescribedby" value="True">The defendant <b>will</b> reoffend within 2 years</b-form-radio>
           <b-form-radio v-model="initial_answer" :aria-describedby="ariaDescribedby" value="False">The defendant <b>will not</b> reoffend within 2 years</b-form-radio>
         </b-form-group>
        </div>
        <div v-if="!is_predicted" class="button-area">
          <b-button variant="primary" name="initial" :disabled="$root.is_loading" v-on:click="record_initial">Continue</b-button>
        </div>
      </div>
      <div v-if="is_predicted">
        <div class="suggestion-area">
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
          <b-form-group v-slot="{ ariaDescribedby }" :disabled="is_submit">
           <b-form-radio v-model="final_answer" :aria-describedby="ariaDescribedby" value="True">The defendant <b>will</b> reoffend within 2 years</b-form-radio>
           <b-form-radio v-model="final_answer" :aria-describedby="ariaDescribedby" value="False">The defendant <b>will not</b> reoffend within 2 years</b-form-radio>
          </b-form-group>
        </div>
        <div v-if="!is_submit" class="button-area">
           <b-button variant="primary" name="final" :disabled="$root.is_loading" v-on:click="final">Continue</b-button>
        </div>
      </div>
      <div v-if="is_submit">
        <div class="truth-area">
          <p>
            <b>What happened after 2 years?</b>
          </p>
          <p>The defendant <span class="highlight">did {{ground_truth}}</span> reoffend within 2 years.</p>
        </div>
        <div class="button-area">
           <b-button variant="primary" name="next" :disabled="$root.is_loading" v-on:click="next">Continue</b-button>
        </div>
      </div>
    </div>
  </b-jumbotron>
</template>
<script>
import axios from 'axios'
import TaskInfo from '@/components/TaskInfo.vue'
export default {
  data: function () {
    return {
      initial_answer: null,
      final_answer: null,
      is_predicted: false,
      is_submit: false,
      start_time: null
    }
  },
  components: {
    TaskInfo
  },
  props: ['taskid'],
  methods: {
    final: function () {
      if (this.initial_answer && this.final_answer) {
        let end_time = new Date()
        let body = new FormData()

        body.append('subject_id', this.$store.state.subject_id)
        body.append('instance_id', this.$store.state.practice_task[this.get_id].instance_id)
        body.append('task_no', this.get_id)
        body.append('initial_answer', this.initial_answer)
        body.append('final_answer', this.final_answer)
        body.append('spend_time', (end_time - this.start_time) / 1000)

        this.$root.is_loading = true
        if (this.$store.state.practice_task[this.get_id].condition === -2) {
          if (this.initial_answer !== 'True' || this.final_answer !== 'False') {
            axios.post(this.$root.server_url + 'unqualified', body)
              .then(response => {
                this.$root.is_loading = false
                this.$router.push('/FailAttention/')
              })
          } else {
            this.$root.is_loading = false
            if (this.displayed_id !== this.$store.state.practice_task.length) {
              this.$router.push('/PracticeTask/' + this.displayed_id)
            } else {
              this.$router.push('/PracticeSummary')
            }
          }
        } else {
          axios.post(this.$root.server_url + 'record_practice', body)
            .then(response => {
              this.$root.is_loading = false
              this.$root.initial_answer = this.initial_answer
              this.$root.final_answer = this.final_answer
              this.$store.commit('practice_record', {task_no: this.get_id, initial_answer: this.initial_answer, final_answer: this.final_answer})
              this.start_time = new Date()
              this.is_submit = true
            })
            .catch(e => {
              this.$alert('Could not record practice tasks.', 'Error', 'error')
            })
        }
      } else {
        this.$alert('Please make your final prediction!.', '', 'warning')
      }
    },
    record_initial: function () {
      if (this.initial_answer !== null) {
        this.is_predicted = true
      } else {
        this.$alert('Please make your initial prediction!', '', 'warning')
      }
    },
    next: function () {
      if (this.displayed_id !== this.$store.state.practice_task.length) {
        this.$router.push('/PracticeTask/' + this.displayed_id)
      } else {
        this.$router.push('/PracticeSummary')
      }
    }
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
    }
  },
  mounted () {
    this.start_time = new Date()
  }
}
</script>
<style>
</style>
