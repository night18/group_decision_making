<template>
  <b-jumbotron header-level='5'>
    <template v-slot:header>
      Instructions
    </template>
    <div class="content-area">
      <p>Now let’s take a look at what information you will be seeing in defendants’ profiles in order to predict recidivism risk for them.</p>
      <p>In each task, you will see the profile of a criminal defendant who was arrested in Broward County, Florida, between 2013 and 2014. An example profile is shown below. You can hover on each property of the crime report to see what that property stands for.</p>
      <TaskInfo :defendant="defendant"/>
      <p>You are asked to predict whether this defendant would violate any laws again in the next two years.</p>
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
      defendant: {
        race: 'White',
        sex: 'Male',
        age: '24',
        prior: '0',
        felony: '0',
        misdemeanor: '1',
        charge_reason: 'Theft',
        charge_degree: 'misdemeanor',
        charge_explain: 'The taking of another person\'s property worth less than $300.'
      }
    }
  },
  components: {
    TaskInfo
  },
  methods: {
    next: function () {
      this.$router.push('/NoTrainInstruction')
    }
  }
}
</script>
