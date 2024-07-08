<template>
  <b-jumbotron header-level='5'>
    <template v-slot:lead>
      Tasks Summary
    </template>
    <div class="content-area">
      <p>Congratulations! You have just completed the individual phase!</p>
      <p>Before moving on to the group phase, let's take a quick look at how accurate your recidivism risk predictions are in the individual phase. Each row represents one individual task. If the cell is red, it represents the prediction is incorrect. If you are interested in revisiting the defendant's profile in a particular task, click on the "Show details" button for that task.</p>
      <b-table :items="details" :fields="fields" striped class='text-center'>
        <template #cell(action)="row">
          <b-button size="sm" @click="row.toggleDetails">
            {{row.detailsShowing ? 'Hide': 'Show' }} Details
          </b-button>
        </template>
        <template #row-details="row">
          <TaskInfo :defendant="row.item.defendant"/>
        </template>
      </b-table>
    </div>
    <div class="button-area">
       <b-button variant="primary" name="next" v-on:click="next">Continue</b-button>
    </div>
  </b-jumbotron>
</template>
<script>
import TaskInfo from '@/components/TaskInfo.vue'
export default {
  data: function () {
    return {
      details: [],
      fields: [
        {key: 'task', label: 'Task No.'},
        {key: 'initial_answer', label: 'Your initial prediction'},
        {key: 'final_answer', label: 'Your final prediction'},
        {key: 'model_suggestion', label: 'Model\'s prediction'},
        {key: 'ground_truth', label: 'Whether reoffend laws?'},
        {key: 'action', label: 'Action'}
      ]
    }
  },
  components: {
    TaskInfo
  },
  methods: {
    next: function () {
      this.$router.push('/FormalInstruction')
    },
    boolean2text: function (boolean) {
      if (boolean === 'True') {
        return 'Reoffend'
      } else {
        return 'Not Reoffend'
      }
    }
  },
  mounted () {
    for (let i = 0; i < this.$store.state.practice_task.length; i++) {
      let task = this.$store.state.practice_task[i]
      if (task.condition !== -2) {
        let initial_warning = ''
        let final_warning = ''
        let model_warning = ''
        if (task.ground_truth !== task.initial_answer) {
          initial_warning = 'danger'
        }
        if (task.ground_truth !== task.final_answer) {
          final_warning = 'danger'
        }
        if (task.ground_truth !== task.model_suggestion) {
          model_warning = 'danger'
        }
        this.details.push({
          task: i + 1,
          initial_answer: this.boolean2text(task.initial_answer),
          final_answer: this.boolean2text(task.final_answer),
          model_suggestion: this.boolean2text(task.model_suggestion),
          ground_truth: this.boolean2text(task.ground_truth),
          defendant: task,
          _cellVariants: { initial_answer: initial_warning, final_answer: final_warning, model_suggestion: model_warning }
        })
      }
    }
  }
}
</script>
