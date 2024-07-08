<template>
  <b-jumbotron header-level='5' ref="top">
    <template v-slot:lead>
      Now let's take a look at all the defendants you have just saw in the six formal tasks. Are your final predictions on them correct?
    </template>
    <div class="content-area">
      <div v-if="$root.is_loading">
        <div class="text-center">
          <b-spinner variant="primary" label="Loading"></b-spinner>
        </div>
      </div>
      <div v-else>
        For the defendant case {{displayed_id}}
        <TaskInfo :defendant="task"/>
        <ul>
          <li>
            The model's prediction is that the defendant <b>{{show_estimation(this.task.model_suggestion)}}</b> reoffend in 2 years.<br>
          </li>
          <li>
            <span v-if="$store.state.group_id !== -1">You and your group members'</span><span v-else>Your</span> final prediction is that the defendant <b>{{show_estimation(this.task.user_prediction)}}</b> reoffend in 2 years.
          </li>
          <li>
            On this case, your final prediction is <b class="highlight">{{show_correct(this.task)}}.</b><br>
          </li>
        </ul>
        <br>
        How much
        <span v-if="show_correct(this.task) === 'correct'"> credit </span>
        <span v-else> responsibility </span>
        you <span v-if="$store.state.condition === 0">, your teammates,</span> and the machine learning model should take for making this {{show_correct(this.task)}} prediction? Please indicate your perceptions below by dragging the point on the pie.
        <pieChart :pie_id="get_id" :condition="$store.state.condition" :credit="show_correct(this.task) === 'correct'" @responsibility="getPieResult"/>
        <div class="button-area">
          <b-button variant="primary" name="next" v-on:click="next">Next</b-button>
        </div>
      </div>
    </div>
  </b-jumbotron>
</template>
<script>
import axios from 'axios'
import TaskInfo from '@/components/TaskInfo.vue'
import PieChart from '@/components/PieChart.vue'
export default {
  data: function () {
    return {
      me: null,
      the_model: null,
      my_teammates: null
    }
  },
  components: {
    TaskInfo,
    PieChart
  },
  props: ['taskid'],
  methods: {
    next: function () {
      if (this.me === null) {
        this.$alert('Please make sure you move the pie chart at least once', 'warning')
      }
      let body = new FormData()
      body.append('subject_id', this.$store.state.subject_id)
      body.append('instance_id', this.$store.state.formal_task[this.get_id].instance_id)
      body.append('task_no', this.get_id)
      body.append('me', this.me)
      body.append('the_model', this.the_model)
      body.append('my_teammates', this.my_teammates)

      axios.post(this.$root.server_url + 'accountability_survey', body)
        .then(response => {
          if (this.displayed_id === this.$store.state.formal_task.length) {
            this.$router.push('/BonusSummary')
          } else {
            this.$router.push('/AccountabilitySurvey/' + this.displayed_id)
            let el = this.$refs.top
            if (typeof el !== 'undefined') {
              el.scrollIntoView({behavior: 'smooth'})
            }
          }
        })
    },
    show_estimation: function (estimation) {
      if (estimation === 'True') {
        return 'will'
      } else if (estimation === 'False') {
        return 'will not'
      }
    },
    show_correct: function (task) {
      if (task.user_prediction === task.ground_truth) {
        return 'correct'
      } else {
        return 'wrong'
      }
    },
    getPieResult: function (data) {
      const responsibility = data.responsibility
      for (let i = 0; i < responsibility.length; i++) {
        let res = responsibility[i]
        if (res.subject === 'Me') {
          this.me = res.value
        } else if (res.subject === 'The model') {
          this.the_model = res.value
        } else if (res.subject === 'My teammates') {
          this.my_teammates = res.value
        }
      }
    }
  },
  computed: {
    displayed_id: function () {
      return parseInt(this.taskid) + 1
    },
    get_id: function () {
      return parseInt(this.taskid)
    },
    task: function () {
      return this.$store.state.formal_task[this.get_id]
    }
  },
  mounted () {
  }
}
</script>
<style>
</style>
