<template>
  <b-jumbotron header-level='5'>
    <template v-slot:header>
      Instructions
    </template>
    <div class="content-area">
      <p>
        In this HIT, you will be asked to complete a sequence of 15 recidivism risk prediction tasks. In each task, you need to review a criminal defendant’s profile and then predict whether the defendant would violate any law again within the next two years.
      </p>
      <p>Specifically, the 15 prediction tasks in this HIT are separated into a <u>practice phase (9 tasks)</u> and a <u>formal phase (6 tasks)</u>:</p>
      <ol>
        <li>
          In the <u>practice phase</u>, you will be asked to take practice on 9 recidivism risk prediction tasks. We aim to help you get some ideas about how to make accurate recidivism risk predictions. So, at the end of each practice task, we will let you know whether the defendant in that task actually violated any laws or not in reality.
        </li>
        <li>
          In the <u>formal phase</u>, you will make recidivism risk predictions for real. This means that on each formal task, you won’t be provided with any feedback on whether the defendant actually violated any laws or not in reality. However, we will check whether your prediction in each formal task is correct or not at the end of the HIT---for each correct prediction you make on the formal task, you will get a bonus payment of $0.4!
        </li>
      </ol>
      We will give you more instructions about the formal phase after you finish completing all tasks in the practice phase.<br>
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
      this.$router.push('/NoTaskInstruction')
    }
  }
}
</script>
