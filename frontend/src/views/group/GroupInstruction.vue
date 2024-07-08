<template>
  <b-jumbotron header-level='1'>
    <template v-slot:lead>
      <span id="task_number" ref="task_number">
        Group test (1/8)
      </span>
    </template>
    <div>
      <b-row>
        <b-col fluid>
          <div class="content-area task-area">
            <div>
              <p>Please review the profile below and predict whether the defendant would reoffend in the next two years.</p>
              <div ref="task_info">
                <TaskInfo :defendant="defendant"/>
              </div>
              <div class="answer-area">
                <p>
                  <b>Make Your Initial Prediction</b>
                </p>
                <p>Do you think this defendant will reoffend within 2 years?</p>
                <b-form-group v-slot="{ ariaDescribedby }" :disabled="is_predicted">
                 <b-form-radio v-model="initial_answer" :aria-describedby="ariaDescribedby" value="True">The defendant <b>will</b> reoffend within two years</b-form-radio>
                 <b-form-radio v-model="initial_answer" :aria-describedby="ariaDescribedby" value="False">The defendant <b>will not</b> reoffend within two years</b-form-radio>
               </b-form-group>
               <b-button id="initial_button" ref="initial_button" v-show="!is_predicted" variant="primary" name="next">Start Group Discussion</b-button>
              </div>
            </div>
            <div v-show="is_predicted">
              <div>
                <div id="ml_suggestion" ref="ml_suggestion" class="suggestion-area">
                    <p>
                      <b>Machine learning Prediction:</b>
                    </p>
                    Our machine learning model predicts that this defendant will <span class="highlight">{{ml_suggestion}}</span> reoffend in 2 years.
                  </div>
                <div ref="answer_area" class="answer-area">
                  <div v-show="all_ready">
                    <p>
                      <b>Vote for Your Final Prediction</b>
                    </p>
                    <p>Do you think this defendant will reoffend within 2 years?</p>
                    <b-form-group v-slot="{ ariaDescribedby }" :disabled="is_submitted">
                     <b-form-radio v-model="final_answer" :aria-describedby="ariaDescribedby" value="True">The defendant <b>will</b> reoffend within two years</b-form-radio>
                     <b-form-radio v-model="final_answer" :aria-describedby="ariaDescribedby" value="False">The defendant <b>will not</b> reoffend within two years</b-form-radio>
                   </b-form-group>
                  </div>
                  <div v-show="!all_ready">
                    <p class="highlight" v-if="!click_ready && disable_ready">
                      Please spend at least one minute to discuss this defendant's case with other members in your group.
                    </p>
                    <p v-if="!disable_ready && !click_ready">
                      If you are ready to make your final prediction, click the button below. You will only be able to cast your final vote when all members of your group indicate that they are ready to vote.
                    </p>
                    <p v-if="click_ready">
                      You will be able to cast your final vote once all members of your group indicate that they are ready to vote.
                    </p>
                    <b-button id="ready" ref="ready" variant="primary" name="ready" :disabled="disable_ready">{{vote_button_text}}</b-button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </b-col>
        <b-col cols='6' v-if="is_predicted">
          <div class="chat-room">
            <div class="member-area">
              <div id="member_area" ref="member_area">
                <span v-for="member in members" :key="member.id" class="member-card">
                  <v-animal size="20px" :name="member.avatar_name" :color="avatarColorHex(member.avatar_color)" class="avatar-icon"/>
                  {{member_name(member)}}
                  <font-awesome-icon :icon="icon_style(member)" :class="{'green_icon': current_state(member)=== 3, 'yellow_icon': current_state(member) === 2, 'gray_icon': current_state(member) === 1 }"/>
                </span>
              </div>
              <b-card id="icon_rule" ref="icon_rule" no-body class="mb-1 icon-rule">
                <b-collapse id="accordion-icon" ref="accordion_icon" accordion="icon-accordion" role="tabpanel" v-on:hide="icon_hidden" v-on:show="icon_shown">
                  <p><b>Mark Style</b>: Initial Vote <br>
                    <font-awesome-icon icon="fa-solid fa-circle-check" class="gray_icon"/> Initial prediction: Reoffend<br>
                    <font-awesome-icon icon="fa-solid fa-circle-xmark" class="gray_icon"/> Initial prediction: Not Reoffend<br>
                  </p>
                  <p><b>Mark Color</b>: Voting Status <br>
                    <font-awesome-icon icon="fa-solid fa-circle" class="gray_icon"/> Made initial vote!<br>
                    <font-awesome-icon icon="fa-solid fa-circle" class="yellow_icon"/> Ready to vote!<br>
                    <font-awesome-icon icon="fa-solid fa-circle" class="green_icon"/> Made final vote!<br>
                  </p>
                </b-collapse>
                <b-card-footer footer-tag="footer" class="p-1" role="tab">
                  <b-button id="icon_button" ref="icon_button" block v-b-toggle.accordion-icon variant="info">{{icon_rule_text}}</b-button>
                </b-card-footer>
              </b-card>
            </div>
            <div class="room-area" ref="roomarea">
              <div class="chat-info">
                Share your thoughts with other members of your group to make an accurate prediction!
              </div>
              <div class="message-card">
                <b-row>
                  <b-col cols="1" class="vertical-align">
                    <div class="message-avatar-icon">
                      <font-awesome-icon icon="fa-solid fa-robot" class="circle-icon"/>
                    </div>
                  </b-col>
                  <b-col cols="9">
                    <b-row>
                      <b-col class="message-avatar-name">Risk Analysis Bot</b-col>
                    </b-row>
                    <b-row>
                      <b-col>
                        <div class="message-content">
                          <span>Our machine learning model predicts that this defendant <span class="highlight">{{ml_suggestion}}</span> in 2 years.</span>
                        </div>
                      </b-col>
                    </b-row>
                  </b-col>
                </b-row>
              </div>
            </div>
            <div class="message-area" id="message_area" ref="message_area">
              <b-card no-body class="mb-1">
                <b-card-header id="rule_button" ref="rule_button" header-tag="footer" class="p-1" role="tab">
                  <b-button block v-b-toggle.accordion-rule variant="info">{{rule_text}}</b-button>
                </b-card-header>
                <b-collapse id="accordion-rule" ref="accordion_rule" accordion="accordion-rule" role="tabpanel" v-on:hide="collapse_hidden" v-on:show="collapse_shown">
                  <b-card-body>
                    <b-card-text>
                      Share your thoughts about this defendant with other members in your group! When you are ready to make your final prediction, click the “Ready to vote” button on the left panel. You will be able to cast your final vote after all members in the group indicate that they are ready to vote. <br>
                      Your group's final prediction on this defendant is decided by the majority vote of all members in the group.<br>
                      Reminder: You can earn bonus if your group's <span class="highlight">final prediction is not a tie and is correct</span>. So, try to convince your group members to reach a consensus!
                    </b-card-text>
                  </b-card-body>
                </b-collapse>
              </b-card>
              <b-input-group  id="input_area" ref="input_area">
                <b-form-input placeholder="Aa" v-model="send_out_message" class="message-input-area" @keydown.enter.native="sendMessage"></b-form-input>
                <b-button variant='primary' class="message-send-button">Send</b-button>
              </b-input-group>
            </div>
          </div>
        </b-col>
      </b-row>
      <div class="button-area" v-show="all_ready">
        <b-overlay
          rounded
          opacity="0.6"
          spinner-small
          spinner-variant="primary"
          >
          <b-button id="confirm" ref="confirm" variant="primary" name="next" :disabled="disable_next">{{next_button_text}}</b-button>
        </b-overlay>
      </div>
    </div>
    <v-tour name="myTour" :steps="steps" :callbacks="{
      onStop: onStopTour
    }"></v-tour>
  </b-jumbotron>
