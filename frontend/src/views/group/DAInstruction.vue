<template>
  <b-jumbotron header-level='5'>
    <template v-slot:header>
      Devil's advocate
    </template>
    <div class="content-area">
      <b-row>
        <b-col cols="3">
          <img width="90%" style="margin: 0 auto;" :src="imageSrc">
        </b-col>
        <b-col cols="9">
          <p>
            In each task in the formal phase, an AI chatbot will be presented to you as an additional “member” of your group to help you carefully deliberate on the defendant's case. This AI chatbot is again developed by AI4Law, and it is designed to play the role of a devil's advocate, i.e., it is designed to challenge some aspects of your decision making processes to ensure that you conduct a comprehensive evaluation of the defendant's case and make an informed decision.
          </p>
          <p>
            In a world where justice prevails, diverse opinions are essential for fair and well-informed judgments. The AI-based Devil's Advocate you will be interacting with in the formal phase tasks embodies this principle, bringing a unique and comprehensive viewpoint to every case. This AI-based Devil's Advocate is programmed to explore alternative scenarios, question assumptions, and identify potential gaps in evidence, thus empowering your group with an extensive spectrum of considerations. By interacting with this AI-based Devil's Advocate, your group may be able to focus your discussions on key issues, leading to more efficient and effective deliberations and ultimately fairer and more equitable decisions.
          </p>
        </b-col>
      </b-row>
    </div>
    <div class="button-area">
       <b-button variant="primary" name="next" v-on:click="next">Continue</b-button>
    </div>
  </b-jumbotron>
</template>
<script>
// import axios from 'axios'
import gavelImage from '@/assets/devil.png'
export default {
  data: function () {
    return {
      avatarName: null,
      avatarColor: null,
      avatarColorHex: null,
      imageSrc: gavelImage
    }
  },
  methods: {
    next: function () {
      let body = new FormData()
      body.append('subject_id', this.$store.state.subject_id)
      body.append('avatar_name', this.avatarName)
      body.append('avatar_color', this.avatarColor)
      this.$router.push('/FormalTask/' + this.$store.state.formal_task_no)
    }
  },
  computed: {
  },
  mounted () {
  }
}
</script>
<style>
.member-card {
  display: inline-block;
  padding: 4px 5px;
  background-color: #e5e5e5;
  line-height: 20px;
  border-radius: 5px;
  text-align: center;
  margin-right: 2px;
  margin-bottom: 2px;
}

.devil_background {
  background-color: #8b0000;
  color: white;
}
</style>
