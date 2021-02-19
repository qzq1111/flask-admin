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
        <el-button type="primary" size="small" @click="onOpenAddUser">
          新增
        </el-button>
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

    <el-dialog
      v-if="userVisible"
      title="新增用户"
      :visible="userVisible"
      @close="userVisible = false"
    >
      <el-form
        :model="userForm"
        :rules="userRules"
        ref="userForm"
        label-width="80px"
      >
        <el-form-item label="账号" prop="user_name">
          <el-input
            v-model="userForm.user_name"
            placeholder="请输入账号"
            autocomplete="off"
            style="width: 50%"
          ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="userForm.password"
            placeholder="请输入密码"
            type="password"
            style="width: 50%"
          ></el-input>
        </el-form-item>
        <el-form-item label="角色" prop="role_id">
          <el-select
            v-model="userForm.role_id"
            placeholder="请选择角色"
            style="width: 50%"
          >
            <el-option
              v-for="item in roleLabels"
              :key="item.role_id"
              :label="item.role_name"
              :value="item.role_id"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="userVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleAddUser('userForm')"
          >确 定</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getUserList, changeUserStatus } from "@/api/user";
import { getRoleLabels } from "@/api/role";
export default {
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
      userForm: {
        user_name: "",
        password: "",
        role_id: "",
      },
      roleLabels: [],
      userRules: {
        user_name: [
          { required: true, message: "请输入账号", trigger: "blur" },
          {
            min: 3,
            max: 20,
            message: "长度在 3 到 20 个字符",
            trigger: "blur",
          },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { min: 6, message: "至少6个字符", trigger: "blur" },
        ],
        role_id: [{ required: true, message: "请选择角色", trigger: "change" }],
      },
    };
  },
  created() {
    this.fetchUserListData();
  },
  methods: {
    // 打开添加用户界面
    onOpenAddUser() {
      this.userForm = {
        user_name: "",
        password: "",
        role_id: "",
      };
      getRoleLabels().then((response) => {
        this.roleLabels = response.data;
      });
      this.userVisible = true;
    },
    // 添加用户
    handleAddUser(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          console.log(this.userForm);
          this.userVisible = false;
          this.$refs[formName].resetFields();
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    // 修改用户状态
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
    // 搜索用户
    onSearch() {
      this.search.page = 1;
      this.fetchUserListData();
    },
    // 修改每页数据量
    handleSizeChange(val) {
      this.search.page_size = val;
      this.fetchUserListData();
    },
    // 修改当前页
    handleCurrentChange(val) {
      this.search.page = val;
      this.fetchUserListData();
    },
    // 获取用户列表
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

