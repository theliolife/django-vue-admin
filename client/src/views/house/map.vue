<template>
  <div>
    <el-row>
      <el-col>
        <el-amap
          ref="map"
          :vid="'amapDemo'"
          :center="center"
          :zoom="zoom"
          :plugin="plugin"
          :events="events"
          class="amap-demo"
          style="height: 900px;width: 100%">
          <el-amap-marker v-for="(u,i) in markers"
                          :position="u.position"
                          :events="u.events"
                          :key="i"></el-amap-marker>
          <el-amap-marker :position="this.position" :icon="icon">
          </el-amap-marker>
        </el-amap>
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
      searchParams: {
        title: '',
        floor: '',
        operate_time_start: '',
        operate_time_end: '',
      },
      drawer: true,
      direction: 'rtl',
      center: [116.28077, 39.91172],
      zoom: 15,
      position: [],
      icon: require('../../assets/icon/mark.png'),
      events: {
        init(o){
          console.log(o.getCenter());
        },
        click: e => {
          // alert('map clicked')
        }
      },
      map_path: '',
      map_name: '',
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
    houseList(this.searchParams).then((res) => {
      that.tableData = res.data.data

      that.tableData.map(function (item){
        that.markers.push({
          position: [item['longitude'], item['latitude']],
          content: item['title'] + item['floor'],
          events: {
            click: e => {
              alert((item['source'] == '5i5j' ? '我爱我家 ' : '贝壳 ') + item['title'] + item['floor'])
            }
          },
        })
      })
    })

    VueAMap.initAMapApiLoader({
      key: '1db68b73990b01267bfc63a1ce39e273',  //上面步骤提到的key复制过来
      plugin: [
        "AMap.Autocomplete", //输入提示插件
        "AMap.PlaceSearch", //POI搜索插件
        "AMap.Scale", //右下角缩略图插件 比例尺
        "AMap.OverView", //地图鹰眼插件
        "AMap.ToolBar", //地图工具条
        "AMap.MapType", //类别切换控件，实现默认图层与卫星图、实施交通图层之间切换的控制
        "AMap.PolyEditor", //编辑 折线多，边形
        "AMap.CircleEditor", //圆形编辑器插件
        "AMap.Geolocation" //定位控件，用来获取和展示用户主机所在的经纬度位置
      ],
      v: '1.4.4'
    });
  },
  methods: {
    handleClose(done) {
      done()
    },
    showMap(lat,lon,gaode,title){
      this.drawer = true
      let steps = JSON.parse(gaode)['route']['paths'][0]['steps']

      let tmp_path = null
      steps.map(function(item){
        if (!tmp_path){
          tmp_path = item['instruction']
        }else{
          tmp_path = tmp_path + '===>' + item['instruction']
        }
      })
      this.map_path = tmp_path
      this.map_name = title

      this.position = [lat,lon];
      this.asyncShowMap()
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
