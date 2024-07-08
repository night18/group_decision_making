<template>
  <b-jumbotron header-level='5'>
    <template v-slot:lead>
      Formal test ({{displayed_id}}/{{$store.state.formal_task.length}})
    </template>
    <template v-if="$root.is_loading">
      <div class="text-center">
        <b-spinner variant="primary" label="Loading"></b-spinner>
      </div>
    </template>
    <template v-else>
      <b-row>
        <b-col cols='12'>
          <div class="content-area">
            <p>Please review the profile below and predict whether the defendant would reoffend in the next two years.</p>
            <TaskInfo :defendant="$store.state.formal_task[get_id]"/>
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
              <b-form-group v-slot="{ ariaDescribedby }">
               <b-form-radio v-model="estimation" :aria-describedby="ariaDescribedby" value="True">The defendant <b>will</b> reoffend within two years</b-form-radio>
               <b-form-radio v-model="estimation" :aria-describedby="ariaDescribedby" value="False">The defendant <b>will not</b> reoffend within two years</b-form-radio>
             </b-form-group>
            </div>
          </div>
        </b-col>
      </b-row>
      <div class="button-area">
       <b-button variant="primary" name="next" v-on:click="next">Continue</b-button>
    </div>
    </template>
  </b-jumbotron>
</template>
<script>
import axios from 'axios'
import TaskInfo from '@/components/TaskInfo.vue'
export default {
  data: function () {
    return {
      estimation: null,
      start_time: null
    }
  },
  components: {
    TaskInfo
  },
  props: ['taskid'],
  methods: {
    next: function () {
      if (this.estimation) {
        let body = new FormData()
        let end_time = new Date()

        body.append('subject_id', this.$store.state.subject_id)
        body.append('instance_id', this.$store.state.formal_task[this.get_id].instance_id)
        body.append('task_no', this.get_id)
        body.append('human_estimation', this.estimation)
        body.append('spend_time', (end_time - this.start_time) / 1000)

        axios.post(this.$root.server_url + 'record_single_formal', body)
          .then(response => {
            this.$store.commit('formal_record', {task_no: this.get_id, estimation: this.estimation})

            let likert_options = {
              1: 'Not confident at all',
              2: 'Mostly not confident',
              3: 'Somewhat confident',
              4: 'Moderately confident',
              5: 'Extremely confident'
            }

            this.$fire({
              title: 'Before moving on',
              html: '<p>Pleasee answer the following question.</p><hr><p>How confident are you in your prediction for this defendant?</p>',
              input: 'radio',
              inputOptions: likert_options,
              type: 'question',
              allowOutsideClick: false,
              preConfirm: (likert) => {
                if (typeof likert === 'undefined' || likert === null) {
                  this.$showValidationMessage('Please make a selection')
                }

                let confidence_body = new FormData()
                confidence_body.append('subject_id', this.$store.state.subject_id)
                confidence_body.append('instance_id', this.$store.state.formal_task[this.get_id].instance_id)
                confidence_body.append('task_no', this.get_id)
                confidence_body.append('confidence', likert)
                this.$root.is_loading = true
                axios.post(this.$root.server_url + 'record_single_confidence', confidence_body)
                  .then(response => {
                    this.$root.is_loading = false
                    this.start_time = new Date()
                    this.estimation = null
                    if (this.displayed_id === this.$store.state.formal_task.length) {
                      this.$router.push('/UnderstandingSurvey')
                    } else {
                      this.$router.push('/SingleFormalTask/' + this.displayed_id)
                    }
                  })
                return true
              }
            })
          })
          .catch(e => {
            this.$alert('Could not record practice tasks.', 'Error', 'error')
          })
      } else {
        this.$alert('please specify your prediction')
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
      if (this.$store.state.formal_task[this.get_id].model_suggestion === 'True') {
        return 'will'
      } else {
        return 'will not'
      }
    }
  },
  mounted () {
    this.start_time = new Date()
    this.estimation = null

    if (this.get_id === 0) {
      let body = new FormData()
      body.append('subject_id', this.$store.state.subject_id)
      axios.post(this.$root.server_url + 'formal_start', body)
    }
  },
  watch: {
  }
}
</script>
<style>
</style>
