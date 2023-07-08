<template>
  <div>
    <el-row :style="{marginTop: '30px'}">
      <el-col :offset="1" :span="22">
        <el-card class="box-card">
          <el-table
            stripe
            :row-class-name="tableRowClassName"
            :data="tableData.filter(data => !search || data.title.toLowerCase().includes(search.toLowerCase()))"
            style="width: 100%">

            <el-table-column type="expand">
              <template slot-scope="props">
                <el-card class="box-card">
                  <el-form label-position="left" inline class="demo-table-expand">
                    <el-form-item label="头图">
                      <el-row :gutter="10">
                        <el-col>
                          <img :style="{width:'100%'}" :src="props.row.img"/>
                        </el-col>
                      </el-row>
                    </el-form-item>
                  </el-form>

                  <el-form label-position="left" inline class="demo-table-expand">
                    <el-form-item label="其他">
                      <el-row :gutter="10">
                        <el-col :span="4" v-for="i in [1,2,3,4,5]">
                          <img :style="{width:'100%'}" src="https://pic.imgdb.cn/item/646b1a07e03e90d874aef456.jpg">
                        </el-col>
                      </el-row>
                    </el-form-item>
                  </el-form>
                </el-card>
              </template>
            </el-table-column>

            <el-table-column label="地址" prop="title">
              <template slot-scope="scope">
                <i class="el-icon-time"></i>
                <a :href="scope.row.url" target="_blank" style="margin-left: 10px">{{ scope.row.title }}</a>
              </template>
            </el-table-column>
            <el-table-column width="100" label="价格" prop="price"></el-table-column>
            <el-table-column width="100" label="面积" prop="size"></el-table-column>
            <el-table-column label="楼层" prop="floor"></el-table-column>
            <el-table-column label="步行距离" prop="gaode">
              <template slot-scope="scope">
                <el-button @click="showMap(scope.row.longitude, scope.row.latitude)">
                  {{scope.row.gaode}}
                </el-button>
              </template>
            </el-table-column>
            <el-table-column label="最后维护日期" prop="operate_time" align="right">
              <template slot="header" slot-scope="scope">
                <el-input
                  v-model="search"
                  size="mini"
                  placeholder="输入关键字搜索"/>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-row>
      <el-col>
        <el-button @click="drawer = true" type="primary" style="margin-left: 16px;">
          点我打开
        </el-button>
        <el-drawer
          title="房屋所在位置"
          size="70%"
          :visible.sync="drawer"
          :direction="direction"
          :style="{padding:'20px'}"
          :before-close="handleClose">
          <el-row>
            <el-col :offset="1" :span="22">
              <div class="amap-wrapper">
                <el-amap
                  ref="map"
                  :vid="'amapDemo'"
                  :center="center"
                  :zoom="zoom"
                  :plugin="plugin"
                  :events="events"
                  class="amap-demo"
                  style="height: 600px;width: 100%">
                  <el-amap-marker v-for="(u,i) in markers" :position="u.position" :key="i"></el-amap-marker>
                  <el-amap-marker :position="this.position">
                  </el-amap-marker>
                </el-amap>
              </div>
            </el-col>
          </el-row>
        </el-drawer>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import {houseList, houseDashboard} from "@/api/house";

import VueAMap from 'vue-amap'

export default {
  data() {
    return {
      tableData: [],
      search: '',

      drawer: false,
      direction: 'rtl',

      center: [116.28077, 39.91172],
      zoom: 15,
      position: [],
      // icon: require('../../assets/icon/pika.jpg'),
      icon: '',
      events: {
        init(o){
          console.log(o.getCenter());
        },
        click: e => {
          alert('map clicked')
        }
      },
      markers: [],
      //使用其他组件
      plugin: [
        {
          pName: 'Scale',
          events: {
            init(instance) {
              console.log(instance)
            }
          }
        },
        {
          pName: 'ToolBar',
          events: {
            init(instance) {
              console.log(instance)
            }
          }
        }
      ],
    }
  },
  mounted() {
    let that = this
    houseList({}).then((res) => {
      that.tableData = res.data.data

      // that.tableData.map(function (item){
      //   that.markers.push({
      //     position: [item['longitude'], item['latitude']]
      //   })
      // })
    })

    VueAMap.initAMapApiLoader({
      key: '1db68b73990b01267bfc63a1ce39e273',  //上面步骤提到的key复制过来
      plugin: ['AMap.Autocomplete', 'AMap.PlaceSearch', 'AMap.Scale', 'AMap.OverView', 'AMap.ToolBar', 'AMap.MapType', 'AMap.PolyEditor', 'AMap.CircleEditor'],
      v: '1.4.4'
    });
  },
  methods: {
    tableRowClassName({row, rowIndex}) {
      if (row.title.indexOf("3号院") !== -1) {
        return 'success-row';
      } else if (row.title.indexOf("36号院") !== -1) {
        return 'warning-row';
      }
      return '';
    },
    handleClose(done) {
      done()
    },
    showMap(lat,lon){
      this.drawer = true

      this.position = [lat,lon];
      this.asyncShowMap()
      console.log(this.position)
      this.$forceUpdate()
    },
    async asyncShowMap() {
      await VueAMap.initAMapApiLoader({
        key: '1db68b73990b01267bfc63a1ce39e273',  //上面步骤提到的key复制过来
        plugin: ['AMap.Autocomplete', 'AMap.PlaceSearch', 'AMap.Scale', 'AMap.OverView', 'AMap.ToolBar', 'AMap.MapType', 'AMap.PolyEditor', 'AMap.CircleEditor'],
        v: '1.4.4'
      });
    }
  },
}
</script>


<style>
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}
</style>
