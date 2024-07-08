<template>
  <b-jumbotron header-level='5'>
    <template v-slot:lead>
      First, please answer a few simple demographic survey questions:
    </template>
    <div class="content-area">
      <ol>
        <li>
          <p>How much knowledge do you have in machine learning?</p>
          <b-form-radio-group
            v-model = "Q1"
            name = "Q1"
            :options="competence"
            stacked
          />
        </li>
        <li>
          <p>What gender do you identify as?</p>
          <b-form-radio-group
            v-model = "Q2"
            name = "Q2"
            :options="gender"
            stacked
          />
        </li>
        <li>
          <p>What is your age?</p>
          <b-form-radio-group
            v-model = "Q3"
            name = "Q3"
            :options="age"
            stacked
          />
        </li>
        <li>
          <p>What race do you identify as?</p>
          <b-form-radio-group
            v-model = "Q4"
            name = "Q4"
            :options="race"
            stacked
          />
        </li>
        <li>
          <p>What is the highest degree or level of education you have completed?</p>
          <b-form-radio-group
            v-model = "Q5"
            name = "Q5"
            :options="education"
            stacked
          />
        </li>
        <!-- <li>
          <p>Which of the following times work the best for you for participating in a research study? Please select all that apply.</p>
          <b-form-checkbox-group
            v-model="Q6"
            name="Q6"
            :options="time"
            :state="Q6_state"
            stacked
          ></b-form-checkbox-group>
          <b-form-invalid-feedback :state="Q6_state">Please select at least one</b-form-invalid-feedback>
        </li> -->
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
      competence: [
        { text: '(No competence – no experience in machine learning)', value: '1' },
        { text: '(Low competence – little experience in machine learning) ', value: '2' },
        { text: '(Average level of competence – some experience in machine learning)', value: '3' },
        { text: '(Moderately high level of competence - good amount of experience in machine learning)', value: '4' },
        { text: '(High level of competence - extensive experience in machine learning) ', value: '5' }
      ],
      gender: [
        { text: 'Female', value: '1' },
        { text: 'Male', value: '2' },
        { text: 'Non-Binary', value: '3' },
        { text: 'Prefer not to say', value: '4' }
      ],
      age: [
        { text: 'Under 18', value: '1' },
        { text: '18 - 24 years old', value: '2' },
        { text: '25 - 34 years old', value: '3' },
        { text: '35 - 44 years old', value: '4' },
        { text: '45 - 54 years old', value: '5' },
        { text: 'Over 55 yeats old', value: '6' }
      ],
      race: [
        { text: 'Asian', value: '1' },
        { text: 'Black', value: '2' },
        { text: 'White', value: '3' },
        { text: 'Latino or Hispanic', value: '4' },
        { text: 'Native Hawaiian or Pacific Islander', value: '5' },
        { text: 'Other', value: '6' },
        { text: 'Prefer not to say', value: '7' }
      ],
      education: [
        { text: 'Some High School', value: '1' },
        { text: 'High School', value: '2' },
        { text: 'Bachelor\'s Degree', value: '3' },
        { text: 'Master\'s Degree', value: '4' },
        { text: 'Ph.D. or higher', value: '5' },
        { text: 'Prefer not to say', value: '6' }
      ],
      time: [
        {text: '(Eastern Time (US & Canada)) 10 am - 11 am / (Pacific Time (US & Canada)) 7 am - 8 am', value: '900'},
        {text: '(Eastern Time (US & Canada)) 2 pm - 3 pm / (Pacific Time (US & Canada)) 11 am - 12 pm', value: '1200'},
        {text: '(Eastern Time (US & Canada)) 6 pm - 7 pm / (Pacific Time (US & Canada)) 3 pm - 4 pm', value: '1500'}
      ],
      Q1: null,
      Q2: null,
      Q3: null,
      Q4: null,
      Q5: null,
      Q6: []
    }
  },
  methods: {
    next: function () {
      let body = new FormData()
      body.append('subject_id', this.$store.state.subject_id)
      body.append('Q1', this.Q1)
      body.append('Q2', this.Q2)
      body.append('Q3', this.Q3)
      body.append('Q4', this.Q4)
      body.append('Q5', this.Q5)
      body.append('Q6', this.Q6)

      axios.post(this.$root.server_url + 'pre_survey', body)
        .then(response => {
          this.$store.commit('assign_qualified', response.data.task_list)
          this.$router.push('/QualificationInstruction')
          // this.$router.push('/HitInstruction')
        })
        .catch(e => {
          this.$alert('Some error happened!! Please leave comments and submit the HIT on MTurk.')
        })
    }
  },
  computed: {
    Q6_state: function () {
      return this.Q6.length >= 1
    }
  },
  mounted () {
  }
}
</script>
<style>
</style>
