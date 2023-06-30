<template>
  <div id="house_trend" class="echart transition-box" :style="{width: '100%', height: '400px'}" />
</template>

<script>
import echarts from 'echarts'

export default {
  props: {
    pMethod: {
      type: Function,
      default: null
    }
  },
  methods: {
    initHouseBarChart(name, xData, yData) {
      const getchart = echarts.init(document.getElementById('house_trend'))

      const option = {
        xAxis: {
          type: 'category',
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [120, 200, 150, 80, 70, 110, 130],
            type: 'bar',
            showBackground: true,
            backgroundStyle: {
              color: 'rgba(180, 180, 180, 0.2)'
            }
          }
        ]
      }

      option && getchart.setOption(option)
      // 随着屏幕大小调节图表
      window.addEventListener('resize', () => {
        getchart.resize()
      })

      const that = this
      getchart.getZr().on('click', function(params) {
        if (that.pMethod) {
          that.pMethod(params)
        }
      })
    }
  }
}
</script>

<style>
  .transition-box {
    margin-bottom: 10px;
    width: 200px;
    height: 100px;
    border-radius: 4px;
    background-color: #ffffff;
    text-align: center;
    color: #fff;
    padding: 40px 20px;
    box-sizing: border-box;
    margin-right: 20px;
  }
</style>
