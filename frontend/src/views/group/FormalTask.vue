<template>
  <b-jumbotron header-level='1'>
    <template v-slot:lead>
      Group test ({{displayed_id}}/{{$store.state.formal_task.length}})
      <!-- <p v-if="all_initial && $store.state.subject_id === $root.devil" class="highlight">You are Devil's Advocate. Please argue against the <span v-if="$store.state.condition === 1 || $store.state.condition === 2">machine learning model's</span><span v-if="$store.state.condition === 3 || $store.state.condition === 4">group's initial majority</span> prediction to help the group analyze the case more critically. That is, please propose some possibility that the defendant might {{against_answer}} reoffend the law within two years.</p> -->
    </template>
    <div v-if="$root.is_loading">
      <div class="text-center">
        <b-spinner variant="primary" label="Loading"></b-spinner>
      </div>
    </div>
    <div v-else>
      <b-row>
        <b-col fluid>
          <div class="content-area task-area">
            <div>
              <p>Please review the profile below and predict whether the defendant would reoffend in the next two years.</p>
              <TaskInfo :defendant="$store.state.formal_task[get_id]"/>
              <div class="answer-area">
                <p>
                  <b>Make Your Initial Prediction</b>
                </p>
                <p>Do you think this defendant will reoffend within 2 years?</p>
                <b-form-group v-slot="{ ariaDescribedby }" :disabled="is_predicted">
                 <b-form-radio v-model="initial_answer" :aria-describedby="ariaDescribedby" value="True">The defendant <b>will</b> reoffend within two years</b-form-radio>
                 <b-form-radio v-model="initial_answer" :aria-describedby="ariaDescribedby" value="False">The defendant <b>will not</b> reoffend within two years</b-form-radio>
               </b-form-group>
               <b-button v-if="!is_predicted" variant="primary" name="next" v-on:click="record_initial">Start Group Discussion</b-button>
              </div>
            </div>
            <div v-if="is_predicted">
              <div v-if="!all_initial">
                Waiting for other members to make their initial prediction.
              </div>
              <div v-else>
                <div class="suggestion-area">
                  <p>
                    <b>Machine learning Prediction:</b>
                  </p>
                  Our machine learning model predicts that this defendant will <span class="highlight">{{ml_suggestion}}</span> reoffend in 2 years.
                </div>
                <div class="answer-area">
                  <div v-if="all_ready">
                    <p>
                      <b>Vote for Your Final Prediction</b>
                    </p>
                    <p>Do you think this defendant will reoffend within 2 years?</p>
                    <b-form-group v-slot="{ ariaDescribedby }" :disabled="is_submitted">
                     <b-form-radio v-model="final_answer" :aria-describedby="ariaDescribedby" value="True">The defendant <b>will</b> reoffend within two years</b-form-radio>
                     <b-form-radio v-model="final_answer" :aria-describedby="ariaDescribedby" value="False">The defendant <b>will not</b> reoffend within two years</b-form-radio>
                   </b-form-group>
                  </div>
                  <div v-else>
                    <p class="highlight" v-if="!click_ready && disable_ready">
                      Please spend at least one minute to discuss this defendant's case with other members in your group.
                    </p>
                    <p v-if="!disable_ready && !click_ready">
                      If you are ready to make your final prediction, click the button below. You will only be able to cast your final vote when all members of your group indicate that they are ready to vote.
                    </p>
                    <p v-if="click_ready">
                      You will be able to cast your final vote once all members of your group indicate that they are ready to vote.
                    </p>
                    <b-button ref="ready" variant="primary" name="ready" :disabled="disable_ready" v-on:click="submit_ready">{{vote_button_text}}</b-button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </b-col>
        <b-col cols='6' v-if="all_initial">
          <ChatRoom ref="chat" :get_id="get_id" :my_message="my_message" @typing="typing"/>
        </b-col>
      </b-row>
      <div class="button-area" v-if="all_ready">
        <b-overlay
          :show=busy
          rounded
          opacity="0.6"
          spinner-small
          spinner-variant="primary"
          >
          <b-button ref="confirm" variant="primary" name="next" :disabled="disable_next" v-on:click="submit_prediction">{{next_button_text}}</b-button>
        </b-overlay>
      </div>
    </div>
  </b-jumbotron>
