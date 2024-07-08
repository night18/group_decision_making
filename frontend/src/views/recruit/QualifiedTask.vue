<template>
  <b-jumbotron header-level='5'>
    <template v-slot:lead>
      Individual Test ({{displayed_id}}/18)
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
            <TaskInfo :defendant="$store.state.qualified_task[get_id]"/>
            <p v-show="$store.state.qualified_task[get_id].condition === -2" style="text-align: left; color:red;">This question is an attention check question. Please select "The defendant will reoffend within 2 years" as your prediction.</p>
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
        body.append('instance_id', this.$store.state.qualified_task[this.get_id].instance_id)
        body.append('task_no', this.get_id)
        body.append('human_estimation', this.estimation)
        body.append('spend_time', (end_time - this.start_time) / 1000)
        this.$root.is_loading = true
        if (this.$store.state.qualified_task[this.get_id].condition === -2) {
          if (this.estimation !== 'True') {
            axios.post(this.$root.server_url + 'unqualified', body)
              .then(response => {
                this.$root.is_loading = false
                this.$router.push('/FailAttention/')
              })
          } else {
            this.$root.is_loading = false
            this.estimation = null
            this.start_time = new Date()
            if (this.displayed_id === this.$store.state.qualified_task.length) {
              this.$router.push('/QualificationComplete')
              // this.$router.push('/ModelInstruction')
            } else {
              this.$router.push('/QualifiedTask/' + this.displayed_id)
            }
          }
        } else {
          axios.post(this.$root.server_url + 'record_qualified_task', body)
            .then(response => {
              this.$root.is_loading = false
              this.start_time = new Date()
              this.estimation = null
              if (this.displayed_id === this.$store.state.qualified_task.length) {
                this.$router.push('/QualificationComplete')
                // this.$router.push('/ModelInstruction')
              } else {
                this.$router.push('/QualifiedTask/' + this.displayed_id)
              }
            })
            .catch(e => {
              this.$alert('Could not record practice tasks.', 'Error', 'error')
            })
        }
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
    }
  },
  mounted () {
    this.start_time = new Date()
    this.estimation = null
  },
  watch: {
  }
}
</script>
<style>
</style>
