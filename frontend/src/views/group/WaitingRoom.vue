<template>
  <b-jumbotron header-level='5'>
    <template v-slot:header>
      Waiting for other
    </template>
    <div class="content-area">
      <p>
        You will start working on 8 recidivism prediction tasks in a group of three people soon. Please wait for another {{numSeats}} of your group members to arrive. <span class="highlight"> Please turn on audio on your device.</span> Once all of the group members arrive, we will notify you with a sound and redirect you to the next page.
      </p>
      <p>
        If no other group member arrives in 5 minutes, we will redirect you back to Prolific.
      </p>
      <p>We will bonus you <b>15 cents per minute</b> for your waiting time. <br>The average waiting time is {{average_waiting_time}} seconds.</p>
      <CountdownTimer :remain_time="300"/>
    </div>
  </b-jumbotron>
</template>
<script>
import axios from 'axios'
import CountdownTimer from '@/components/CountdownTimer.vue'
export default {
  data: function () {
    return {
      group_capacity: 3,
      timeout: null,
      average_waiting_time: null
    }
  },
  components: {
    CountdownTimer
  },
  methods: {
    getRoomName () {
      let body = new FormData()
      body.append('subject_id', this.$store.state.subject_id)
      body.append('condition', this.$store.state.condition) // Must be -1 in the formal test.
      axios.post(this.$root.server_url + 'pairing', body)
        .then(response => {
          this.group_capacity = response.data.group_capacity
          this.average_waiting_time = response.data.average_waiting_time.toFixed(0)
          this.$store.commit('assign_group_id', {group_id: response.data.group_id})
          this.$store.commit('assign_condition', {condition: response.data.condition})
          this.$root.initWebSocket()
        })
    }
  },
  mounted () {
    this.getRoomName()
    this.timeout = setTimeout(() => {
      this.$root.members = []
      this.$root.alarm_sound.play()
      this.$root.websock.close(4001)
      this.$router.push('/FailPairing')
    }, 1000 * 60 * 5) // Could not be successfully paired in 5 minutes.
  },
  computed: {
    numSeats: function () {
      return this.group_capacity - this.$root.members.length
    }
  },
  beforeDestroy () {
    clearInterval(this.timeout)
  }
}
</script>
