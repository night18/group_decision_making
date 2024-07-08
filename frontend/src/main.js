import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import './plugins/axios'
import './plugins/bootstrap-vue'
import VueSimpleAlert from './plugins/vue-simple-alert'
import App from './App.vue'
import router from './router'
import animal from 'vue-animals'
import './assets/style.css'
import Vuex from 'vuex'
import Amplify from 'aws-amplify'
import '@aws-amplify/ui-vue'
import aws_exports from './aws-exports'
import { useSound } from '@vueuse/sound'
import sound from './assets/alert.mp3'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'
/* import specific icons */
import { faCircleCheck, faCircleXmark, faCircle, faSkull, faGavel } from '@fortawesome/free-solid-svg-icons'
/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import VueTour from 'vue-tour'
import axios from 'axios'

require('vue-tour/dist/vue-tour.css')
Amplify.configure(aws_exports)
Vue.config.productionTip = false
Vue.use(Vuex)
Vue.use(VueSimpleAlert)
Vue.use(Toast, {
  transition: 'Vue-Toastification__bounce',
  maxToasts: 20,
  newestOnTop: true
})
Vue.use(VueTour)
Vue.component('v-animal', animal)
library.add(faCircleCheck)
library.add(faCircleXmark)
library.add(faCircle)
library.add(faSkull)
library.add(faGavel)
Vue.component('font-awesome-icon', FontAwesomeIcon)

const store = new Vuex.Store({
  // plugins: [createPersistedState({
  //   getItem: key => Cookies.get(key),
  //   setItem: (key, value) => Cookies.set(key, value, { expires: 3, secure: false }),
  //   removeItem: key => Cookies.remove(key)
  // })],
  state () {
    return {
      subject_id: null,
      avatar_name: null,
      avatar_color: null,
      condition: -1,
      qualified_task_no: 0,
      practice_task_no: 0,
      formal_task_no: 0,
      group_id: -1,
      qualified_task: [],
      practice_task: [],
      formal_task: [],
      messages: []
    }
  },
  mutations: {
    assign_subject_id (state, record) {
      state.subject_id = record.subject_id
    },
    assign_condition (state, record) {
      state.condition = record.condition
    },
    assign_qualified (state, tasks) {
      state.qualified_task = tasks
    },
    qualified_increment (state) {
      state.qualified_task_no++
    },
    assign_practice (state, tasks) {
      state.practice_task = tasks
    },
    practice_increment (state) {
      state.practice_task_no++
    },
    practice_record (state, record) {
      state.practice_task[record.task_no].initial_answer = record.initial_answer
      state.practice_task[record.task_no].final_answer = record.final_answer
    },
    assign_group_id (state, record) {
      state.group_id = record.group_id
    },
    assign_formal (state, tasks) {
      state.formal_task = tasks
    },
    formal_increment (state) {
      state.formal_task_no++
    },
    formal_record (state, record) {
      state.formal_task[record.task_no].user_prediction = record.estimation
    },
    formal_truth (state, record) {
      for (let i = 0; i < record.length; i++) {
        for (let j = 0; j < state.formal_task.length; j++) {
          if (state.formal_task[j].instance_id === record[i].instance_id) {
            Vue.set(state.formal_task[j], 'ground_truth', record[i].ground_truth)
            // state.formal_task[j].ground_truth = record[i].ground_truth
          }
        }
      }
    },
    new_message (state, message) {
      state.messages.push(message)
    },
    clear_messages (state) {
      state.messages = []
    }
  },
  getters: {
  }
})

