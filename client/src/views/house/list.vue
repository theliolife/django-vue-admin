<template>
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
          <el-table-column label="价格" prop="price"></el-table-column>
          <el-table-column label="面积" prop="size"></el-table-column>
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
</template>

<script>
import {houseList, houseDashboard} from "@/api/house";

export default {
  data() {
    return {
      tableData: [],
      search: ''
    }
  },
  mounted() {
    let that = this
    houseList({}).then((res) => {
      that.tableData = res.data.data
    })
  },
  methods: {
    tableRowClassName({row, rowIndex}) {
      if (row.title.indexOf("3号院") !== -1) {
        return 'success-row';
      } else if (row.title.indexOf("36号院") !== -1) {
        return 'warning-row';
      }
      return '';
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
