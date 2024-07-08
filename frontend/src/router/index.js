import Vue from 'vue'
import VueRouter from 'vue-router'
import VueSimpleAlert from 'vue-simple-alert'
/** Qualifications **/
import QualificationEntrance from '../views/recruit/QualificationEntrance.vue'
import PreSurvey from '../views/recruit/PreSurvey.vue'
import QualificationInstruction from '../views/recruit/QualificationInstruction.vue'
import QualifiedTask from '../views/recruit/QualifiedTask.vue'
import QualificationComplete from '../views/recruit/QualificationComplete.vue'
/** Common pages **/
/** Common pages - Instructions**/
import CommonEntrance from '../views/commons/CommonEntrance.vue'
import HitInstruction from '../views/commons/HitInstruction.vue'
import TaskInstruction from '../views/commons/TaskInstruction.vue'
import TrainInstruction from '../views/commons/TrainInstruction.vue'
import ModelInstruction from '../views/commons/ModelInstruction.vue'
/** Common pages - Practice tasks**/
import PracticeTask from '../views/commons/PracticeTask.vue'
import PracticeTruth from '../views/commons/PracticeTruth.vue'
import PracticeSummary from '../views/commons/PracticeSummary.vue'
/** Common pages - Exit pages**/
import PostSurvey from '../views/commons/PostSurvey.vue'
import UnderstandingSurvey from '../views/commons/UnderstandingSurvey.vue'
import AccountabilitySurvey from '../views/commons/AccountabilitySurvey.vue'
import BonusSummary from '../views/commons/BonusSummary.vue'
/** Group conditions**/
import GroupEntrance from '../views/group/GroupEntrance.vue'
import FormalInstruction from '../views/group/FormalInstruction.vue'
import DAInstruction from '../views/group/DAInstruction.vue'
import GroupInstruction from '../views/group/GroupInstruction.vue'
import NetiquetteRule from '../views/group/NetiquetteRule.vue'
import WaitingRoom from '../views/group/WaitingRoom.vue'
import FormalTask from '../views/group/FormalTask.vue'
/** Individual conditions**/
import SingleEntrance from '../views/individual/SingleEntrance.vue'
import SingleFormalInstruction from '../views/individual/SingleFormalInstruction.vue'
import SingleFormalTask from '../views/individual/SingleFormalTask.vue'
/** Errors **/
import KickOut from '../views/errors/KickOut.vue'
import FailPairing from '../views/errors/FailPairing.vue'
import FailAttention from '../views/errors/FailAttention.vue'
import PreviousPage from '../views/errors/PreviousPage.vue'
import FailQualification from '../views/errors/FailQualification.vue'
/** Without AI **/
import NoEntrance from '../views/withoutAI/NoEntrance.vue'
import NoHitInstruction from '../views/withoutAI/NoHitInstruction.vue'
import NoTaskInstruction from '../views/withoutAI/NoTaskInstruction.vue'
import NoTrainInstruction from '../views/withoutAI/NoTrainInstruction.vue'
import NoFormalInstruction from '../views/withoutAI/NoFormalInstruction.vue'
import NoFormalTask from '../views/withoutAI/NoFormalTask.vue'

Vue.use(VueRouter)
let previous_page = []
// let try_back = []

