<template>
  <div class="app-container">
    <el-row>
      <el-form
        :inline="true"
        :model="search"
        class="demo-form-inline"
        size="small"
      >
        <el-form-item label="账号">
          <el-input v-model="search.user_name" placeholder="账号" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSearch">查询</el-button>
        </el-form-item>
      </el-form>
    </el-row>
    <el-row>
      <el-col style="text-align: right" :span="22">
        <el-button type="primary" size="small" @click="onAddUser"
          >新增</el-button
        >
      </el-col>
    </el-row>

    <el-table
      v-loading="listLoading"
      :data="userList"
      style="width: 100%"
      element-loading-text="Loading"
    >
      <el-table-column type="index" width="50" label="#"> </el-table-column>
      <el-table-column prop="user_name" label="账号"> </el-table-column>
      <el-table-column prop="role_name" label="角色"> </el-table-column>
      <el-table-column label="状态">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.status"
            :active-value="1"
            :inactive-value="0"
            @change="handleStatusChange(scope.row)"
          >
          </el-switch>
        </template>
      </el-table-column>
      <el-table-column prop="create_time" label="创建时间"> </el-table-column>
      <el-table-column fixed="right" label="操作">
        <template>
          <el-button type="text" size="small">查看</el-button>
          <el-button type="text" size="small">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="search.page"
      :page-sizes="[10, 20, 50, 100]"
      :page-size="search.page_size"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
    >
    </el-pagination>
    <userTemplate
      v-if="userVisible"
      :visible="userVisible"
      @close="userVisible = false"
    ></userTemplate>
  </div>
</template>

<script>
import { getUserList, changeUserStatus } from "@/api/user";
import userTemplate from "./userTemplate";
export default {
  components: {
    userTemplate,
  },
  data() {
    return {
      userVisible: false,
      listLoading: true,
      total: 0,
      search: {
        user_name: "",
        page: 1,
        page_size: 10,
      },
      userList: [],
    };
  },
  created() {
    this.fetchUserListData();
  },
  methods: {
    onAddUser() {
      this.userVisible = true;
    },
    handleStatusChange(row) {
      console.log(row);
      let text = row.status === 1 ? "启用" : "禁用";
      this.$confirm(
        "确认要" + text + ":" + row.user_name + " 用户吗?",
        "警告",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }
      )
        .then(function () {
          return changeUserStatus(row.user_id, { status: row.status });
        })
        .then(() => {
          this.$message.success(text + "成功");
        })
        .catch(function () {
          row.status = row.status === 0 ? 1 : 0;
        });
    },

    onSearch() {
      this.search.page = 1;
      this.fetchUserListData();
    },
    handleSizeChange(val) {
      this.search.page_size = val;
      this.fetchUserListData();
    },
    handleCurrentChange(val) {
      this.search.page = val;
      this.fetchUserListData();
    },

    fetchUserListData() {
      this.listLoading = true;
      getUserList(this.search).then((response) => {
        this.userList = response.data;
        this.total = response.total;
        this.listLoading = false;
      });
    },
  },
};
</script>

<style scoped>
</style>

