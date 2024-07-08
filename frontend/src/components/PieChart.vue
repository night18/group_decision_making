<template>
  <b-container>
    <b-row>
      <b-col lg="6" class="pie_col" order-lg="1">
        <div class="pie_div">
          <p v-for="percentage in get_percentage" :key="percentage.subject">
            {{percentage.subject}} should take {{percentage.percent}}% of the {{get_credit_term}} for this {{get_correct_term}} prediction.
          </p>
        </div>
      </b-col>
      <b-col lg="6" order-lg="0">
        <div :id="'pie' + pie_id">
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>
<script>
import * as d3 from 'd3'
export default {
  name: 'PieChart',
  props: [
    'pie_id', 'condition', 'credit'
  ],
  data: function () {
    return {
      responsibility: [
        {subject: 'Me', value: 100},
        {subject: 'The model', value: 100},
        {subject: 'My teammates', value: 100}
      ]
    }
  },
  methods: {
    setValue (index, value) {
      this.$set(this.responsibility[index], 'value', value)
      const data = {
        pie_id: this.pie_id,
        responsibility: this.responsibility
      }
      this.$emit('responsibility', data)
    },
    generatePie () {
      const _id = '#pie' + this.pie_id
      const vueInstance = this
      let w = 400
      let h = 400
      let margin = 30
      let radius = Math.min(w, h) / 2 - margin

      d3.select(_id + ' svg').remove()

      let svg = d3
        .select(_id)
        .append('svg')
        .attr('width', w)
        .attr('height', h)
      const color = d3.scaleOrdinal(['#C9CBA3', '#FFE1A8', '#E26D5C', '#723D46', '#472D30'])

      const pie = d3
        .pie()
        .sort(null)
        .value(d => { return d.value })

      const data_ready = pie(this.responsibility)

      const arcGenerator = d3.arc()
        .innerRadius(0)
        .outerRadius(radius)

      let selected_node, next_section, section_id

      function draglistener (selection, event_type) {
        if (event_type === 'dragstart') {
          selected_node = selection
          selected_node
            .transition()
            .duration(1)
            .attr('r', 10)
            .attr('stroke-width', 5)
          section_id = selected_node._groups[0][0].__data__.index
          next_section = data_ready[ (section_id + 1) % data_ready.length ]
        } else if (event_type === 'dragon') {
          const hypot = Math.sqrt((selection.x * selection.x) + (selection.y * selection.y))
          let isleft
          if (selection.x >= 0) {
            if (selection.x === 0 && selection.y < 0) {
              isleft = true
            }
            isleft = false
          } else {
            isleft = true
          }
          let angle
          if (isleft) {
            angle = 2 * Math.PI - Math.abs(Math.acos(-1 * selection.y / hypot))
          } else {
            angle = Math.abs(Math.acos(-1 * selection.y / hypot))
          }

          const next_limit = next_section.endAngle
          const prev_limit = selected_node._groups[0][0].__data__.startAngle

          if (angle < prev_limit) {
            angle += Math.PI * 2
          }
          if (angle < next_limit) {
            selected_node
              .attr('cx', (selection.x / hypot) * radius)
              .attr('cy', (selection.y / hypot) * radius)

            vueInstance.setValue(section_id, 300 * (angle - prev_limit) / (Math.PI * 2))
            vueInstance.setValue((section_id + 1) % vueInstance.responsibility.length, 300 * (next_limit - angle) / (Math.PI * 2))
          }
        } else if (event_type === 'dragend') {
          selected_node
            .transition()
            .duration(1)
            .attr('r', 5)
            .attr('stroke-width', 2)
          vueInstance.generatePie()
        }
      }

      const drag = d3.drag()
        .on('start', function () {
          draglistener(d3.select(this), 'dragstart')
        })
        .on('drag', function (event) {
          draglistener(event, 'dragon')
        })
        .on('end', function () {
          draglistener(d3.select(this), 'dragend')
        })

      const g = svg.append('g')
      g.selectAll('.sector')
        .data(data_ready)
        .enter()
        .append('path')
        .attr('class', 'sector')
        .attr('d', arcGenerator)
        .attr('fill', (d, i) => color(i))
        .attr('stroke', 'white')
        .attr('stroke-width', '1px')

      g.selectAll('.label')
        .data(data_ready)
        .enter()
        .append('text')
        .attr('class', 'label')
        .attr('dy', '0em')
        .text(d => `${d.data.subject}`)
        .attr('transform', function (d) { return 'translate(' + arcGenerator.centroid(d) + ')' })
        .style('text-anchor', 'middle')

      g.selectAll('.ratio')
        .data(data_ready)
        .enter()
        .append('text')
        .attr('class', 'ratio')
        .attr('dy', '1em')
        .text(d => `${(d.data.value / 3).toFixed(1)}%`)
        .attr('transform', function (d) { return 'translate(' + arcGenerator.centroid(d) + ')' })
        .style('text-anchor', 'middle')

      g.selectAll('.sector_button')
        .data(data_ready)
        .enter()
        .filter(function (d, i) {
          return i !== data_ready.length - 1
        })
        .append('circle')
        .attr('class', 'sector_button')
        .attr('cx', function (d, i) {
          return (Math.sin(d.endAngle)) * radius
        })
        .attr('cy', function (d) {
          return -(Math.cos(d.endAngle)) * radius
        })
        .attr('r', 5)
        .attr('fill', 'white')
        .attr('stroke', (d, i) => color(i))
        .attr('stroke-width', 2)
        .call(drag)

      g.attr('transform', `translate(${Math.min(w, h) / 2},${Math.min(w, h) / 2})`)
    }
  },
  computed: {
    get_percentage () {
      let percentage = []
      for (let i = 0; i < this.responsibility.length; i++) {
        let subject = this.responsibility[i].subject
        if (subject === 'Me') {
          subject = 'I'
        }
        percentage.push({ subject: subject, percent: (this.responsibility[i].value / 3).toFixed(1) })
      }
      return percentage
    },
    get_credit_term () {
      return this.credit ? 'credit' : 'responsibility'
    },
    get_correct_term () {
      return this.credit ? 'correct' : 'wrong'
    }
  },
  mounted () {
    if (this.condition === 0) {
      // group condition
      this.responsibility = [
        {subject: 'Me', value: 100},
        {subject: 'The model', value: 100},
        {subject: 'My teammates', value: 100}
      ]
      this.setValue(0, 100)
      this.setValue(1, 100)
      this.setValue(2, 100)
      this.generatePie()
    } else if (this.condition === 1) {
      // individual condition
      this.responsibility = [
        {subject: 'Me', value: 150},
        {subject: 'The model', value: 150}
      ]
      this.setValue(0, 150)
      this.setValue(1, 150)
      this.generatePie()
    }
  },
  beforeDestroy () {
  }
}
</script>
<style scoped>
  .pie_col {
    margin: auto 0;
  }

  .pie_div {
    margin-top: 10px;
    padding: 5px;
    border: solid #1897AE 2px;
  }
</style>