const routes = [
  {
    path: '/QualificationEntrance',
    name: 'QualificationEntrance',
    component: QualificationEntrance
  },
  {
    path: '/PreSurvey',
    name: 'PreSurvey',
    component: PreSurvey
  },
  {
    path: '/QualificationInstruction',
    name: 'QualificationInstruction',
    component: QualificationInstruction
  },
  {
    path: '/QualifiedTask/:taskid',
    name: 'QualifiedTask',
    component: QualifiedTask,
    props: true
  },
  {
    path: '/QualificationComplete',
    name: 'QualificationComplete',
    component: QualificationComplete
  },
  {
    path: '/CommonEntrance',
    name: 'CommonEntrance',
    component: CommonEntrance
  },
  {
    path: '/GroupEntrance',
    name: 'GroupEntrance',
    component: GroupEntrance
  },
  {
    path: '/SingleEntrance',
    name: 'SingleEntrance',
    component: SingleEntrance
  },
  {
    path: '/NetiquetteRule',
    name: 'NetiquetteRule',
    component: NetiquetteRule
  },
  {
    path: '/HitInstruction',
    name: 'HitInstruction',
    component: HitInstruction
  },
  {
    path: '/TaskInstruction',
    name: 'TaskInstruction',
    component: TaskInstruction
  },
  {
    path: '/ModelInstruction',
    name: 'ModelInstruction',
    component: ModelInstruction
  },
  {
    path: '/TrainInstruction',
    name: 'TrainInstruction',
    component: TrainInstruction
  },
  {
    path: '/PracticeTask/:taskid',
    name: 'PracticeTask',
    component: PracticeTask,
    props: true
  },
  {
    path: '/PracticeTruth/:taskid',
    name: 'PracticeTruth',
    component: PracticeTruth,
    props: true
  },
  {
    path: '/PracticeSummary',
    name: 'PracticeSummary',
    component: PracticeSummary
  },
  {
    path: '/FormalInstruction',
    name: 'FormalInstruction',
    component: FormalInstruction
  },
  {
    path: '/DAInstruction',
    name: 'DAInstruction',
    component: DAInstruction
  },
  {
    path: '/GroupInstruction',
    name: 'GroupInstruction',
    component: GroupInstruction
  },
  {
    path: '/SingleFormalInstruction',
    name: 'SingleFormalInstruction',
    component: SingleFormalInstruction
  },
  {
    path: '/WaitingRoom',
    name: 'WaitingRoom',
    component: WaitingRoom
  },
  {
    path: '/FormalTask/:taskid',
    name: 'FormalTask',
    component: FormalTask,
    props: true
  },
  {
    path: '/SingleFormalTask/:taskid',
    name: 'SingleFormalTask',
    component: SingleFormalTask,
    props: true
  },
  {
    path: '/PostSurvey',
    name: 'PostSurvey',
    component: PostSurvey
  },
  {
    path: '/UnderstandingSurvey',
    name: 'UnderstandingSurvey',
    component: UnderstandingSurvey
  },
  {
    path: '/AccountabilitySurvey/:taskid',
    name: 'AccountabilitySurvey',
    component: AccountabilitySurvey,
    props: true
  },
  {
    path: '/BonusSummary',
    name: 'BonusSummary',
    component: BonusSummary
  },
  {
    path: '/KickOut',
    name: 'KickOut',
    component: KickOut
  },
  {
    path: '/FailPairing',
    name: 'FailPairing',
    component: FailPairing
  },
  {
    path: '/FailAttention',
    name: 'FailAttention',
    component: FailAttention
  },
  {
    path: '/PreviousPage',
    name: 'PreviousPage',
    component: PreviousPage
  },
  {
    path: '/NoEntrance',
    name: 'NoEntrance',
    component: NoEntrance
  },
  {
    path: '/NoHitInstruction',
    name: 'NoHitInstruction',
    component: NoHitInstruction
  },
  {
    path: '/NoTaskInstruction',
    name: 'NoTaskInstruction',
    component: NoTaskInstruction
  },
  {
    path: '/NoTrainInstruction',
    name: 'NoTrainInstruction',
    component: NoTrainInstruction
  },
  {
    path: '/NoFormalInstruction',
    name: 'NoFormalInstruction',
    component: NoFormalInstruction
  },
  {
    path: '/NoFormalTask/:taskid',
    name: 'NoFormalTask',
    component: NoFormalTask,
    props: true
  },
  {
    path: '/FailQualification',
    name: 'FailQualification',
    component: FailQualification
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (previous_page.indexOf(to.path) === -1) {
    previous_page.push(from.path)
    next()
  } else {
    VueSimpleAlert.confirm('Do you want to give up the HIT?', 'If you leave, you could not earn the reward.', 'warning').then((result) => {
      if (result) {
        router.push('/PreviousPage')
      }
    }).catch(e => {
      console.error(e)
    })
  }
})

export default router
