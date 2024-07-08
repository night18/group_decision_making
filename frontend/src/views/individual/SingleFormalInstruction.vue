<template>
  <b-jumbotron header-level='5'>
    <template v-slot:header>
      Formal Phase Instruction
    </template>
    <div class="content-area">
      <p>Now, we are about to move on to the formal phase. You will be working on 6 recidivism prediction tasks in this phase. For each of these tasks, you need to follow the following steps:</p>
      <ol>
        <li>
          Carefully review the defendant’s profile and the machine learning model’s prediction of this defendant.
        </li>
        <li>
          Make a prediction on whether the defendant will reoffend in the next two years.
        </li>
      </ol>
      <p>As a reminder, for each formal task, you can earn $0.4 as an additional bonus if your prediction is correct.</p>
    </div>
    <div class="button-area">
       <b-button variant="primary" name="next" v-on:click="next">Continue</b-button>
    </div>
  </b-jumbotron>
</template>
<script>
import axios from 'axios'
export default {
  data: function () {
    return {
    }
  },
  methods: {
    next: function () {
      let body = new FormData()
      body.append('subject_id', this.$store.state.subject_id)
      axios.get(this.$root.server_url + 'get_formal')
        .then(response => {
          this.$store.commit('assign_condition', {condition: 1})
          this.$store.commit('assign_formal', response.data.task_list)
          this.$router.push('/SingleFormalTask/0')
        })
    }
  },
  computed: {
  },
  mounted () {
  }
}
</script>
<style>
</style>