new Vue({
  data: function () {
    return {
      // localhost
      server_url: 'http://127.0.0.1:8000/ccw/api/',
      chat_url: 'ws://127.0.0.1:8000/ws/chat/',
      test_mode: true,
      // AWS
      // server_url: 'https://devil-advocate.hci-study.com/ccw/api/',
      // chat_url: 'wss://devil-advocate.hci-study.com/ws/chat/',
      // test_mode: false,
      estimation: null,
      is_loading: false,
      fire_400: false,
      members: [],
      decisions: []
    }
  },
  methods: {
    initWebSocket () {
      this.websock = new WebSocket(this.chat_url + this.$store.state.group_id + '/')
      this.websock.onmessage = this.webSocketOnMessage
      this.websock.onopen = this.webSocketOnOpen
      this.websock.onerror = this.webSocketOnError
      this.websock.onclose = this.webSocketOnClose
    },
    sendWebSocketMessage (msg) {
      this.websock.send(JSON.stringify(msg))
    },
    webSocketOnMessage (response) {
      let message = JSON.parse(response.data).message
      if (message.code === 101) {
        // Successful pairing
        // return format
        // { "code": 101,
        //   "user_list": user_list,
        //   "startable": startable,
        //   "task_list" : new_list }

        this.$root.members = message.user_list
        if (message.startable === 1) {
          this.$store.commit('assign_formal', message.task_list)
          this.alarm_sound.play()
          // show popup message based on the condition
          let popup_message = 'You will redirect to more instructions in 5 seconds'
          if (this.$store.state.condition === 0) { // No devil's advocate
            popup_message = 'You will redirect to formal task in 5 seconds'
          }

          this.$toast(popup_message, {
            position: 'top-right',
            timeout: 4500,
            closeOnClick: false,
            pauseOnFocusLoss: false,
            pauseOnHover: false,
            draggable: false,
            draggablePercent: 0.6,
            showCloseButtonOnHover: false,
            hideProgressBar: true,
            closeButton: false,
            icon: true,
            rtl: false
          })
          setTimeout(() => {
            if (this.$store.state.condition === 0) { // No devil's advocate
              this.$router.push('/FormalTask/' + this.$store.state.formal_task_no)
            } else {
              this.$router.push('/DAInstruction')
            }
          }, 5000)
        }
      } else if (message.code === 201) {
        let received_msg = message.message
        for (let i = 0; i < this.$root.members.length; i++) {
          if (received_msg.sender.subject_id === this.$root.members[i].subject_id) {
            received_msg.sender.avatar_name = this.$root.members[i].avatar_name
            received_msg.sender.avatar_color = this.$root.members[i].avatar_color
          }
        }
        this.$store.commit('new_message', received_msg)
        if (this.$store.state.condition === 2 || this.$store.state.condition === 4) {
          if (received_msg.sender.subject_id === this.$store.state.subject_id) {
            if (received_msg.content.indexOf('Auto Generated') === -1) {
              let body = new FormData()
              body.append('subject_id', this.$store.state.subject_id)
              body.append('group_id', this.$store.state.group_id)
              body.append('instance_id', this.$store.state.formal_task[this.$store.state.formal_task_no].instance_id)
              body.append('task_no', this.$store.state.formal_task_no)
              const messagesData = JSON.stringify(this.$store.state.messages)
              body.append('messages', messagesData)
              let initial_prediction = ''
              let positive = 0
              let negative = 0

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
                initial_prediction = 'true'
              } else if (negative > positive) {
                initial_prediction = 'false'
              } else {
                initial_prediction = 'tie'
              }
              body.append('initial_prediction', initial_prediction)
              body.append('send_out_message', this.send_out_message)
              body.append('condition', this.$store.state.condition)
              console.log(body)
              axios.post(this.$root.server_url + 'gpt_response', body).then((response) => {
                let gpt_response = response.data.content
                if (gpt_response !== '...') {
                  let sned_gpt_response = {
                    'code': 777,
                    'data': {
                      'subject_id': this.$store.state.subject_id,
                      'group_id': this.$store.state.group_id,
                      'instance_id': this.$store.state.formal_task[this.$store.state.formal_task_no].instance_id,
                      'task_no': this.$store.state.formal_task_no,
                      'msg': gpt_response
                    }
                  }
                  this.$root.sendWebSocketMessage(sned_gpt_response)
                }
              })
            }
          }
        } else if (received_msg.content.indexOf('Auto Generated') >= 0 && received_msg.sender.subject_id === this.$store.state.subject_id) {
          if (this.$store.state.condition === 1 || this.$store.state.condition === 3) { // Fixed devil's advocate
            // The activate user whose id is the smallest has to request the server for the devil's advocate
            for (let i = 0; i < this.$root.members.length; i++) {
              if (this.$root.members[i].is_activated === 1) {
                if (this.$store.state.subject_id === this.$root.members[i].subject_id) {
                  let body = new FormData()
                  body.append('subject_id', this.$store.state.subject_id)
                  body.append('group_id', this.$store.state.group_id)
                  body.append('instance_id', this.$store.state.formal_task[this.$store.state.formal_task_no].instance_id)
                  body.append('task_no', this.$store.state.formal_task_no)
                  let initial_prediction = ''
                  let positive = 0
                  let negative = 0

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
                    initial_prediction = 'true'
                  } else if (negative > positive) {
                    initial_prediction = 'false'
                  } else {
                    initial_prediction = 'tie'
                  }
                  body.append('initiaL_prediction', initial_prediction)
                  body.append('condition', this.$store.state.condition)
                  axios.post(this.$root.server_url + 'gpt_response', body).then((response) => {
                    let gpt_response = response.data.content
                    let response_array = gpt_response.split('- ')
                    for (let i = 1; i < response_array.length; i++) {
                      let sned_gpt_response = {
                        'code': 777,
                        'data': {
                          'subject_id': this.$store.state.subject_id,
                          'group_id': this.$store.state.group_id,
                          'instance_id': this.$store.state.formal_task[this.$store.state.formal_task_no].instance_id,
                          'task_no': this.$store.state.formal_task_no,
                          'msg': response_array[i]
                        }
                      }
                      this.$root.sendWebSocketMessage(sned_gpt_response)
                    }
                  })
                }
                break
              }
            }
          }
        }
      } else if (message.code === 301) {
        for (let i = 0; i < this.$root.members.length; i++) {
          this.$root.members[i].is_confirm = 0
        }
        let received_est = message.estimation
        for (let i = 0; i < this.$root.members.length; i++) {
          if (received_est.sender.subject_id === this.$root.members[i].subject_id) {
            this.$set(this.$root.members[i], 'estimation', received_est.estimation)
          }
        }
      } else if (message.code === 351) {
        let answer = message.answer

        for (let i = 0; i < this.$root.members.length; i++) {
          if (answer.sender.subject_id === this.$root.members[i].subject_id) {
            this.$root.members[i].is_initial = 1
            this.$set(this.$root.members[i], 'initial', answer.initial)
          }
        }
      } else if (message.code === 381) {
        let ready_subject = message.sender.subject_id
        for (let i = 0; i < this.$root.members.length; i++) {
          if (this.$root.members[i].subject_id === ready_subject) {
            this.$root.members[i].is_ready_vote = 1
          }
        }
      } else if (message.code === 392) {
        let confirm_subject = message.sender.subject_id
        for (let i = 0; i < this.$root.members.length; i++) {
          if (this.$root.members[i].subject_id === confirm_subject) {
            this.$root.members[i].is_confirm = 1
          }
        }
      } else if (message.code === 401) {
        let answer = message.answer
        // Pop out the final vote result
        for (let i = 0; i < this.$root.members.length; i++) {
          if (answer.sender.subject_id === this.$root.members[i].subject_id) {
            this.$root.members[i].is_final = 1
            this.$set(this.$root.members[i], 'final', answer.final)
          }
        }
        // this.$store.commit('formal_record', {task_no: this.$store.state.formal_task_no, estimation: message.final})
        // this.$root.is_loading = true
      } else if (message.code === 502) { // someone answers the confidence question
        let confirm_subject = message.sender.subject_id
        let avatar_color = null
        let avatar_name = null
        for (let i = 0; i < this.$root.members.length; i++) {
          if (this.$root.members[i].subject_id === confirm_subject) {
            this.$root.members[i].is_answer_confidence = 1
            avatar_color = this.$root.members[i].avatar_color
            avatar_name = this.$root.members[i].avatar_name
          }
        }

        this.$toast(avatar_color + ' ' + avatar_name + ' has just finished answering the confidence question', {
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
      } else if (message.code === 667) {
        // this.$root.devil = message.devil
        // this.$root.devil_lock = true
      } else if (message.code === 778) {
        let received_msg = message.message
        this.$store.commit('new_message', received_msg)
      } else if (message.code === 888) {
        let finish_subject = message.sender.subject_id
        for (let i = 0; i < this.$root.members.length; i++) {
          if (this.$root.members[i].subject_id === finish_subject) {
            this.$root.members[i].is_finish = 1
          }
        }
      } else if (message.code === 901) {
        // Someone leaving during formal experiment
        let leaving_subject = message.leaving_subject
        for (let i = 0; i < this.$root.members.length; i++) {
          if (this.$root.members[i].subject_id === leaving_subject) {
            this.$root.members[i].is_activated = 0
          }
        }
      } else if (message.code === 931) {
        // Someone leaving when pairing
        let leaving_subject = message.leaving_subject
        for (let i = 0; i < this.$root.members.length; i++) {
          if (this.$root.members[i].subject_id === leaving_subject) {
            this.$root.members.splice(i, 1)
          }
        }
      }
    },
    webSocketOnOpen (e) {
      let enter_room = {
        'code': 100,
        'data': {
          'subject_id': this.$store.state.subject_id
        }
      }
      this.sendWebSocketMessage(enter_room)
    },
    webSocketOnError (e) {
      console.error(e)
    },
    webSocketOnClose (e) {
      let leave_room = {
        'code': 130,
        'message': this.$store.state.subject_id
      }
      this.sendWebSocketMessage(leave_room)
    }
  },
  setup () {
    const alarm_sound = useSound(sound)

    return {
      alarm_sound
    }
  },
  store: store,
  router,
  render: h => h(App)
}).$mount('#app')
