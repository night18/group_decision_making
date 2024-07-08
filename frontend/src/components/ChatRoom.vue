<template>
  <div class="chat-room">
    <div class="member-area">
      <span v-for="member in members" :key="member.id" class="member-card">
        <v-animal size="20px" :name="member.avatar_name" :color="avatarColorHex(member.avatar_color)" class="avatar-icon"/>
        {{member_name(member)}}
        <font-awesome-icon :icon="icon_style(member)" :class="{'green_icon': current_state(member)=== 3, 'yellow_icon': current_state(member) === 2, 'gray_icon': current_state(member) === 1 }"/>
      </span>
      <b-card no-body class="mb-1 icon-rule">
        <b-collapse id="accordion-icon" accordion="icon-accordion" role="tabpanel" v-on:hide="icon_hidden" v-on:show="icon_shown">
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
          <b-button block v-b-toggle.accordion-icon variant="info">{{icon_rule_text}}</b-button>
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
              <font-awesome-icon icon="fa-solid fa-gavel" class="circle-icon-judge"/>
            </div>
          </b-col>
          <b-col cols="9">
            <b-row>
              <b-col class="message-avatar-name">RiskComp</b-col>
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
      <div v-for="message in messages" :key="message.id" class="message-card">
        <b-row v-if="message.sender.subject_id === -1"> <!-- -1 is the id of gpt -->
          <b-col cols="1" class="vertical-align">
            <div class="message-avatar-icon">
              <font-awesome-icon icon="fa-solid fa-skull" class="circle-icon"/>
            </div>
          </b-col>
          <b-col cols="9">
            <b-row>
              <b-col class="message-avatar-name">Devil's Advocate</b-col>
            </b-row>
            <b-row>
              <b-col>
                <div class="message-content">
                  <span>{{message.content}}</span>
                </div>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
        <b-row v-else-if="message.sender.subject_id !== $store.state.subject_id">
          <b-col cols="1" class="vertical-align">
            <div class="message-avatar-icon">
              <v-animal size="30px" :name="message.sender.avatar_name" :color="avatarColorHex(message.sender.avatar_color)" class="avatar-icon"/>
            </div>
          </b-col>
          <b-col cols="9">
            <b-row>
              <b-col class="message-avatar-name">{{member_name(message.sender)}}</b-col>
            </b-row>
            <b-row>
              <b-col>
                <div class="message-content">
                  <span>{{message.content}}</span>
                </div>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
        <b-row v-else-if="message.sender.subject_id === $store.state.subject_id" class="own_message">
          <b-col cols="2"/>
          <b-col cols="9" style="padding-right: 0;">
            <b-row style="margin-left: 0;">
              <b-col class="message-avatar-name">{{member_name(message.sender)}}</b-col>
            </b-row>
            <b-row style="margin-left: 0;">
              <b-col>
                <div class="message-content">
                  <span>{{message.content}}</span>
                </div>
              </b-col>
            </b-row>
          </b-col>
          <b-col cols="1" class="vertical-align" style="text-align: left; padding-right: 0; padding-left: 10px;">
            <div class="message-avatar-icon">
              <v-animal size="30px" :name="message.sender.avatar_name" :color="avatarColorHex(message.sender.avatar_color)" class="avatar-icon"/>
          </div>
          </b-col>
        </b-row>
      </div>
    </div>
    <div class="message-area">
      <b-card no-body class="mb-1">
        <b-card-header header-tag="footer" class="p-1" role="tab">
          <b-button block v-b-toggle.accordion-rule variant="info">{{rule_text}}</b-button>
        </b-card-header>
        <b-collapse id="accordion-rule" accordion="accordion-rule" role="tabpanel" v-on:hide="collapse_hidden" v-on:show="collapse_shown">
          <b-card-body>
            <b-card-text>
              Share your thoughts about this defendant with other members in your group! When you are ready to make your final prediction, click the “Ready to vote” button on the left panel. You will be able to cast your final vote after all members in the group indicate that they are ready to vote. <br>
              Your group's final prediction on this defendant is decided by the majority vote of all members in the group.<br>
              Reminder: You can earn bonus if your group's <span class="highlight">final prediction is not a tie and is correct</span>. So, try to convince your group members to reach a consensus!
            </b-card-text>
            <!-- <b-card-text v-if="$store.state.condition != 0">
              <code>Devil's Advocate</code>: The devil's advocate is asked to argue against the <b v-if="$store.state.condition <= 2">Machine Learning's</b><b v-else>group's initial</b> prediction ({{against_answer}}).
            </b-card-text> -->
          </b-card-body>
        </b-collapse>
      </b-card>
      <b-input-group>
        <b-form-input placeholder="Aa" v-model="send_out_message" class="message-input-area" @keydown.enter.native="sendMessage"></b-form-input>
        <b-button variant='primary' class="message-send-button" v-on:click="sendMessage">Send</b-button>
      </b-input-group>
    </div>
  </div>
