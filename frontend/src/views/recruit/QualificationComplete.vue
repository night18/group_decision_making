<template>
  <b-jumbotron header-level='5'>
    <template v-slot:header>
      That's all!
    </template>
    <div>
      Thank you again for taking this qualification HIT. The formal HIT will be posted this week at
      <ul>
        <li>14:00 (ET) on Tuesday (2023/08/16)</li>
        <li>14:00 (ET) on Wednesday (2023/08/17)</li>
        <li>17:00 (ET) on Wednesday (2023/08/17)</li>
        <li>14:00 (ET) on Thursday (2023/08/18)</li>
        <li>17:00 (ET) on Thursday (2023/08/18)</li>
        <li>14:00 (ET) on Friday (2023/08/19)</li>
        <li>17:00 (ET) on Friday (2023/08/19)</li>
      </ul>
      After completing this HIT, are you interested in to get email notification of the formal HIT to work on more recidivism prediction tasks?
      <b-form-radio-group
          v-model="is_interest"
          name="is_interest"
          :options="interest"
          stacked
      />
      <div v-if="is_interest === 'True'">
        <p v-if="is_interest">Thank you for your interest in our research study. Once we post the HITs later this week for our research study, we will send an email to notify you.</p>
        <p v-else>No problem. Please submit this HIT to get your payment for this HIT!</p>
      </div>
    </div>
    <div class="button-area">
      <h5>Please push the button below to submit the HIT!</h5>
      <b-button variant="primary" name="next" v-bind:disabled="is_interest === null" v-on:click="next">Submit HIT</b-button>
    </div>
  </b-jumbotron>
</template>
<script>
import axios from 'axios'
export default {
  data: function () {
    return {
      is_interest: null,
      interest: [
        { text: 'Yes, I’d like to sign up notification for this week’s research study.', value: 'True' },
        { text: 'No, I prefer not to get notification this week’s research study.', value: 'False' }
      ]
    }
  },
  methods: {
    next: function () {
      let body = new FormData()
      body.append('subject_id', this.$store.state.subject_id)
      body.append('is_interest', this.is_interest)
      axios.post(this.$root.server_url + 'complete_qualification', body)
        .then(response => {
          window.location.href = response.data.mturk_url
        })
        .catch(e => {
          alert('Some error happened!! Please leave comments and submit the HIT on MTurk.')
        })
    }
  },
  mounted () {
  }
}
</script>
