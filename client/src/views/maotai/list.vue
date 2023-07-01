<template>
  <el-row :style="{marginTop: '30px'}">
    <el-col :offset="1" :span="22">
      <el-card class="box-card">
        <el-table
          stripe
          border
          :row-class-name="tableRowClassName"
          :data="tableData.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
          style="width: 100%">

          <el-table-column label="名称" prop="name"></el-table-column>
          <el-table-column label="今天价格" prop="today_price"></el-table-column>
          <el-table-column label="昨天价格" prop="today_price"></el-table-column>
          <el-table-column label="查询日期" prop="date" align="right">
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
import {maotai_list} from "@/api/maotai";

export default {
  data() {
    return {
      tableData: [],
      search: ''
    }
  },
  mounted() {
    let that = this
    maotai_list({}).then((res) => {
      that.tableData = res.data.data
    })
  },
  methods: {
    tableRowClassName({row, rowIndex}) {
      if (row.name.indexOf("兔") !== -1) {
        return 'success-row';
      } else if (row.name.indexOf("活动") !== -1) {
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
