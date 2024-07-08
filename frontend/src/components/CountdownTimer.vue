<template>
  <div class="text-center">
    {{get_minutes}} : {{get_seconds}}
  </div>
</template>
<script>
export default {
  name: 'CountdownTimer',
  props: {
    remain_time: {
      type: Number,
      default: 300
    }
  },
  data: function () {
    return {
      timer: null,
      counter: this.remain_time
    }
  },
  methods: {
    countdown: function () {
      this.counter--
      if (this.counter === 0) {
        clearInterval(this.timer)
      }
    }
  },
  computed: {
    get_hours: function () {
      // return parseInt(this.counter / (1000 * 60 * 60))
      return 0
    },
    get_minutes: function () {
      return parseInt(this.counter / 60 - this.get_hours * 60).toLocaleString('en-US', { minimumIntegerDigits: 2, useGrouping: false })
    },
    get_seconds: function () {
      return parseInt((this.counter) - (this.get_hours) * 3600 - (this.get_minutes) * 60).toLocaleString('en-US', { minimumIntegerDigits: 2, useGrouping: false })
    }
  },
  mounted () {
    this.timer = setInterval(this.countdown, 1000)
  },
  beforeDestroy () {
    clearInterval(this.timer)
  }
}
</script>
