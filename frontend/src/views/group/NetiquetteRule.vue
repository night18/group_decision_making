<template>
  <b-jumbotron header-level='5'>
    <template v-slot:header>
      Discussion Netiquette and Rules
    </template>
    <template v-slot:lead>
      In the next 8 tasks, you will need to discuss with other members of your group and vote for a prediction for each defendant that you see. To encourage a safe and healthy discussion environment, we'd like to remind you of a few rules you should follow during the discussion:
    </template>
    <div class="content-area">
      <ol>
        <li>Do <b>NOT</b> give out any of your personal information during the discussion. This includes your full name, address, email address, or phone number.</li>
        <li>Respect other people during the discussion. You might have different opinions from other people in your group on some defendants. Please communicate your opinions to others in a rational way. Do not verbally abuse, attack, embarrass, or threaten anyone else in the chat room.</li>
      </ol>
      <p>Agreement</p>
      <b-form-checkbox
        id="read"
        v-model="is_read"
        name="read"
        value="accepted"
        unchecked-value="not_accepted">
        I have read and agree to the discussion netiquette and rules.
      </b-form-checkbox>
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
      is_read: 'not_accepted'
    }
  },
  methods: {
    next: function () {
      if (this.is_read !== 'accepted') {
        this.$alert('Please read and agree the discussion netiquette and rules before going to next step!', '', 'warning')
      } else {
        this.$router.push('/WaitingRoom')
      }
    }
  }
}
</script>
