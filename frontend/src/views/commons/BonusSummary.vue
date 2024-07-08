<template>
  <b-jumbotron header-level='5'>
    <template v-slot:header>
      That's all!
    </template>
    <template v-slot:lead>
      Fantastic! You've just completed all tasks in this HIT! Thank you!
    </template>
    <div class="content-area">
      <p>
        The amount of bonus you got in phase 2 is <b>${{total_bonus}}</b>.<br>
        Among them, a  ${{waiting_bonus}} bonus is because you spend {{waiting_time}} seconds in the waiting room.<br>
        The table below shows the detailed information about your bonus.
      </p>
      <b-table :items="detail" :fields="fields" class="text-center bonus_table"></b-table>
      <hr class="my-4">
    </div>
    <div class="button-area">
      <h5>Please push the button below to submit the task!</h5>
      <b-button variant="primary" name="submit" v-on:click="submit">Submit Task</b-button>
    </div>
  </b-jumbotron>
</template>
<script>
import axios from 'axios'
export default {
  data: function () {
    return {
      total_bonus: 0.0,
      waiting_time: null,
      waiting_bonus: null,
      detail: [],
      fields: [
        {key: 'task', label: 'Task No.'},
        {key: 'user_prediction', label: 'Group prediction'},
        {key: 'ground_truth', label: 'Whether reoffend laws?'},
        {key: 'bonus', label: 'Bonus'}
      ]
    }
  },
  methods: {
    submit: function (event) {
      let body = new FormData()
      body.append('subject_id', this.$store.state.subject_id)
      body.append('status', 'success')
      axios.post(this.$root.server_url + 'submittomtruk', body)
        .then(response => {
          window.location.href = response.data.mturk_url
        })
        .catch(e => {
          alert('Some error happened!! Please leave comments and submit the HIT on MTurk.')
        })
    },
    boolean2text: function (boolean) {
      if (boolean === 'True') {
        return 'Reoffend'
      } else if (boolean === 'False') {
        return 'Not Reoffend'
      } else {
        return 'Tie'
      }
    }
  },
  mounted () {
    let body = new FormData()
    body.append('subject_id', this.$store.state.subject_id)
    axios.post(this.$root.server_url + 'show_bonus', body)
      .then(response => {
        let tasks = response.data.detail
        for (let i = 0; i < tasks.length; i++) {
          let task = tasks[i]
          this.detail.push({
            task: task.task,
            user_prediction: this.boolean2text(task.user_prediction),
            ground_truth: this.boolean2text(task.ground_truth),
            bonus: task.bonus
          })
        }
        this.total_bonus = response.data.total_bonus
        this.waiting_time = response.data.waiting_time.toFixed(0)
        this.waiting_bonus = response.data.waiting_bonus
      })
  }
}
</script>
