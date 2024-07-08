<template>
  <b-jumbotron header-level='5'>
    <template v-slot:header>
      Predict criminal defendants' recidivism risk
    </template>
    <div class="content-area">
      <p>
        As states struggle to pay for swelling prison and jail populations, paroling low risk defendants who would not jeopardize the public welfare becomes a prevalent method to reduce the government cost. In order to make the right parole decisions, it is critical to have accurate predictions of defendants' recidivism risks (i.e., will they violate laws again should they be granted parole?).
      </p>
      <p>
        In this task, we invite you to try out this prediction task by yourself. You will be asked to complete a sequence of recidivism risk prediction tasks. In each task, you will see the profile of a defendant with his or her previous criminal record. Then, you will be asked to predict <b>whether this defendant will reoffend (i.e., violate any laws again) in the next two years.</b>
      </p>
      <p>This task offers the opportunity to earn a maximum bonus of $3.2.</p>
      <p>
        You can take this HIT only once. Also, please DO NOT refresh the page.
      </p>
      <p>
        Sound interesting? Push the button below to start the HIT.
      </p>
    </div>
    <div v-if="$root.test_mode" class='warning-box'>
      <b>Test Mode</b><br>
      If you see the message, you are in the preview mode. You should not see the message when you accept the HIT. If you see the message after you accept the HIT. There are something wrong about the server. Please return the HIT.
      <b-form-input placeholder="Test Worker ID" v-model="worker_id"/>
      <b-form-group label="condition_selection" v-slot="{ ariaDescribedby }">
        <b-form-radio v-model="selected" :aria-describedby="ariaDescribedby" name="condition_selection" value="-1">
          Not assigned (formal)
        </b-form-radio>
        <b-form-radio v-model="selected" :aria-describedby="ariaDescribedby" name="condition_selection" value="0">
          No devil's advocate
        </b-form-radio>
        <b-form-radio v-model="selected" :aria-describedby="ariaDescribedby" name="condition_selection" value="1">
          Static devil's advocate for AI
        </b-form-radio>
        <b-form-radio v-model="selected" :aria-describedby="ariaDescribedby" name="condition_selection" value="2">
          Dynamic devil's advocate for AI
        </b-form-radio>
        <b-form-radio v-model="selected" :aria-describedby="ariaDescribedby" name="condition_selection" value="3">
          Static devil's advocate for group
        </b-form-radio>
        <b-form-radio v-model="selected" :aria-describedby="ariaDescribedby" name="condition_selection" value="4">
          Dynamic devil's advocate for group
        </b-form-radio>
      </b-form-group>
      <b-button variant="primary" v-on:click="test_next">Start evaluation with test worker id</b-button>
    </div>
    <div v-else-if="not_qualified">
      If you see the message, you might be in preview mode or haven't passed the qualifying exam. If you believe that you have the qualification and accepted the HIT but still see the message, please return the HIT.
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
      not_qualified: true,
      hit_id: null,
      worker_id: null,
      assignment_id: null,
      task_submit_to: null,
      selected: null
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
        body.append('condition', this.selected)

        axios.post(this.$root.server_url + 'create_group_subject', body)
          .then(response => {
            if (response.data.success === true) {
              this.$store.commit('assign_subject_id', {subject_id: response.data.subject_id})
              this.$store.commit('assign_condition', {condition: response.data.condition})
              this.$router.push('/HitInstruction')
              // this.$router.push('/formalInstruction')
            } else {
              this.$alert('We could not find your information in the server, please make sure you have passed the qualification.', '', 'warning')
            }
          })
          .catch(e => {
            if (e.response.status === 403) {
              this.$alert(e.response.data.detail, '', 'warning')
            } else {
              this.$alert('Please contact us and mention where do you see the alert.', 'Server Error', 'warning')
            }
          })
      }
    },
    next: function () {
      this.$router.push('/PreSurvey')
      // this.$router.push('/HitInstruction')
    },
    mturk_processor: function (url) {
      // https://jamesbillings67.com/work/?assignmentId=3HL8HNGX4638GN2MFD1ZTQ8J2Z59FO&hitId=360ZO6N6J2LC0DXABY0A0WX1PIV9MI&workerId=A2R1LFNZ1XLCYW&turkSubmitTo=https%3A%2F%2Fwww.mturk.com
      // if (url.indexOf('mturk') !== -1) {
      //   // Link from mturk, no matter formal entrance or sandbox
      //   if (url.indexOf('?') !== -1) {
      //     // Accept: array[0]: assignmentId, array[1]: hitId, array[2]:workerId, array[3]: turkSubmitTo
      //     // Preview: array[0]: assignmentId, whose value is 'ASSIGNMENT_ID_NOT_AVAILABLE'
      //     let mturkArray = url.split('?')[1].split('&')
      //     this.assignment_id = mturkArray[0].split('=')[1]
      //     if (this.assignment_id !== null && this.assignment_id !== 'ASSIGNMENT_ID_NOT_AVAILABLE') {
      //       // Already accept the HIT
      //       this.hit_id = mturkArray[1].split('=')[1]
      //       this.worker_id = mturkArray[2].split('=')[1]
      //       this.task_submit_to = mturkArray[3].split('=')[1]

      //       let body = new FormData()
      //       if (typeof this.worker_id === 'undefined' || this.worker_id === null || this.worker_id === '') {
      //         this.$alert('We could not get your MTurk ID information, please return the HIT.', '', 'warning')
      //         return
      //       }
      //       body.append('worker_id', this.worker_id)
      //       body.append('assignment_id', this.assignment_id)
      //       body.append('hit_id', this.hit_id)
      //       body.append('task_submit_to', this.task_submit_to)
      //       axios.post(this.$root.server_url + 'get_subject_info', body)
      //         .then(response => {
      //           if (response.data.success === true) {
      //             this.$store.commit('assign_subject_id', {subject_id: response.data.subject_id})
      //             // this.$store.commit('assign_condition', {condition: response.data.condition})
      //           } else {
      //             this.$alert('We could not find your information in the server, please make sure you have passed the qualification.', '', 'warning')
      //           }
      //         })
      //         .catch(e => {
      //           this.$alert(e.response.data.detail, '', 'warning')
      //         })
      //       this.not_qualified = false
      //     }
      //   }
      // }
      if (url.indexOf('?') !== -1) {
        // from prolific
        // https://dev.d1uau7ss3lp78y.amplifyapp.com/qualificationentrance/?PROLIFIC_PID={{%PROLIFIC_PID%}}&STUDY_ID={{%STUDY_ID%}}&SESSION_ID={{%SESSION_ID%}}
        this.platform = 'prolific'
        let prolificArray = url.split('?')[1].split('&')
        this.worker_id = prolificArray[0].split('=')[1]
        this.study_id = prolificArray[1].split('=')[1]
        this.session_id = prolificArray[2].split('=')[1]

        let body = new FormData()
        if (typeof this.worker_id === 'undefined' || this.worker_id === null || this.worker_id === '') {
          this.$alert('We could not get your MTurk ID information, please return the HIT.', '', 'warning')
          return
        }
        body.append('worker_id', this.worker_id)
        body.append('study_id', this.study_id)
        body.append('session_id', this.session_id)
        axios.post(this.$root.server_url + 'create_subject', body)
          .then(response => {
            if (response.data.success === true) {
              this.$store.commit('assign_subject_id', {subject_id: response.data.subject_id})
            } else {
              this.$alert('You have done the task before, please return the HIT.', '', 'warning')
            }
          })
          .catch(e => {
            this.$alert(e.response.data.detail)
          })
        this.not_qualified = false
      } else {
        this.not_qualified = true
      }
    }
  },
  mounted () {
    this.mturk_processor(location.href)
  }
}
</script>
