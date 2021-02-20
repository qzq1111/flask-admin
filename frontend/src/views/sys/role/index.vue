<template>
  <div class="app-container">
    <el-row>
      <el-form
        :inline="true"
        :model="search"
        class="demo-form-inline"
        size="small"
      >
        <el-form-item label="角色">
          <el-input v-model="search.role_name" placeholder="角色" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSearch">查询</el-button>
        </el-form-item>
      </el-form>
    </el-row>
    <el-row>
      <el-col style="text-align: right" :span="22">
        <el-button type="primary" size="small" @click="openAddRole">
          新增
        </el-button>
      </el-col>
    </el-row>

    <el-table
      v-loading="listLoading"
      :data="roleList"
      style="width: 100%"
      element-loading-text="Loading"
    >
      <el-table-column type="index" width="50" label="#"> </el-table-column>
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
          <el-button type="text" size="small">编辑</el-button>
          <el-button type="text" size="small">删除</el-button>
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
      v-if="addRoelVisible"
      title="新增角色"
      :visible="addRoelVisible"
      @close="addRoelVisible = false"
    >
      <el-form
        :model="addRoleForm"
        :rules="roleRules"
        ref="addRoleForm"
        label-width="80px"
      >
        <el-form-item label="角色" prop="role_name">
          <el-input
            v-model="addRoleForm.role_name"
            placeholder="请输入角色"
            autocomplete="off"
            style="width: 50%"
          ></el-input>
        </el-form-item>
        <el-form-item label="菜单权限" prop="menu_ids">
          <el-tree
            :data="menus"
            show-checkbox
            ref="role_tree"
            node-key="id"
            style="width: 50%"
          >
          </el-tree>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addRoelVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleAddRole('addRoleForm')"
          >确 定</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getRoleList, changeRoleStatus, addRole } from "@/api/role";
import { getMenuLabels } from "@/api/menu";
export default {
  data() {
    return {
      currentPage: 1,
      search: {
        role_name: "",
        page: 1,
        page_size: 10,
      },
      listLoading: true,
      total: 0,
      roleList: [],
      addRoelVisible: false,
      roleRules: {
        role_name: [
          { required: true, message: "请输入角色", trigger: "blur" },
          {
            min: 3,
            max: 20,
            message: "长度在 3 到 20 个字符",
            trigger: "blur",
          },
        ],
      },
      addRoleForm: {
        role_name: "",
        menu_ids: [],
      },
      menus: [],
    };
  },
  created() {
    this.fetchRoleListData();
  },
  methods: {
    openAddRole() {
      getMenuLabels().then((response) => {
        this.menus = response.data;
      });

      this.addRoleForm = {
        role_name: "",
        menu_ids: [],
      };
      this.addRoelVisible = true;
    },

    handleAddRole(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.addRoleForm.menu_ids = this.$refs.role_tree.getCheckedKeys();
          addRole(this.addRoleForm).then((res) => {
            this.$message.success("添加成功");
            this.addRoelVisible = false;
            this.$refs[formName].resetFields();
          });
        } else {
          return false;
        }
      });
    },
    // 修改角色状态
    handleStatusChange(row) {
      let text = row.status === 1 ? "启用" : "禁用";
      this.$confirm(
        "确认要" + text + ":" + row.role_name + " 角色吗?",
        "警告",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }
      )
        .then(function () {
          return changeRoleStatus(row.role_id, { status: row.status });
        })
        .then(() => {
          this.$message.success(text + "成功");
        })
        .catch(function () {
          row.status = row.status === 0 ? 1 : 0;
        });
    },
    // 搜索角色
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
    // 获取角色列表
    fetchRoleListData() {
      this.listLoading = true;
      getRoleList(this.search).then((response) => {
        this.roleList = response.data;
        this.total = response.total;
        this.listLoading = false;
      });
    },
  },
};
</script>

<style scoped>
</style>

