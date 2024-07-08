<template>
  <b-jumbotron header-level='5'>
    <template v-slot:header>
      Group Phase Instruction (1/2)
    </template>
    <div class="content-area">
      <p>Now, we are about to move on to the group phase. As we told you before, you will be assigned to a group of three people, and as a group, you will be working on 8 recidivism prediction tasks in this phase. For each of these tasks, you need to follow the following steps:</p>
      <ol>
        <li>
          Carefully review the defendant's profile and make your initial prediction on whether this defendant will reoffend in the next two years.
        </li>
        <li>
          Review the machine learning model's prediction on this defendant and share your thoughts on whether this defendant will reoffend in the next two years with other members of your group, using the chat function provided to you on the interface.
        </li>
        <li>
          Discuss with other members in your group, and vote for whether you think the defendant will reoffend in the next two years. The final prediction of your group will be the majority vote of all members in the group. If the ballots for <u>reoffend</u> and <u>not reoffend</u> are the same, your group's final prediction is a tie.
        </li>
      </ol>
      <p>You will see more detailed instructions on the next page. </p>
      <p>As a reminder, for each group task, you can earn <b>$0.4</b> as an additional bonus only if your group's final prediction is correct. You will not earn the bonus if the group's final prediction is a tie.</p>
      <p>To protect your identity, we would assign you an avatar to represent you in your group throughout the rest of this HIT. If you are not satisfied with the assigned avatar, please click the <b>Refresh</b> button to get a new one.</p>
    </div>
    <div class="avatar-area">
      Your anonymous avatar is:<br>
      <v-animal size="40px" :name="avatarName" :color="avatarColorHex" class="avatar-icon"/>
      {{avatarColor}} {{avatarName}}
      <b-button size="sm" variant='warning' name="reroll" v-on:click="changeAvatar">Refresh</b-button>
    </div>
    <div class="button-area">
       <b-button variant="primary" name="next" v-on:click="next">Continue</b-button>
    </div>
  </b-jumbotron>
</template>
<script>
import axios from 'axios'
import { animals, colors } from '@/components/constants'
export default {
  data: function () {
    return {
      avatarName: null,
      avatarColor: null,
      avatarColorHex: null
    }
  },
  methods: {
    next: function () {
      let body = new FormData()
      body.append('subject_id', this.$store.state.subject_id)
      body.append('avatar_name', this.avatarName)
      body.append('avatar_color', this.avatarColor)
      axios.post(this.$root.server_url + 'record_avatar', body)
        .then(response => {
          this.$store.state.avatar_name = this.avatarName
          this.$store.state.avatar_color = this.avatarColor
          this.$router.push('/GroupInstruction')
          // this.$router.push('/NetiquetteRule')
        })
    },
    changeAvatar () {
      const keys = Object.keys(colors)
      this.avatarName = animals[(animals.length * Math.random()) << 0]
      this.avatarColor = keys[(keys.length * Math.random()) << 0]
      this.avatarColorHex = colors[this.avatarColor]
    }
  },
  computed: {
  },
  mounted () {
    this.changeAvatar()
  }
}
</script>
<style>
</style>
