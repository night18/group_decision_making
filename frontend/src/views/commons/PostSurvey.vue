<template>
  <b-jumbotron header-level='5'>
    <template v-slot:lead>
      Fantastic, you have completed all prediction tasks in this HIT! Before you submit this HIT, please answer a few survey questions.
    </template>
    <div class="content-area">
      <ol>
        <li>
          <p>How mentally demanding was the task?</p>
          <b-form-radio-group
              v-model="mental_demand"
              name="mental_demand"
              label="Individual radios"
              :options="scale"
              :state="mental_demand_state"
              stacked
            />
        </li>
        <li>
          <p>How physically demanding was the task?</p>
          <b-form-radio-group
              v-model="physical_demand"
              name="physical_demand"
              :options="scale"
              :state="physical_demand_state"
              stacked
            />
        </li>
        <li>
          <p>How hurried or rushed was the pace of the task?</p>
          <b-form-radio-group
              v-model="temporal_demand"
              name="temporal_demand"
              :options="scale"
              :state="temporal_demand_state"
              stacked
            />
        </li>
        <li>
          <p>How successful were you in accomplishing what you were asked to do?</p>
          <b-form-radio-group
              v-model="performance"
              name="performance"
              :options="scale"
              :state="performance_state"
              stacked
            />
        </li>
        <li>
          <p>How hard did you have to work to accomplish your level of performance?</p>
          <b-form-radio-group
              v-model="effort"
              name="effort"
              :options="scale"
              :state="effort_state"
              stacked
            />
        </li>
        <li>
          <p>How insecure, discouraged, irritated, stressed, and annoyed were you?</p>
          <b-form-radio-group
              v-model="frustration"
              name="frustration"
              :options="scale"
              :state="frustration_state"
              stacked
            />
        </li>
        <hr>
        <p>How much do you agree with the following statements?</p>
        <li>
          <p>I'm happy with the timeliness of the information from other members.</p>
          <b-form-radio-group
              v-model="timeline"
              name="timeline"
              :options="agreements"
              :state="timeline_state"
              stacked
            />
        </li>
        <li>
          <p>I'm happy with the precision of the information from other team members. </p>
          <b-form-radio-group
              v-model="precision"
              name="precision"
              :options="agreements"
              :state="precision_state"
              stacked
            />
        </li>
        <li>
          <p>I'm happy with the usefulness of the information from other team members. </p>
          <b-form-radio-group
              v-model="usefulness"
              name="usefulness"
              :options="agreements"
              :state="usefulness_state"
              stacked
            />
        </li>
        <div v-if="this.$store.state.condition !== 0">
          <li>
            <p>I feel like I was collaborating with Devil's Advocate during the task.</p>
            <b-form-radio-group
                v-model="da_collaboration"
                name="da_collaboration"
                :options="agreements"
                :state="da_collaboration_state"
                stacked
              />
          </li>
          <li>
            <p>I'm satisfied with the assistance provided by Devil's Advocate in completing the tasks.</p>
            <b-form-radio-group
                v-model="da_satisfaction"
                name="da_satisfaction"
                :options="agreements"
                :state="da_satisfaction_state"
                stacked
              />
          </li>
          <li>
            <p>I'm pleased with the quality of Devil's Advocate in completing the tasks.</p>
            <b-form-radio-group
                v-model="da_quality"
                name="da_quality"
                :options="agreements"
                :state="da_quality_state"
                stacked
              />
          </li>
          <li>
            <p>I will recommend Devil's Advocate to my friends if they need to complete similar tasks.</p>
            <b-form-radio-group
                v-model="da_recommend"
                name="da_recommend"
                :options="agreements"
                :state="da_recommend_state"
                stacked
              />
          </li>
          <li>
            <p>If given the option, I would use Devil's Advocate to assist me with completing similar decision-making tasks in the future.</p>
            <b-form-radio-group
                v-model="da_future"
                name="da_future"
                :options="agreements"
                :state="da_future_state"
                stacked
              />
          </li>
        </div>
      </ol>
    </div>
    <div class="button-area">
      <b-button variant="primary" name="next" :disabled="!all_confirm" v-on:click="next">Check the bonus</b-button>
    </div>
  </b-jumbotron>
