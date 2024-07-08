<template>
  <b-jumbotron header-level='5'>
    <template v-slot:header>
      Predict criminal defendants’ recidivism risk
    </template>
    <div class="content-area">
      <p>
        As states struggle to pay for swelling prison and jail populations, paroling low risk defendants who would not jeopardize the public welfare becomes a prevalent method to reduce the government cost. In order to make the right parole decisions, it is critical to have accurate predictions of defendants’ recidivism risks (i.e., will they violate laws again should they be granted parole?).
      </p>
      <p>
        In this HIT, we invite you to try out this prediction task by yourself. You will be asked to complete a sequence of recidivism risk prediction tasks. In each task, you will see the profile of a defendant with his or her previous criminal record. Then, you will be asked to predict <b>whether this defendant would reoffend (I.e., violate any laws again) in the next two years.</b>
      </p>
      <p>
        You can take this HIT only once.
      </p>
      <p>
        Sound interesting? Push the button below to start the HIT.
      </p>
    </div>
    <div v-if="$root.test_mode" class='warning-box'>
      <b>Test Mode</b><br>
      If you see the message, you are in the preview mode. You should not see the message when you accept the HIT. If you see the message after you accept the HIT. There are something wrong about the server. Please return the HIT.
      <b-form-input placeholder="Test Worker ID" v-model="worker_id"/>
      <b-button variant="primary" v-on:click="test_next">Start evaluation with test worker id</b-button>
    </div>
    <div v-else class="button-area">
       <b-button variant="primary" name="next" v-on:click="next">Start Evaluation</b-button>
    </div>
  </b-jumbotron>
</template>
<script>
import axios from 'axios'
export default {
  data: function () {
    return {
      hit_id: null,
      worker_id: null,
      assignment_id: null,
      task_submit_to: null
    }
  },
  methods: {
    test_next: function () {
      let body = new FormData()
      if (this.$store.state.subject_id === null) {
        if (this.$root.test_mode) {
          this.assignment_id = 'test'
          this.hit_id = 'test'
          this.task_submit_to = 'test'
        }
        if (typeof this.worker_id === 'undefined' || this.worker_id === null || this.worker_id === '') {
          this.$alert('We could not get your MTurk ID information, please return the HIT.', '', 'warning')
          return
        }
        body.append('worker_id', this.worker_id)
        body.append('assignment_id', this.assignment_id)
        body.append('hit_id', this.hit_id)
        body.append('task_submit_to', this.task_submit_to)
        axios.post(this.$root.server_url + 'create_without_AI_subject', body)
          .then(response => {
            this.$store.commit('assign_subject_id', {subject_id: response.data.subject_id})
            this.$store.commit('assign_condition', {condition: response.data.condition})
            this.$router.push('/NoHitInstruction')
          })
          .catch(e => {
            if (e.response.status === 403) {
              this.$alert(e.response.data.detail, 'Server Error', 'warning')
            } else {
              this.$alert('We could not get your MTurk ID information, please return the HIT.', 'Server Error', 'warning')
            }
          })
      }
    },
    next: function () {
      let url = location.href
      if (url.indexOf('mturk') !== -1) {
        // Link from mturk, no matter formal entrance or sandbox

        if (url.indexOf('?') !== -1) {
          // Accept: array[0]: assignmentId, array[1]: hitId, array[2]:workerId, array[3]: turkSubmitTo
          // Preview: array[0]: assignmentId, whose value is 'ASSIGNMENT_ID_NOT_AVAILABLE'
          let mturkArray = url.split('?')[1].split('&')
          this.assignment_id = mturkArray[0].split('=')[1]
          if (this.assignment_id !== null && this.assignment_id !== 'ASSIGNMENT_ID_NOT_AVAILABLE') {
            // Already accept the HIT
            this.hit_id = mturkArray[1].split('=')[1]
            this.worker_id = mturkArray[2].split('=')[1]
            this.task_submit_to = mturkArray[3].split('=')[1]

            let body = new FormData()
            if (typeof this.worker_id === 'undefined' || this.worker_id === null || this.worker_id === '') {
              this.$alert('We could not get your MTurk ID information, please return the HIT.', '', 'warning')
              return
            }
            body.append('worker_id', this.worker_id)
            body.append('assignment_id', this.assignment_id)
            body.append('hit_id', this.hit_id)
            body.append('task_submit_to', this.task_submit_to)
            axios.post(this.$root.server_url + 'create_without_AI_subject', body)
              .then(response => {
                this.$store.commit('assign_subject_id', {subject_id: response.data.subject_id})
                this.$store.commit('assign_condition', {condition: response.data.condition})
                this.$router.push('/NoHitInstruction')
              })
              .catch(e => {
                if (e.response.status === 403) {
                  this.$alert(e.response.data.detail, 'Server Error', 'warning')
                } else {
                  this.$alert('We could not get your MTurk ID information, please return the HIT.', 'Server Error', 'warning')
                }
              })
          }
        }
      }
      this.$router.push('/HitInstruction')
    },
    mturk_processor: function (url) {
      // https://jamesbillings67.com/work/?assignmentId=3HL8HNGX4638GN2MFD1ZTQ8J2Z59FO&hitId=360ZO6N6J2LC0DXABY0A0WX1PIV9MI&workerId=A2R1LFNZ1XLCYW&turkSubmitTo=https%3A%2F%2Fwww.mturk.com
    }
  },
  mounted () {
    this.mturk_processor(location.href)
  }
}
</script>