</template>
<script>
import { colors } from '@/components/constants'
export default {
  data: function () {
    return {
      send_out_message: '',
      // devil_tip: 'Devil\'s Advocate',
      rule_text: 'Hide Rules',
      icon_rule_text: 'Show Icon Explanation',
      gpt_allowed: true
    }
  },
  props: {
    'get_id': {
      type: Number,
      required: true
    },
    'my_message': {
      type: String,
      default: ''
    }
  },
  methods: {
    avatarColorHex (avatar_color) {
      return colors[avatar_color]
    },
    sendMessage (event) {
      if (this.send_out_message !== null && this.send_out_message !== '') {
        let send_chat_message = {
          'code': 200,
          'data': {
            'subject_id': this.$store.state.subject_id,
            'group_id': this.$store.state.group_id,
            'instance_id': this.$store.state.formal_task[this.$store.state.formal_task_no].instance_id,
            'task_no': this.$store.state.formal_task_no,
            'msg': this.send_out_message
          }
        }
        this.$root.sendWebSocketMessage(send_chat_message)
        this.send_out_message = ''
      }
    },
    initial_answer: function (initial) {
      if (initial === 'True') {
        return true
      } else {
        return false
      }
    },
    has_confirmed: function (is_confirm) {
      return is_confirm === 1
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
    member_name: function (member) {
      if (member.subject_id === this.$store.state.subject_id) {
        return 'You'
      } else {
        return member.avatar_color + ' ' + member.avatar_name
      }
    },
    // is_devil: function (member) {
    //   return member.subject_id === this.$root.devil
    // },
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
    },
    icon_style: function (member) {
      if (this.initial_answer(member.initial)) {
        return 'fa-solid fa-circle-check'
      } else {
        return 'fa-solid fa-circle-xmark'
      }
    }
  },
  watch: {
    messages: function () {
      this.$nextTick(() => {
        let el = this.$refs.roomarea.lastElementChild
        if (typeof el !== 'undefined') {
          el.scrollIntoView({behavior: 'smooth'})
        }
      })
      // el.scrollTop = el.lastElementChild.offsetTop + el.lastElementChild.offsetHeight
    },
    send_out_message: function () {
      this.$emit('typing')
    }
  },
  mounted () {
  },
  computed: {
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
        result = 'will reoffend'
      } else if (negative > positive) {
        result = 'will not reoffend'
      } else {
        result = 'Tie'
      }
      return result
    },
    against_answer: function () {
      if (this.$store.state.condition === 1 || this.$store.state.condition === 2) {
        return this.ml_suggestion
      } else if (this.$store.state.condition === 3 || this.$store.state.condition === 4) {
        return this.group_initial
      }
      return ''
    },
    messages: function () {
      return this.$store.state.messages
    },
    members: function () {
      return this.$root.members.filter(i => i.is_activated === 1)
    },
    ml_suggestion: function () {
      if (this.$store.state.formal_task[this.get_id].model_suggestion === 'True') {
        return 'will reoffend'
      } else {
        return 'will not reoffend'
      }
    }
    // ,diff_answer: function (member) {
    //   if (this.$root.members.length === 0) {
    //     return 'gray_icon'
    //   }

    //   if (this.estimation === null) {
    //     return 'gray_icon'
    //   }

    //   let selection = null
    //   let count = 0

    //   for (let i = 0; i < this.$root.members.length; i++) {
    //     if (this.$root.members[i].is_activated) {
    //       if (typeof this.$root.members[i].estimation === 'undefined' || this.$root.members[i].estimation === null) {
    //         return 'gray_icon'
    //       }

    //       if (selection !== this.$root.members[i].estimation) {
    //         if (this.$root.members[i].estimation === 'True' || this.$root.members[i].estimation === 'False') {
    //           selection = this.$root.members[i].estimation
    //           count = count + 1
    //         }
    //       }
    //     }
    //   }
    //   if (count !== 1) {
    //     return 'gray_icon'
    //   } else {
    //     return 'green_icon'
    //   }
    // }
  }
}
</script>
<style>
  .chat-room {
    height: calc(100vh - 70px);
    min-height: 391px;
    width: 100%;
    border: solid 1px #1d3557;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
  }

  @media (max-height: 600px) {
    .chat-room {
      height: calc(100vh - 150px);
    }
  }

  .member-area {
    padding: 10px 15px;
    border-bottom: solid 1px #E5E5E5;
    line-height: 20px;
  }

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

  .room-area {
    padding: 10px 0 10px 10px;
    /* min-height: 300px; */
    max-height: 800px;
    background-color: white;
    height: 100vh;
    border-radius: 10px;
    overflow-x: none;
    flex: 1;
    overflow-y: auto;
  }

  .message-card {
    padding-bottom: 10px;
  }

  .message-card .row{
    width: 100%;
  }

  .message-avatar-icon {
    display: inline-block;
    text-align: center;
    line-height: 30px;
    margin: auto 0;
  }

  .circle-icon-judge {
    background: #432818;
    color:  #FFFFFF;
    width: 20px;
    height: 16px;
    border-radius: 50%;
    text-align: center;
    line-height: 30px;
    vertical-align: middle;
    padding: 7px 5px;
  }

  .circle-icon {
    background: #980002;
    color:  #FFFFFF;
    width: 20px;
    height: 16px;
    border-radius: 50%;
    text-align: center;
    line-height: 30px;
    vertical-align: middle;
    padding: 7px 5px;
  }

  .message-avatar-name {
    font-size: 0.8em;
  }

  .message-content {
    background-color: #E4E6EB;
    padding: 3px 15px;
    border-radius: 10px;
    display: inline-block;
  }

  .own_message {
    text-align: right;
    margin-left: -10px;
  }

  .own_message .message-content {
    background-color: #0184ff;
    color:  #ffffff;
    margin-right: 0;
    margin-left: auto;
  }

  .own_message .col {
    padding-right: 0;
  }

  .message-area {
    border-radius: 10px;
  }

  .message-input-area {
    background-color: #F0F2F5;
    border-radius: 10px;
  }

  .message-send-button {
    border-bottom-right-radius: 10px;
  }

  .chat-info {
    display: block;
    text-align: left;
    color: #666666;
    border-style: solid;
    border-color: #999999;
    margin-left: -10px;
    margin: 0 20px;
    padding-left: 5px;
    padding-bottom: 10px;
  }

  .gray_icon {
    color: #8d99ae;
  }

  .green_icon {
    color: #57cc99;
  }

  .yellow_icon {
    color: #f5cd79;
  }

  .red_icon {
    color: #f42c57;
  }

  .devil_background {
    background-color: #8b0000;
    color: white;
  }

  #accordion-icon, #accordion-rule {
    padding-left: 5px;
    padding-right: 5px;
    background-color: #e5f9f9;
  }
</style>
