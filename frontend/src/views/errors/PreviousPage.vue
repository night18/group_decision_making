<template>
  <b-jumbotron header-level='5'>
    <template v-slot:header>
      Previous page prohibition
    </template>
    <template v-slot:lead>
      You tried to go to previous page, which is not allowed in this task. We will redirect the page to Prolific in 5 seconds.
    </template>
  </b-jumbotron>
</template>
<script>
import axios from 'axios'
export default {
  data: function () {
    return {
      total_bonus: 0.0,
      detail: [],
      fields: [
        {key: 'task', label: 'Task No.'},
        {key: 'user_prediction', label: 'Your prediction'},
        {key: 'ground_truth', label: 'Whether reoffend laws?'},
        {key: 'bonus', label: 'Bonus'}
      ]
    }
  },
  methods: {
  },
  mounted () {
    this.$root.websock.close(4001)
    let body = new FormData()
    body.append('subject_id', this.$store.state.subject_id)
    body.append('status', 'prev')
    axios.post(this.$root.server_url + 'submittomtruk', body)
      .then(response => {
        setTimeout(() => {
          window.location.href = response.data.mturk_url
        }, 5000)
      })
      .catch(e => {
        alert('Some error happened!! Please leave comments and submit the HIT on MTurk.')
      })
  }
}
</script>