</template>
<script>
import axios from 'axios'
import { colors } from '@/components/constants'
import TaskInfo from '@/components/TaskInfo.vue'
import ChatRoom from '@/components/ChatRoom.vue'
export default {
  data: function () {
    return {
      my_message: null,
      initial_answer: null,
      final_answer: null,
      start_time: null,
      timeout: null,
      logout_timeout: null,
      vote_timer: null,
      disable_next: true,
      disable_ready: true,
      busy: false,
      vote_button_text: 'Ready to vote',
      next_button_text: 'Vote',
      remain_time: 1,
      counter: 60, // Wait 60 seconds then can start voting.
      is_predicted: false,
      is_submitted: false,
      click_ready: false,
      time_lock: false
    }
  },
  components: {
    TaskInfo,
    ChatRoom
  },
  props: ['taskid'],
  methods: {
    typing () {
      if (!this.is_submitted) {
        this.reset_all_timeout() // Send out message after submit the final prediction
      }
    },
    avatarColorHex (avatar_color) {
      return colors[avatar_color]
    },
    reset_logout_timeout: function () {
      clearTimeout(this.logout_timeout)
      this.logout_timeout = setTimeout(() => {
        this.$router.push('/KickOut')
      }, 1000 * 60 * 2)
    },
    reset_timeout: function () {
      clearTimeout(this.timeout)
      this.timeout = setTimeout(() => {
        this.$toast(this.prompt_text, {
          position: 'top-right',
          timeout: 10000,
          closeOnClick: true,
          pauseOnFocusLoss: false,
          pauseOnHover: false,
          draggable: true,
          draggablePercent: 0.6,
          showCloseButtonOnHover: false,
          hideProgressBar: true,
          closeButton: 'button',
          icon: true,
          rtl: false
        })
        this.remain_time--
        this.reset_timeout()
      }, 1000 * 60)
    },
    record_initial: function () {
      if (this.initial_answer !== null) {
        this.is_predicted = true
        clearTimeout(this.logout_timeout)
        clearTimeout(this.timeout)
        this.time_lock = true
        let send_initial_complete_message = {
          'code': 350,
          'data': {
            'subject_id': this.$store.state.subject_id,
            'group_id': this.$store.state.group_id,
            'instance_id': this.$store.state.formal_task[this.$store.state.formal_task_no].instance_id,
            'task_no': this.$store.state.formal_task_no,
            'initial_answer': this.initial_answer
          }
        }
        this.$root.sendWebSocketMessage(send_initial_complete_message)
      } else {
        this.$alert('Please make your initial prediction!', '', 'warning')
      }
    },
    submit_ready: function () {
      this.time_lock = true
      clearTimeout(this.logout_timeout)
      clearTimeout(this.timeout)
      let send_confirm_message = {
        'code': 380,
        'data': {
          'subject_id': this.$store.state.subject_id,
          'group_id': this.$store.state.group_id,
          'instance_id': this.$store.state.formal_task[this.$store.state.formal_task_no].instance_id,
          'task_no': this.$store.state.formal_task_no
        }
      }
      this.$root.sendWebSocketMessage(send_confirm_message)
      this.disable_ready = true
      this.click_ready = true
      this.vote_button_text = 'Waiting for others to vote'
    },
    // submit_confirm: function () {
    //   this.disable_next = true
    //   this.next_button_text = 'Waiting for others’ votes'
    //   this.busy = true
    //   this.is_submitted = true
    //   clearTimeout(this.timeout)
    //   clearTimeout(this.logout_timeout)
    //   let send_confirm_message = {
    //     'code': 390,
    //     'data': {
    //       'subject_id': this.$store.state.subject_id,
    //       'group_id': this.$store.state.group_id,
    //       'instance_id': this.$store.state.formal_task[this.$store.state.formal_task_no].instance_id,
    //       'task_no': this.$store.state.formal_task_no
    //     }
    //   }
    //   this.$root.sendWebSocketMessage(send_confirm_message)
    // },
    submit_prediction: function () {
      this.disable_next = true
      this.next_button_text = 'Waiting for others to vote'
      this.busy = true
      this.is_submitted = true
      this.time_lock = true
      clearTimeout(this.timeout)
      clearTimeout(this.logout_timeout)
      let end_time = new Date()
      let send_final_prediction_message = {
        'code': 400,
        'data': {
          'subject_id': this.$store.state.subject_id,
          'group_id': this.$store.state.group_id,
          'instance_id': this.$store.state.formal_task[this.$store.state.formal_task_no].instance_id,
          'task_no': this.$store.state.formal_task_no,
          'initial_answer': this.initial_answer,
          'final_answer': this.final_answer,
          'spend_time': (end_time - this.start_time) / 1000
        }
      }
      this.$root.sendWebSocketMessage(send_final_prediction_message)
    },
    generate_confidence_question: function () {
      let likert_options = {
        1: 'Not confident at all',
        2: 'Mostly not confident',
        3: 'Somewhat confident',
        4: 'Moderately confident',
        5: 'Extremely confident'
      }
      this.logout_timeout = setTimeout(() => {
        this.$Swal_close()
        // this.$router.push('/KickOut')
      }, 1000 * 60 * 2)
      this.$toast('Please answer the question in 2 minutes.', {
        position: 'top-right',
        timeout: 10000,
        closeOnClick: true,
        pauseOnFocusLoss: false,
        pauseOnHover: false,
        draggable: true,
        draggablePercent: 0.6,
        showCloseButtonOnHover: false,
        hideProgressBar: true,
        closeButton: 'button',
        icon: true,
        rtl: false
      })
      this.$fire({
        title: 'Before moving on',
        html: '<p>Please answer the following question. We will redirect you to the next page once all group members answer this question</p><hr><p>How confident are you in your group\'s prediction for this defendant?</p>',
        input: 'radio',
        inputOptions: likert_options,
        icon: 'question',
        allowOutsideClick: false,
        preConfirm: (likert) => {
          if (typeof likert === 'undefined' || likert === null) {
            this.$showValidationMessage('Please make a selection')
          } else {
            clearTimeout(this.logout_timeout)
            clearTimeout(this.timeout)
            let send_option_change_message = {
              'code': 500,
              'data': {
                'subject_id': this.$store.state.subject_id,
                'instance_id': this.$store.state.formal_task[this.$store.state.formal_task_no].instance_id,
                'task_no': this.$store.state.formal_task_no,
                'confidence': likert
              }
            }
            this.$root.sendWebSocketMessage(send_option_change_message)
            return true
          }
        }
      })
    },
    reset_all_timeout: function () {
      this.remain_time = 1
      this.reset_timeout()
      this.reset_logout_timeout()
    },
    clear_setting: function () {
      for (let i = 0; i < this.$root.members.length; i++) {
        this.$root.members[i].is_initial = 0
        this.$root.members[i].is_final = 0
        this.$root.members[i].is_ready_vote = 0
        this.$root.members[i].is_confirm = 0
        this.$root.members[i].is_answer_confidence = 0
        this.$root.members[i].is_finish = 0
      }
      this.reset_all_timeout()
      if (this.$store.state.formal_task_no !== 0) {
        this.$store.commit('clear_messages')
      }
    },
    countdown: function () {
      this.counter--
      if (this.counter === 0) {
        clearInterval(this.vote_timer)
      }
    }
  },
  computed: {
    displayed_id: function () {
      return parseInt(this.taskid) + 1
    },
    get_id: function () {
      return parseInt(this.taskid)
    },
    members: function () {
      return this.$root.members
    },
    members_length: function () {
      return this.members.length
    },
    ml_suggestion: function () {
      if (this.$store.state.formal_task[this.get_id].model_suggestion === 'True') {
        return ''
      } else {
        return 'not'
      }
    },
    all_initial: function () {
      if (this.members_length === 0) {
        return true
      }

      for (let i = 0; i < this.members_length; i++) {
        if (this.members[i].is_activated === 1 && this.members[i].is_initial === 0) {
          return false
        }
      }
      return true
    },
    all_final: function () {
      if (this.members_length === 0) {
        return true
      }

      for (let i = 0; i < this.members_length; i++) {
        if (this.members[i].is_activated === 1 && this.members[i].is_final === 0) {
          return false
        }
      }
      return true
    },
    all_ready: function () {
      if (this.members_length === 0) {
        return true
      }

      for (let i = 0; i < this.members_length; i++) {
        if (this.members[i].is_activated === 1 && this.members[i].is_ready_vote === 0) {
          return false
        }
      }
      return true
    },
    all_confirm: function () {
      if (this.members_length === 0) {
        return true
      }

      for (let i = 0; i < this.members_length; i++) {
        if (this.members[i].is_activated === 1 && this.members[i].is_confirm === 0) {
          return false
        }
      }
      return true
    },
    all_confidence: function () {
      if (this.members_length === 0) {
        return true
      }

      for (let i = 0; i < this.members_length; i++) {
        if (this.members[i].is_activated === 1 && this.members[i].is_answer_confidence === 0) {
          return false
        }
      }
      return true
    },
    all_finish: function () {
      if (this.members_length === 0) {
        return true
      }

      for (let i = 0; i < this.members_length; i++) {
        if (this.members[i].is_activated === 1 && this.members[i].is_finish === 0) {
          return false
        }
      }
      return true
    },
    prompt_text: function () {
      if (this.is_ready_vote) {
        return 'Please tell others what you think about this defendant. If you are idle on the interface or not select any prediction on the interface for more than ' + this.remain_time + ' minutes, you will be logged out of the group automatically and won\'t be able to complete this HIT.'
      } else {
        return 'Please tell others what you think about this defendant. If you are idle on the interface for more ' + this.remain_time + ' minutes, you will be logged out of the group automatically and won\'t be able to complete this HIT.'
      }
    },
    group_initial: function () {
      let positive = 0
      let negative = 0
      let result = 'Some error happened!'

      for (let i = 0; i < this.$root.members.length; i++) {
        if (this.$root.members[i].is_activated === 1) {
          if (this.$root.members[i].initial === 'True') {
            positive = positive + 1
          } else {
            negative = negative + 1
          }
        }
      }

      if (positive > negative) {
        result = ''
      } else if (negative > positive) {
        result = 'not'
      } else {
        result = 'Tie'
      }
      return result
    },
    against_answer: function () {
      if (this.$store.state.condition === 1 || this.$store.state.condition === 2) {
        if (this.ml_suggestion === 'not') {
          return ''
        } else {
          return 'not'
        }
      } else if (this.$store.state.condition === 3 || this.$store.state.condition === 4) {
        if (this.group_initial === 'not') {
          return ''
        } else {
          return 'not'
        }
      }
      return ''
    }
  },
  destroyed () {
    clearTimeout(this.timeout)
    clearTimeout(this.logout_timeout)
    clearTimeout(this.vote_timer)
  },
  mounted () {
    if (this.get_id === 0) {
      let body = new FormData()
      body.append('subject_id', this.$store.state.subject_id)
      axios.post(this.$root.server_url + 'formal_start', body)
    }
    if (this.$store.state.formal_task_no === this.$store.state.formal_task.length) {
      this.$root.websock.close(4000)
      this.$router.push('/PostSurvey')
      setTimeout(() => {
        this.$root.is_loading = false
      }, 750)
    }
    this.start_time = new Date()
    this.initial_answer = null
    this.final_answer = null
    // this.$root.devil_lock = false
    this.disable_next = true
    this.disable_ready = true
    this.remain_time = 1
    this.$toast('Please make your initial prediction in 2 minutes', {
      position: 'top-right',
      timeout: 10000,
      closeOnClick: true,
      pauseOnFocusLoss: false,
      pauseOnHover: false,
      draggable: true,
      draggablePercent: 0.6,
      showCloseButtonOnHover: false,
      hideProgressBar: true,
      closeButton: 'button',
      icon: true,
      rtl: false
    })
    this.reset_logout_timeout()
    this.$watch(
      '$refs.chat.send_out_message',
      (new_value, old_value) => {
        if (!this.time_lock) {
          this.reset_all_timeout() // Send out message after submit the final prediction
        }
      }
    )
  },
  watch: {
    final_answer: function (val) {
      this.reset_all_timeout()
      if (this.final_answer != null) {
        this.disable_next = false
        let send_option_change_message = {
          'code': 300,
          'data': {
            'subject_id': this.$store.state.subject_id,
            'group_id': this.$store.state.group_id,
            'instance_id': this.$store.state.formal_task[this.$store.state.formal_task_no].instance_id,
            'task_no': this.$store.state.formal_task_no,
            'final_answer': this.final_answer
          }
        }
        this.$root.sendWebSocketMessage(send_option_change_message)
        this.$refs.confirm.scrollIntoView({behavior: 'smooth'})
      }
    },
    counter: function (val) {
      if (val > 0) {
        this.vote_button_text = 'Minimum discussion time left: ' + val + ' seconds'
      } else {
        clearTimeout(this.vote_timer)
        this.vote_button_text = 'Ready to vote'
        this.disable_ready = false
      }
    },
    all_initial: function (val) {
      if (val === false) {
        return
      }
      // Send their initial result.
      let preset_msg = '(Auto Generated) I voted for the defendant will ###### in my initial prediction.'
      if (this.initial_answer === 'True') {
        preset_msg = preset_msg.replace('######', 'reoffend')
      } else {
        preset_msg = preset_msg.replace('######', 'not reoffend')
      }

      let send_chat_message = {
        'code': 200,
        'data': {
          'subject_id': this.$store.state.subject_id,
          'group_id': this.$store.state.group_id,
          'instance_id': this.$store.state.formal_task[this.$store.state.formal_task_no].instance_id,
          'task_no': this.$store.state.formal_task_no,
          'msg': preset_msg
        }
      }
      this.$root.sendWebSocketMessage(send_chat_message)
      // request whether there is any devil's advocate
      // let send_request_devil_advocate_message = {
      //   'code': 666,
      //   'data': {
      //     'task_no': this.$store.state.formal_task_no
      //   }
      // }
      // this.$root.sendWebSocketMessage(send_request_devil_advocate_message)
      this.vote_timer = setInterval(this.countdown, 1000)
      this.time_lock = false
      this.reset_all_timeout()
    },
    // '$root.devil_lock': function () {
    //   if (this.$root.devil_lock) {
    //     if (this.$store.state.subject_id === this.$root.devil) {
    //       let target = ''
    //       if (this.$store.state.condition === 1 || this.$store.state.condition === 2) {
    //         target = 'machine learning model\'s'
    //       } else if (this.$store.state.condition === 3 || this.$store.state.condition === 4) {
    //         target = 'group\'s initial majority'
    //       } else {
    //         target = ''
    //       }
    //       this.$fire({
    //         title: 'You are the devil\'s advocate in this task! ',
    //         text: 'Please argue against the ' + target + ' prediction in this task!',
    //         icon: 'warning',
    //         allowOutsideClick: false
    //       })
    //     }
    //     let preset_msg = '(Auto Generated) I voted for the defendant will ###### in my initial prediction.'

    //     if (this.initial_answer === 'True') {
    //       preset_msg = preset_msg.replace('######', 'reoffend')
    //     } else {
    //       preset_msg = preset_msg.replace('######', 'not reoffend')
    //     }

    //     let send_chat_message = {
    //       'code': 200,
    //       'data': {
    //         'subject_id': this.$store.state.subject_id,
    //         'group_id': this.$store.state.group_id,
    //         'instance_id': this.$store.state.formal_task[this.$store.state.formal_task_no].instance_id,
    //         'task_no': this.$store.state.formal_task_no,
    //         'msg': preset_msg
    //       }
    //     }
    //     this.$root.sendWebSocketMessage(send_chat_message)
    //   }
    // },
    all_ready: function (val) {
      if (val === false) {
        return
      }
      this.time_lock = false
      this.reset_all_timeout()
    },
    all_final: function (val) {
      if (val === false) {
        return
      }
      let positive = 0
      let negative = 0
      let result = 'Some error happened!'

      for (let i = 0; i < this.$root.members.length; i++) {
        if (this.$root.members[i].is_activated === 1) {
          if (this.$root.members[i].final === 'True') {
            positive = positive + 1
          } else {
            negative = negative + 1
          }
        }
      }

      if (positive > negative) {
        result = 'Reoffend'
      } else if (negative > positive) {
        result = 'Not Reoffend'
      } else {
        result = 'Tie'
      }

      this.time_lock = false
      this.reset_all_timeout()

      this.$fire({
        title: 'Your group\'s final decision:',
        text: result,
        icon: 'info',
        allowOutsideClick: false
      }).then((result) => {
        this.time_lock = true
        clearTimeout(this.timeout)
        clearTimeout(this.logout_timeout)
        clearTimeout(this.vote_timer)
        let send_finish_message = {
          'code': 888,
          'data': {
            'subject_id': this.$store.state.subject_id
          }
        }
        this.$root.sendWebSocketMessage(send_finish_message)
      })
    },
    all_finish: function (val) {
      if (val === false) {
        return
      }
      this.$store.commit('formal_increment')
      this.clear_setting()
      this.$router.push('/FormalTask/' + this.$store.state.formal_task_no)
      setTimeout(() => {
        this.$root.is_loading = false
      }, 750)
    }
  }
}
</script>
<style>
</style>
