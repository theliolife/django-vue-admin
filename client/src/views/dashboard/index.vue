<template>
  <div class="dashboard-container">
    <div class="dashboard-text">name: {{ name }}</div>
    <div class="dashboard-text">perms: <span v-for="perm in perms" :key="perm">{{ perm }}</span></div>
    <div class="home">
      <ChartLine ref="chart_line_one" />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ChartLine from '../../components/charts/charts_line.vue'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name',
      'perms'
    ])
  },
  components: {
    ChartLine
  },
  data() {
    return {
      xData: ['2020-02', '2020-03', '2020-04', '2020-05'],
      yData: [30, 132, 80, 134]
    }
  },
  mounted() {
    const { xData, yData } = this;
    console.log(this.$refs)
    this.$refs.chart_line_one.initChart('line_data', xData, yData)
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
