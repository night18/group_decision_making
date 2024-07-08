<template>
  <b-navbar id="nav-bar" toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand>Parole Judgement Test</b-navbar-brand>
    <b-nav class="ml-auto">
      <b-navbar-brand :class="avatarShowed" class="avatar-area">
        <v-animal size="40px" :name="avatarNamechanged" :color="avatarColorHexchanged" class="avatar-icon"/>
        {{avatarColorchanged}} {{avatarNamechanged}}
      </b-navbar-brand>
    </b-nav>
  </b-navbar>
</template>
<script>
import { colors } from '@/components/constants'
export default {
  name: 'nav-bar',
  data: function () {
    return {
    }
  },
  computed: {
    avatarNamechanged () {
      return this.$store.state.avatar_name
    },
    avatarColorchanged () {
      return this.$store.state.avatar_color
    },
    avatarColorHexchanged () {
      return colors[this.$store.state.avatar_color]
    },
    avatarShowed () {
      return (this.avatarNamechanged != null) ? 'show_avatar' : 'hide_avatar'
    }
  }
}
</script>
<style>
  .show_avatar {
    visibility: visible;
  }

  .hide_avatar {
    visibility: hidden;
  }
</style>
