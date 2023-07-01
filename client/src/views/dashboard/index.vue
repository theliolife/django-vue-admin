<template>
  <div class="dashboard-container">
    <!--    <div class="dashboard-text">name: {{ name }}</div>-->
    <!--    <div class="dashboard-text">perms: <span v-for="perm in perms" :key="perm">{{ perm }}</span></div>-->
    <el-row>
      <el-col :span="24">
        <template>
          <div>
            <el-row :gutter="20">
              <el-col :span="4">
                <div>
                  <el-statistic group-separator="," :precision="2" :value="value2" :title="title"></el-statistic>
                </div>
              </el-col>
              <el-col :span="4">
                <div>
                  <el-statistic title="茅台预约">
                    <template slot="formatter"> 456/2 </template>
                  </el-statistic>
                </div>
              </el-col>
              <el-col :span="4">
                <div>
                  <el-statistic group-separator="," :precision="2" decimal-separator="." :value="value1" title="出租房数量">
                    <template slot="prefix">
                      <i class="el-icon-s-flag" style="color: red"></i>
                    </template>
                    <template slot="suffix">
                      <i class="el-icon-s-flag" style="color: blue"></i>
                    </template>
                  </el-statistic>
                </div>
              </el-col>
              <el-col :span="4">
                <div>
                  <el-statistic :value="like ? 521 : 520" title="上涨/下跌数">
                    <template slot="suffix">
              <span @click="like = !like" class="like">
                <i class="el-icon-star-on" style="color:red" v-show="!!like"></i>
                <i class="el-icon-star-off" v-show="!like"></i>
              </span>
                    </template>
                  </el-statistic>
                </div>
              </el-col>
              <el-col :span="4">
                <div>
                  <el-statistic group-separator="," :precision="2" decimal-separator="." :value="value1" title="北向流向">
                    <template slot="prefix">
                      <i class="el-icon-s-flag" style="color: red"></i>
                    </template>
                    <template slot="suffix">
                      <i class="el-icon-s-flag" style="color: blue"></i>
                    </template>
                  </el-statistic>
                </div>
              </el-col>
              <el-col :span="4">
                <div>
                  <el-statistic :value="like ? 521 : 520" title="Feedback">
                    <template slot="suffix">
              <span @click="like = !like" class="like">
                <i class="el-icon-star-on" style="color:red" v-show="!!like"></i>
                <i class="el-icon-star-off" v-show="!like"></i>
              </span>
                    </template>
                  </el-statistic>
                </div>
              </el-col>
            </el-row>
          </div>
        </template>
      </el-col>
    </el-row>

    <el-row :gutter="20" :style="{marginTop: '30px'}">
      <el-col :span="8">
        <el-card class="box-card">
          <ChartDom ref="chart_dom_one"/>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card class="box-card">
          <HouseTrend ref="house_trend" :p-method="showDraw"/>
        </el-card>
      </el-col>
    </el-row>

    <el-row :style="{marginTop: '20px'}">
      <el-col :span="24">
        <el-card class="box-card">
          <ChartLine ref="chart_line_one"/>
        </el-card>
      </el-col>
    </el-row>

    <el-row>
      <el-col>
        <el-button @click="drawer = true" type="primary" style="margin-left: 16px;">
          点我打开
        </el-button>
        <el-drawer
          title="我是标题"
          size="70%"
          :visible.sync="drawer"
          :direction="direction"
          :style="{padding:'20px'}"
          :before-close="handleClose">
          <el-row>
            <el-col :offset="1" :span="22">
              <el-table
                :data="tableData"
                height="250"
                border
                style="width: 100%">
                <el-table-column
                  prop="date"
                  label="日期"
                  width="180">
                </el-table-column>
                <el-table-column
                  prop="name"
                  label="姓名"
                  width="180">
                </el-table-column>
                <el-table-column
                  prop="address"
                  label="地址">
                </el-table-column>
              </el-table>
            </el-col>
          </el-row>
        </el-drawer>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ChartLine from '../../components/dashboard/charts_line.vue'
import ChartDom from '../../components/dashboard/house_rate.vue'
import HouseTrend from '../../components/dashboard/house_trend'
import { houseDashboard } from '@/api/house'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name',
      'perms'
    ])
  },
  components: {
    ChartLine,
    ChartDom,
    HouseTrend
  },
  data() {
    return {
      xData: ['2020-02', '2020-03', '2020-04', '2020-05'],
      yData: [30, 132, 80, 134],

      drawer: false,
      direction: 'rtl',
      tableData: [{
        date: '2016-05-03',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-02',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-04',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-01',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-08',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-06',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-07',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }],
      like: true,
      value1: 4154.564,
      value2: 2222,
      title: '今年的增长'
    }
  },
  mounted() {
    const { xData, yData } = this
    this.$refs['chart_line_one'].initChart('line_data', xData, yData)
    this.$refs['chart_dom_one'].initChart('line_data', xData, yData)
    this.$refs['house_trend'].initHouseBarChart('line_data', xData, yData)

    houseDashboard({ name: 1 }).then((res) => {
      console.log(123)
      console.log(res)
    })
  },
  methods: {
    handleClose(done) {
      done()
      // this.$confirm('确认关闭？')
      //   .then(_ => {
      //     done()
      //   }).catch(_ => {})
    },
    showDraw(params) {
      console.log(params)
      this.drawer = true
    }
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

    .like {
      cursor: pointer;
      font-size: 25px;
      display: inline-block;
    }
  }
</style>
