<template>
  <b-jumbotron header-level='5'>
    <template v-slot:header>
      Predict criminal defendants’ recidivism risk
    </template>
    <div class="content-area">
      <p>
        We plan to post HITs in the next week inviting Amazon Mechanical Turk workers to participate in a research study, in which they will be asked to complete a sequence of recidivism risk prediction tasks. This HIT will serve as a qualification task for that research study. If you are interested in that study, please complete this HIT to sign up for it.
      </p>
      <p>
        Specifically, in this HIT, you will be asked to complete a simple demographic survey. We will also give you a sample of recidivism risk prediction tasks (i.e., the same type of tasks that you will be asked to work on in the next week’s research study), so that you can try them out and determine whether you are interested in our research study next week.
      </p>
    </div>
    <div v-if="$root.test_mode" class='warning-box'>
      <b>Test Mode</b><br>
      If you see the message, you are in the preview mode, and you will not see the message when you accept the HIT.<br>
      If you have accepted the HIT, and still see the message. There are something wrong about the server. Please return the HIT.
      <b-form-input placeholder="Test Worker ID" v-model="worker_id"/>
      <b-button variant='primary' v-on:click="next">Create test worker id</b-button>
    </div>
    <div v-else class="button-area">
       <b-button variant="primary" name="next" v-on:click="next">Get Qualification</b-button>
    </div>
  </b-jumbotron>
</template>
<script>
import axios from 'axios'
export default {
  data: function () {
    return {
      platform: null,
      worker_id: null,
      hit_id: null,
      assignment_id: null,
      task_submit_to: null
    }
  },
  methods: {
    next: function () {
      let body = new FormData()
      if (this.$store.state.subject_id === null) {
      // New login
        if (this.platform === 'mutrk') {
          if (typeof this.worker_id === 'undefined' || this.worker_id === null || this.worker_id === '') {
            this.$alert('We could not get your MTurk ID information, please return the HIT.', '', 'warning')
            return
          }
          body.append('worker_id', this.worker_id)
          body.append('assignment_id', this.assignment_id)
          body.append('hit_id', this.hit_id)
          body.append('task_submit_to', this.task_submit_to)
          axios.post(this.$root.server_url + 'create_subject', body)
            .then(response => {
              if (response.data.success === true) {
                this.$store.commit('assign_subject_id', {subject_id: response.data.subject_id})
                this.$router.push('/PreSurvey')
              } else {
                this.$alert('You have done the task before, please return the HIT.', '', 'warning')
              }
            })
            .catch(e => {
              this.$alert(e.response.data.detail)
            })
        } else if (this.platform === 'prolific') {
          if (typeof this.worker_id === 'undefined' || this.worker_id === null || this.worker_id === '') {
            this.$alert('We could not get your MTurk ID information, please return the HIT.', '', 'warning')
            return
          }
        } else if (this.$root.test_mode) {
          this.study_id = 'test'
          this.session_id = 'test'
        }
        body.append('worker_id', this.worker_id)
        body.append('study_id', this.study_id)
        body.append('session_id', this.session_id)
        axios.post(this.$root.server_url + 'create_subject', body)
          .then(response => {
            if (response.data.success === true) {
              this.$store.commit('assign_subject_id', {subject_id: response.data.subject_id})
              this.$router.push('/PreSurvey')
            } else {
              this.$alert('You have done the task before, please return the HIT.', '', 'warning')
            }
          })
          .catch(e => {
            this.$alert(e.response.data.detail)
          })
      }
    },
    mturk_processor: function (url) {
      // https://jamesbillings67.com/work/?assignmentId=3HL8HNGX4638GN2MFD1ZTQ8J2Z59FO&hitId=360ZO6N6J2LC0DXABY0A0WX1PIV9MI&workerId=A2R1LFNZ1XLCYW&turkSubmitTo=https%3A%2F%2Fwww.mturk.com
      if (url.indexOf('?') !== -1) {
        if (url.indexOf('mturk') !== -1) {
          this.platform = 'mturk'
          let mturkArray = url.split('?')[1].split('&')
          // Accept: array[0]: assignmentId, array[1]: hitId, array[2]:workerId, array[3]: turkSubmitTo
          // Preview: array[0]: assignmentId, whose value is 'ASSIGNMENT_ID_NOT_AVAILABLE'
          this.assignment_id = mturkArray[0].split('=')[1]
          if (this.assignment_id !== null && this.assignment_id !== 'ASSIGNMENT_ID_NOT_AVAILABLE') {
            // Already accept the HIT
            this.hit_id = mturkArray[1].split('=')[1]
            this.worker_id = mturkArray[2].split('=')[1]
            this.task_submit_to = mturkArray[3].split('=')[1]
          }
        } else {
          // from prolific
          // https://dev.d1uau7ss3lp78y.amplifyapp.com/qualificationentrance/?PROLIFIC_PID={{%PROLIFIC_PID%}}&STUDY_ID={{%STUDY_ID%}}&SESSION_ID={{%SESSION_ID%}}
          this.platform = 'prolific'
          let prolificArray = url.split('?')[1].split('&')
          this.worker_id = prolificArray[0].split('=')[1]
          this.study_id = prolificArray[1].split('=')[1]
          this.session_id = prolificArray[2].split('=')[1]
        }
      }
    }
  },
  mounted () {
    this.mturk_processor(location.href)
  }
}
</script>
