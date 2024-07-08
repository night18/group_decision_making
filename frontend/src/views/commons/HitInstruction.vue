<template>
  <b-jumbotron header-level='5'>
    <template v-slot:header>
      Instructions
    </template>
    <div class="content-area">
      <p>
        In this HIT, you will be asked to complete a sequence of 26 recidivism risk prediction tasks. In each task, you need to review a criminal defendant's profile and then predict whether the defendant would violate any law again within the next two years.
      </p>
      <p>Specifically, the 26 prediction tasks in this HIT are separated into a <u>individual phase (18 tasks)</u> and a <u>group phase (8 tasks)</u>:</p>
      <ol>
        <li>
          In the <u>individual phase</u>, you will be asked to complete the recidivism risk prediction tasks on <u>your own</u>. In the later 9 tasks, we aim to help you get some ideas about how to make accurate recidivism risk predictions and gain some experience with the machine learning model. So, at the end of each practice task, we will let you know whether the defendant in that task actually violated any laws or not in reality.
        </li>
        <li>
          In the <u>group phase</u>, you will be assigned to <b>a group of three people</b> (who are all workers from Amazon Mechanical Turk), and as a group, you will make recidivism risk predictions for real. This means that on each group task, you won't be provided with any feedback on whether the defendant actually violated any laws or not in reality. However, we will check whether your prediction in each group task is correct or not at the end of the HIT---for each correct prediction you make on the group task, you will get a bonus payment of $0.4!
        </li>
      </ol>
      We will give you more instructions about the group phase after you finish completing all tasks in the practice phase.<br>
    </div>
    <div class="button-area">
       <b-button variant="primary" name="next" v-on:click="next">Continue</b-button>
    </div>
  </b-jumbotron>
</template>
<script>
export default {
  data: function () {
    return {
    }
  },
  methods: {
    next: function () {
      this.$router.push('/TaskInstruction')
    }
  }
}
</script>
