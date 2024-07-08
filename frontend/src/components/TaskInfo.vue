<template>
  <b-container fluid>
    <div class='task-info text-center'>
      <b-row>
        <b-col cols="2" id='race_title' class='task-info-title'>Race</b-col>
        <b-tooltip target='race_title' triggers='hover' variant='Dark'>
          Defendant's self-identified race
        </b-tooltip>
        <b-col cols="2" class='task-info-data'>{{defendant.race}}</b-col>
        <b-col cols="2" id='sex_title' class='task-info-title'>Sex</b-col>
        <b-tooltip target='sex_title' triggers='hover' variant='Dark'>
          Defendant's biological sex
        </b-tooltip>
        <b-col cols="2" class='task-info-data'>{{defendant.sex}}</b-col>
        <b-col cols="2" id='age_title' class='task-info-title'>Age</b-col>
        <b-tooltip target='age_title' triggers='hover' variant='Dark'>
          Defendent's age
        </b-tooltip>
        <b-col cols="2" class='task-info-data'>{{defendant.age}}</b-col>
      </b-row>
      <b-row class='second_row'>
        <b-col cols="8" id='prior_title' class='task-info-title'>Prior Crime Count after Age 18</b-col>
        <b-tooltip target='prior_title' triggers='hover' variant='Dark' placement='right'>
          The total number of criminal charges that the defendant had after 18 and before the current charge
        </b-tooltip>
        <b-col cols="4" class='task-info-data'>{{defendant.prior}}</b-col>
      </b-row>
      <b-row>
        <b-col cols="8" id='felony_title' class='task-info-title'>Felony Crime Count before Age 18</b-col>
        <b-tooltip target='felony_title' triggers='hover' variant='Dark' placement='bottom'>
          The total number of felony criminal charges that the defendant had before 18.<br><br>Felony offenses can only be handled by circuit court judges and are punishable by the possibility of more than one-year in prison.
        </b-tooltip>
        <b-col cols="4" class='task-info-data'>{{defendant.felony}}</b-col>
      </b-row>
      <b-row>
        <b-col cols="8" id='misdemeanor_title' class='task-info-title'>Misdemeanor Count before Age 18</b-col>
        <b-tooltip target='misdemeanor_title' triggers='hover' variant='Dark' placement='bottom'>
          The total number of misdemeanor criminal charges that the defendant had before 18. Misdemeanor offenses are
          <ul>
            <li>Petit (petty) theft</li>
            <li>Domestic violence</li>
            <li>Shoplifting</li>
            <li>Vandalism</li>
            <li>Driving under the influence (DUI)</li>
            <li>Possession of less than 20 grams of marijuana</li>
          </ul>
        </b-tooltip>
        <b-col cols="4" class='task-info-data'>{{defendant.misdemeanor}}</b-col>
      </b-row>
      <b-row>
        <b-col cols="3" id='charge_degree_title' class='task-info-title'>Current Charge Degree</b-col>
        <b-tooltip target='charge_degree_title' triggers='hover' variant='Dark' placement='right'>
          Whether the current criminal charge of the defendant is felony or misdemeanor.
        </b-tooltip>
        <b-col cols="9" class='task-info-data'>{{defendant.charge_degree}}</b-col>
      </b-row>
      <b-row>
        <b-col cols="3" id='charge_reason_title' class='task-info-title'>Current Charge Issue</b-col>
        <b-tooltip target='charge_reason_title' triggers='hover' variant='Dark' placement='right'>
          The reason for the defendant's current criminal charge
        </b-tooltip>
        <b-col cols="9" class='task-info-data'>{{defendant.charge_reason}}<br>*{{defendant.charge_reason}}: {{defendant.charge_explain}}</b-col>
      </b-row>
    </div>
  </b-container>
</template>
<script>
export default {
  props: {
    defendant: {
      type: Object,
      default: function () {
        return {
          race: 'null',
          sex: 'null',
          age: 'null',
          prior: 'null',
          felony: 'null',
          misdemeanor: 'null',
          charge_reason: 'null',
          charge_degree: 'null',
          charge_explain: 'null'
        }
      }
    }
  }
}
</script>
<style>
</style>
