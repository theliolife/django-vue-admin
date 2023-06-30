<template>
  <div id="echart-dom" class="echart transition-box" :style="{width: '100%', height: '400px'}" />
</template>

<script>
import echarts from 'echarts'

export default {
  methods: {
    initChart(name, xData, yData) {
      const getchart = echarts.init(document.getElementById('echart-dom'))
      const labelRight = {
        position: 'right'
      }

      const option = {
        color: ['#4992FF'],
        title: {
          text: 'Bar Chart with Negative Value'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          top: 80,
          bottom: 30
        },
        xAxis: {
          type: 'value',
          position: 'top',
          splitLine: {
            lineStyle: {
              type: 'dashed'
            }
          }
        },
        yAxis: {
          type: 'category',
          axisLine: { show: false },
          axisLabel: { show: false },
          axisTick: { show: false },
          splitLine: { show: false },
          data: [
            'ten',
            'nine',
            'eight',
            'seven',
            'six',
            'five',
            'four',
            'three',
            'two',
            'one'
          ]
        },
        series: [
          {
            name: 'Cost',
            type: 'bar',
            stack: 'Total',
            label: {
              show: true,
              formatter: '{b}'
            },
            data: [
              { value: -0.07, label: labelRight },
              { value: -0.09, label: labelRight },
              0.2,
              0.44,
              { value: -0.23, label: labelRight },
              0.08,
              { value: -0.17, label: labelRight },
              0.47,
              { value: -0.36, label: labelRight },
              0.18
            ]
          }
        ]
      }

      option && getchart.setOption(option)
      // 随着屏幕大小调节图表
      window.addEventListener('resize', () => {
        getchart.resize()
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
