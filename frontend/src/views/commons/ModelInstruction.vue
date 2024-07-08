<template>
  <b-jumbotron header-level='5'>
    <template v-slot:header>RiskComp</template>
    <template v-slot:lead>
      In this HIT, a machine learning model, RiskComp will be presented to you to help you make your prediction.
    </template>
    <div class="content-area">
      <b-row>
        <b-col cols="3">
          <img width="90%" style="margin: 0 auto;" :src="imageSrc">
        </b-col>
        <b-col cols="9">
          <p>RiskComp is a machine learning model developed to predict the reoffend rate of defendants and facilitate more informed decisions on conditional release. It was developed by AI4Law, a non-profit organization dedicated to leveraging artificial intelligence in the legal system, aiming to help judges and juries make more informed decisions.</p>
          <p>More specifically, RiskComp draws upon an extensive dataset of relevant properties of defendants, including the defendant's past criminal records and demographics, such as their race, gender, and age, to generate an assessment of the defendant's reoffend risk.</p>
          <p>Note that RiskComp is not intended to replace human judgment, but rather to complement and augment it. RiskComp is designed to be a tool that assists judges and juries in making well-informed decisions, fostering a judicial process that is grounded in both data-driven insights and human empathy.</p>
          <p>By embracing technology thoughtfully and responsibly, AI4Law strives to create a legal landscape that values fairness, equity, and compassion while acknowledging and addressing any potential biases that may arise. Together with the partners in the legal community, AI4Law is committed to advancing RiskComp and promoting the cause of justice in a rapidly evolving world.</p>
        </b-col>
      </b-row>
    </div>
    <div class="button-area">
       <b-button variant="primary" name="next" v-on:click="next">Continue</b-button>
    </div>
  </b-jumbotron>
</template>
<script>
import gavelImage from '@/assets/gavel.png'
export default {
  data: function () {
    return {
      imageSrc: gavelImage
    }
  },
  methods: {
    next: function () {
      this.$router.push('/TrainInstruction')
    }
  }
}
</script>
