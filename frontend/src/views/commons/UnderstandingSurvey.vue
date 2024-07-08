<template>
  <b-jumbotron header-level='5'>
    <template v-slot:lead>
      Fantastic, you have completed all prediction tasks in this HIT! Before you submit this HIT, please answer a few survey questions.
    </template>
    <div class="content-area">
      <ol>
        <li>
          <p>
            Based on your understandings of how the machine learning model makes its predictions, how much influence the defendant's <span class="highlight">race</span> has on the model's prediction about the defendant?
            <b-form-radio-group
              v-model="race"
              name="race"
              :options="influences"
              stacked
            />
          </p>
        </li>
        <li>
          <p>
            Based on your understandings of how the machine learning model makes its predictions, how much influence the defendant's <span class="highlight">sex</span> has on the model's prediction about the defendant?
            <b-form-radio-group
              v-model="sex"
              name="sex"
              :options="influences"
              stacked
            />
          </p>
        </li>
        <li>
          <p>
            Based on your understandings of how the machine learning model makes its predictions, how much influence the defendant's <span class="highlight">age</span> has on the model's prediction about the defendant?
            <b-form-radio-group
              v-model="age"
              name="age"
              :options="influences"
              stacked
            />
          </p>
        </li>
        <li>
          <p>
            Based on your understandings of how the machine learning model makes its predictions, how much influence the defendant's <span class="highlight">priors crime count</span> has on the model's prediction about the defendant?
            <b-form-radio-group
              v-model="prior"
              name="prior"
              :options="influences"
              stacked
            />
          </p>
        </li>
        <li>
          <p>
            Based on your understandings of how the machine learning model makes its predictions, how much influence the defendant's <span class="highlight">felony count before 18</span> has on the model's prediction about the defendant?
            <b-form-radio-group
              v-model="felony"
              name="felony"
              :options="influences"
              stacked
            />
          </p>
        </li>
        <li>
          <p>
            Based on your understandings of how the machine learning model makes its predictions, how much influence the defendant's <span class="highlight">misdemeanor count before 18</span> has on the model's prediction about the defendant?
            <b-form-radio-group
              v-model="misdemeanor"
              name="misdemeanor"
              :options="influences"
              stacked
            />
          </p>
        </li>
        <li>
          <p>
            Based on your understandings of how the machine learning model makes its predictions, how much influence the defendant's <span class="highlight">current charge degree</span> has on the model's prediction about the defendant?
            <b-form-radio-group
              v-model="charge_degree"
              name="charge_degree"
              :options="influences"
              stacked
            />
          </p>
        </li>
        <li>
          <p>
            Based on your understandings of how the machine learning model makes its predictions, how much influence the defendant's <span class="highlight">current charge issue</span> has on the model's prediction about the defendant?
            <b-form-radio-group
              v-model="charge_issue"
              name="charge_issue"
              :options="influences"
              stacked
            />
          </p>
        </li>
      </ol>
    </div>
    <div class="button-area">
      <b-button variant="primary" name="next" v-on:click="next">Next</b-button>
    </div>
  </b-jumbotron>
</template>
<script>
import axios from 'axios'
export default {
  data: function () {
    return {
      influences: [
        { text: '1 - Not at all influential', value: 1 },
        { text: '2 - Slightly influential', value: 2 },
        { text: '3 - Somewhat influential ', value: 3 },
        { text: '4 - Very influential', value: 4 },
        { text: '5 - Extremely influential', value: 5 }
      ],
      race: null,
      sex: null,
      age: null,
      prior: null,
      felony: null,
      misdemeanor: null,
      charge_degree: null,
      charge_issue: null
    }
  },
  components: {
  },
  methods: {
    next: function () {
      if (this.race === null || this.sex === null || this.age === null || this.prior === null || this.felony === null || this.misdemeanor === null || this.charge_degree === null || this.charge_issue === null) {
        this.$alert('Please make sure you answer all the question', '', 'warning')
        return
      }
      let body = new FormData()
      body.append('subject_id', this.$store.state.subject_id)
      body.append('race', this.race)
      body.append('sex', this.sex)
      body.append('age', this.age)
      body.append('prior', this.prior)
      body.append('felony', this.felony)
      body.append('misdemeanor', this.misdemeanor)
      body.append('charge_degree', this.charge_degree)
      body.append('charge_issue', this.charge_issue)
      axios.post(this.$root.server_url + 'understanding_survey', body)
        .then(response => {
          this.$router.push('/AccountabilitySurvey/0')
        })
        .catch(e => {
          this.$alert('Some error happened!! Please leave comments and submit the HIT on MTurk.', '', 'warning')
        })
    }
  },
  computed: {
  },
  mounted () {
    let body = new FormData()
    let instance_ids = []
    for (let i = 0; i < this.$store.state.formal_task.length; i++) {
      instance_ids.push(this.$store.state.formal_task[i].instance_id)
    }
    body.append('instance_ids', instance_ids)
    axios.post(this.$root.server_url + 'get_correct_answer', body)
      .then(response => {
        let answers = response.data.task_list
        this.$store.commit('formal_truth', answers)
      })
      .catch(e => {
        console.error(e)
        this.$alert('Could not get the ground truth from the server.')
      })
  }
}
</script>
<style>
</style>