</template>
<script>
import TaskInfo from '@/components/TaskInfo.vue'
import { colors } from '@/components/constants'
export default {
  data: function () {
    return {
      // Default values
      defendant: {
        race: 'Asian',
        sex: 'Male',
        age: '24',
        prior: '0',
        felony: '0',
        misdemeanor: '1',
        charge_reason: 'Theft',
        charge_degree: 'misdemeanor',
        charge_explain: 'The taking of another person\'s property worth less than $300.'
      },
      members: [
        {
          subject_id: 0,
          avatar_name: 'camel',
          avatar_color: 'purple',
          is_activated: 1,
          is_initial: 0,
          is_final: 0,
          is_ready_vote: 0,
          is_confirm: 0,
          is_answer_confidence: 0,
          is_finish: 0,
          initial: 'True'
        },
        {
          subject_id: 1,
          avatar_name: 'rabbit',
          avatar_color: 'teal',
          is_activated: 1,
          is_initial: 0,
          is_final: 0,
          is_ready_vote: 0,
          is_confirm: 0,
          is_answer_confidence: 0,
          is_finish: 0,
          initial: 'True'
        },
        {
          subject_id: 2,
          avatar_name: 'wolf',
          avatar_color: 'brown',
          is_activated: 1,
          is_initial: 0,
          is_final: 0,
          is_ready_vote: 0,
          is_confirm: 0,
          is_answer_confidence: 0,
          is_finish: 0,
          inintial: 'True'
        }
      ],
      highlights: [],
      // Step 1: making initial prediction.
      is_predicted: false,
      initial_answer: null,
      // Step 2: review ML prediction and click ready to vote.
      disable_ready: true,
      click_ready: false,
      all_ready: false,
      is_submitted: false,
      vote_button_text: 'Ready to vote',
      ml_suggestion: 'will',
      // Step 3: submit final prediction
      disable_next: true,
      next_button_text: 'Vote',
      rule_text: 'Hide Rules',
      icon_rule_text: 'Show Icon Explanation',
      send_out_message: null,
      final_answer: null,
      steps: [
        {
          target: '#task_number',
          header: {
            title: 'Get Started'
          },
          content: 'In the formal phase, you will complete 8 recidivism risk prediction tasks together with other members in your group. Let\'s go through the task interface to see what you need to do in each task!',
          before: type => {
            this.updateHighlights([this.$refs.task_number])
          }
        },
        {
          target: '#initial_button',
          content: 'In each task, you first need to review the defendant\'s profile and make your own recidivism risk prediction for this defendant. After you make your prediction, click on the "Start Group Discussion" button.',
          before: type => {
            this.is_predicted = false
            this.vote_button_text = 'Ready to vote'
            this.updateHighlights([this.$refs.initial_button, this.$refs.task_info])
          }
        },
        {
          target: '#ml_suggestion',
          content: 'When all members in your group finish making their own prediction, you will be redirected to this discussion interface. Remember to first check out the machine learning model\'s prediction for the defendant on this interface!',
          before: type => {
            this.initial_answer = 'True'
            this.is_predicted = true
            this.vote_button_text = 'Minimum discussion time left: 60 seconds'
            for (let i = 0; i < this.members.length; i++) {
              this.members[i].is_initial = 1
            }
            this.updateHighlights([this.$refs.ml_suggestion])
          }
        },
        {
          target: '#member_area',
          content: `Here, you can see other group members' initial prediction:
          <svg data-v-5ccaa159="" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="circle-check" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="gray_icon svg-inline--fa fa-circle-check"><path data-v-5ccaa159="" fill="currentColor" d="M0 256C0 114.6 114.6 0 256 0C397.4 0 512 114.6 512 256C512 397.4 397.4 512 256 512C114.6 512 0 397.4 0 256zM371.8 211.8C382.7 200.9 382.7 183.1 371.8 172.2C360.9 161.3 343.1 161.3 332.2 172.2L224 280.4L179.8 236.2C168.9 225.3 151.1 225.3 140.2 236.2C129.3 247.1 129.3 264.9 140.2 275.8L204.2 339.8C215.1 350.7 232.9 350.7 243.8 339.8L371.8 211.8z" class=""></path></svg> means they think the defendant will reoffend, and
          <svg data-v-5ccaa159="" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="circle-xmark" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="gray_icon svg-inline--fa fa-circle-xmark"><path  fill="currentColor" d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM175 175c9.4-9.4 24.6-9.4 33.9 0l47 47 47-47c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9l-47 47 47 47c9.4 9.4 9.4 24.6 0 33.9s-24.6 9.4-33.9 0l-47-47-47 47c-9.4 9.4-24.6 9.4-33.9 0s-9.4-24.6 0-33.9l47-47-47-47c-9.4-9.4-9.4-24.6 0-33.9z"/></svg> means they think the defendant will not reoffend.`,
          before: type => {
            this.$refs.accordion_icon.show = true
            this.updateHighlights([this.$refs.member_area])
          }
        },
        {
          target: '#icon_button',
          content: 'You can click on this button to hide or show the explanations of what the icons alongside each group member mean.',
          before: type => {
            this.updateHighlights([this.$refs.icon_button])
          }
        },
        {
          target: '#input_area',
          content: 'You are asked to share your thoughts with other group members regarding whether you think this defendant will reoffend in the next two years and why. In-depth discussion will help your group evaluate the case more thoroughly and make more informed predictions!',
          before: type => {
            this.$refs.accordion_icon.show = false
            this.updateHighlights([this.$refs.input_area])
          }
        },
        {
          target: '#ready',
          content: 'After your group is done with the discussion, you can click on this button to indicate you are ready to make the final prediction for this defendant. You are required to engage in group discussion for at least 1 minute before making your final prediction.',
          before: typ => {
            this.vote_button_text = 'Minimum discussion time left: 60 seconds'
            this.all_ready = false
            this.updateHighlights([this.$refs.ready])
          }
        },
        {
          target: '#member_area',
          content: 'A group member\'s icon will turn yellow once they have indicated that they are ready to make the final prediction.',
          before: typ => {
            this.vote_button_text = 'Ready to Vote'
            for (let i = 0; i < this.members.length - 1; i++) {
              this.members[i].is_ready_vote = 1
            }
            this.updateHighlights([this.$refs.member_area])
          }
        },
        {
          target: '#confirm',
          content: 'After all members are ready, you can proceed to make the final prediction.',
          before: type => {
            this.members[2].is_ready_vote = 1
            this.all_ready = true
            this.disable_next = true
            this.$refs.answer_area.lastElementChild.scrollIntoView({behavior: 'smooth'})
            this.updateHighlights([this.$refs.confirm, this.$refs.answer_area])
          }
        },
        {
          target: '#member_area',
          content: 'The member status will turn green after voting. Once all members have voted, we will display your group\'s final prediction based on the majority vote.',
          before: typ => {
            for (let i = 1; i < this.members.length; i++) {
              this.members[i].is_final = 1
            }
            this.updateHighlights([this.$refs.member_area])
          }
        },
        {
          target: '#rule_button',
          content: 'In case you are not sure what to do in a task, click on this button to hide or show the explanations of rules of the task (i.e., what you are asked to do in the task).',
          before: typ => {
            this.members[0].is_final = 1
            this.disable_next = false
            this.$refs.accordion_rule.show = true
            this.updateHighlights([this.$refs.rule_button])
          }
        }
      ]
    }
  },
  components: {
    TaskInfo
  },
  methods: {
    onStopTour () {
      this.$router.push('/NetiquetteRule')
    },
    updateHighlights (highlights) {
      for (let i = 0; i < this.highlights.length; i++) {
        this.unhighlightBlock(this.highlights[i])
      }
      this.highlights = highlights
      for (let i = 0; i < this.highlights.length; i++) {
        this.highlightBlock(this.highlights[i])
      }
    },
    highlightBlock (item) {
      item.classList.add('highlight_block')
    },
    unhighlightBlock (item) {
      item.classList.remove('highlight_block')
    },
    // Chat room function
    avatarColorHex (avatar_color) {
      return colors[avatar_color]
    },
    member_name: function (member) {
      if (member.subject_id === 0) {
        return 'You'
      } else {
        return member.avatar_color + ' ' + member.avatar_name
      }
    },
    icon_style: function (member) {
      if (member.initial === 'True') {
        return 'fa-solid fa-circle-check'
      } else {
        return 'fa-solid fa-circle-xmark'
      }
    },
    current_state: function (member) {
      if (member.is_final === 1) {
        return 3
      } else if (member.is_ready_vote === 1) {
        return 2
      } else if (member.is_initial === 1) {
        return 1
      } else {
        return 0
      }
    },
    collapse_hidden: function () {
      this.rule_text = 'Show Rules'
    },
    collapse_shown: function () {
      this.rule_text = 'Hide Rules'
    },
    icon_hidden: function () {
      this.icon_rule_text = 'Show Icon Explanation'
    },
    icon_shown: function () {
      this.icon_rule_text = 'Hide Icon Explanation'
    }
  },
  computed: {
  },
  destroyed () {
  },
  mounted () {
    this.$tours['myTour'].start()
  },
  watch: {
  }
}
</script>
<style scoped>
.highlight_block {
    border: solid 2px red;
  }
</style>
