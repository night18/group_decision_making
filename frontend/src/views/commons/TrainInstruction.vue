<template>
  <b-jumbotron header-level='5'>
    <template v-slot:header>
      Practice Phase Instruction
    </template>
    <div class="content-area">
      <p>Next, you will be given 9 recidivism risk prediction tasks in this phase. On each task, you will complete the following five steps: </p>
      <ol>
        <li>
          Carefully review the defendant's information.
        </li>
        <li>
          Make your initial prediction on whether the defendant would violate any law in the next two years by yourself.
        </li>
        <li>
          Review the machine learning model's prediction on this defendant.
        </li>
        <li>
          Make your final prediction on the defendant.
        </li>
        <li>
          Review the feedback on whether the defendant actually violated any law in the next two years in reality.
        </li>
      </ol>
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
      axios.get(this.$root.server_url + 'get_train')
        .then(response => {
          this.$store.commit('assign_practice', response.data.task_list)
          this.$router.push('/PracticeTask/' + this.$store.state.practice_task_no)
        })
    }
  }
}
</script>
