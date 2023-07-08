<template>
  <el-amap
    ref="map2"
    :vid="'amap'"
    :center="[116.28077, 39.91172]"
    :zoom="15"
    class="amap-demo"
    style="position: absolute; width: 100%; height: 100%">
  </el-amap>
</template>

<script>
import VueAMap from 'vue-amap'

export default {
  data() {
    return {
      zoom: 15,
    }
  },
  mounted() {},
  methods: {
    showMap(){
      VueAMap.initAMapApiLoader({
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