</template>
<script>
import axios from 'axios'
export default {
  data: function () {
    return {
      mental_demand: null,
      physical_demand: null,
      temporal_demand: null,
      performance: null,
      effort: null,
      frustration: null,
      timeline: null,
      precision: null,
      usefulness: null,
      da_collaboration: null,
      da_satisfaction: null,
      da_quality: null,
      da_recommend: null,
      da_future: null,
      scale: [
        { text: 'Very Low', value: 1 },
        { text: 'Below Average', value: 2 },
        { text: 'Average', value: 3 },
        { text: 'Above Average', value: 4 },
        { text: 'Very High', value: 5 }
      ],
      agreements: [
        { text: 'Strongly Disagree', value: 1 },
        { text: 'Disagree', value: 2 },
        { text: 'Undecided', value: 3 },
        { text: 'Agree', value: 4 },
        { text: 'Strongly Agree', value: 5 }
      // ],
      // confidences: [
      //   { text: 'Not confident at all', value: 1 },
      //   { text: 'Mostly not confident', value: 2 },
      //   { text: 'Somewhat confident', value: 3 },
      //   { text: 'Moderately confident', value: 4 },
      //   { text: 'Extremely confident', value: 5 }
      // ],
      // influences: [
      //   { text: 'Not at all influential', value: 1 },
      //   { text: 'Slightly influential', value: 2 },
      //   { text: 'Somewhat influential ', value: 3 },
      //   { text: 'Very influential', value: 4 },
      //   { text: 'Extremely influential', value: 5 }
      // ],
      // features: [
      //   { text: 'Race', value: 'race' },
      //   { text: 'Sex', value: 'sex' },
      //   { text: 'Age', value: 'age' },
      //   { text: 'Priors Crime Count', value: 'prior' },
      //   { text: 'Felony Count before 18', value: 'felony' },
      //   { text: 'Misdemeanor Count before 18', value: 'misdemeanor' },
      //   { text: 'Charge Issue', value: 'charge_reason' },
      //   { text: 'Charge Degree', value: 'charge_degree' }
      ]
    }
  },
  components: {
  },
  methods: {
    next: function () {
      let body = new FormData()
      body.append('subject_id', this.$store.state.subject_id)
      body.append('mental_demand', this.mental_demand)
      body.append('physical_demand', this.physical_demand)
      body.append('temporal_demand', this.temporal_demand)
      body.append('performance', this.performance)
      body.append('effort', this.effort)
      body.append('frustration', this.frustration)
      body.append('timeline', this.timeline)
      body.append('precision', this.precision)
      body.append('usefulness', this.usefulness)
      if (this.$store.state.condition !== 0) {
        body.append('da_collaboration', this.da_collaboration)
        body.append('da_satisfaction', this.da_satisfaction)
        body.append('da_quality', this.da_quality)
        body.append('da_recommend', this.da_recommend)
        body.append('da_future', this.da_future)
      }
      axios.post(this.$root.server_url + 'post_survey', body)
        .then(response => {
          this.$router.push('/BonusSummary')
        })
        .catch(e => {
          this.$alert('Some error happened!! Please leave comments and submit the HIT on MTurk.')
        })
    }
  },
  computed: {
    mental_demand_state () {
      return Boolean(this.mental_demand)
    },
    physical_demand_state () {
      return Boolean(this.physical_demand)
    },
    temporal_demand_state () {
      return Boolean(this.temporal_demand)
    },
    performance_state () {
      return Boolean(this.performance)
    },
    effort_state () {
      return Boolean(this.effort)
    },
    frustration_state () {
      return Boolean(this.frustration)
    },
    timeline_state () {
      return Boolean(this.timeline)
    },
    precision_state () {
      return Boolean(this.precision)
    },
    usefulness_state () {
      return Boolean(this.usefulness)
    },
    da_collaboration_state () {
      return Boolean(this.da_collaboration)
    },
    da_satisfaction_state () {
      return Boolean(this.da_satisfaction)
    },
    da_quality_state () {
      return Boolean(this.da_quality)
    },
    da_recommend_state () {
      return Boolean(this.da_recommend)
    },
    da_future_state () {
      return Boolean(this.da_future)
    },
    all_confirm () {
      if (this.$store.state.condition === 0) {
        return this.mental_demand_state && this.physical_demand_state && this.temporal_demand_state && this.performance_state && this.effort_state && this.frustration_state && this.timeline_state && this.precision_state && this.usefulness_state
      }
      return this.mental_demand_state && this.physical_demand_state && this.temporal_demand_state && this.performance_state && this.effort_state && this.frustration_state && this.timeline_state && this.precision_state && this.usefulness_state && this.da_collaboration_state && this.da_satisfaction_state && this.da_quality_state && this.da_recommend_state && this.da_future_state
    }
  },
  mounted () {
  }
}
</script>
<style>
</style>
