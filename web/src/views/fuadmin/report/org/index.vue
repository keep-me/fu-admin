<template>
  <div class="p-4">
    <Row :gutter="[16, 16]">
      <Col :span="6" v-for="(card, index) in overviewCards" :key="index">
        <Card hoverable>
          <Statistic
            :title="card.title"
            :value="card.value"
            :value-style="{ color: card.color }"
          />
        </Card>
      </Col>
    </Row>

    <Row :gutter="[16, 16]" class="mt-4">
      <Col :span="12">
        <Card title="部门用户分布" class="enter-y">
          <template #extra>
            <Button type="primary" @click="handleExportDept">
              <DownloadOutlined />
              导出
            </Button>
          </template>
          <DeptChart :data="deptData" height="350px" title="" />
        </Card>
      </Col>
      <Col :span="12">
        <Card title="角色用户分布" class="enter-y">
          <template #extra>
            <Button type="primary" @click="handleExportRole">
              <DownloadOutlined />
              导出
            </Button>
          </template>
          <RoleChart :data="roleData" height="350px" title="" />
        </Card>
      </Col>
    </Row>
  </div>
</template>

<script lang="ts" setup>
  import { ref, reactive, onMounted } from 'vue';
  import { Row, Col, Card, Statistic, Button, message } from 'ant-design-vue';
  import { DownloadOutlined } from '@ant-design/icons-vue';
  import DeptChart from '../components/DeptChart.vue';
  import RoleChart from '../components/RoleChart.vue';
  import {
    getDeptOverview,
    getDeptDistribution,
    getRoleOverview,
    getRoleDistribution,
    exportDept,
    exportRole,
  } from '../report.api';
  import type { DeptDistributionItem, RoleDistributionItem } from '../components/props';

  const deptData = ref<DeptDistributionItem[]>([]);
  const roleData = ref<RoleDistributionItem[]>([]);

  const overviewCards = reactive([
    { title: '部门总数', value: 0, color: '#1890ff' },
    { title: '活跃部门', value: 0, color: '#52c41a' },
    { title: '总用户数', value: 0, color: '#E6A23C' },
    { title: '角色总数', value: 0, color: '#019680' },
  ]);

  async function loadData() {
    try {
      const deptOverview = await getDeptOverview();
      overviewCards[0].value = deptOverview.total_dept || 0;
      overviewCards[1].value = deptOverview.active_dept || 0;
      overviewCards[2].value = deptOverview.total_user || 0;

      const roleOverview = await getRoleOverview();
      overviewCards[3].value = roleOverview.total_role || 0;

      const deptDist = await getDeptDistribution();
      deptData.value = deptDist || [];

      const roleDist = await getRoleDistribution();
      roleData.value = roleDist || [];
    } catch (error) {
      message.error('加载数据失败');
    }
  }

  async function handleExportDept() {
    try {
      const response = await exportDept();
      downloadFile(response, `部门统计_${new Date().toLocaleDateString()}.xlsx`);
      message.success('导出成功');
    } catch (error) {
      message.error('导出失败');
    }
  }

  async function handleExportRole() {
    try {
      const response = await exportRole();
      downloadFile(response, `角色统计_${new Date().toLocaleDateString()}.xlsx`);
      message.success('导出成功');
    } catch (error) {
      message.error('导出失败');
    }
  }

  function downloadFile(response: any, filename: string) {
    const blob = new Blob([response.data], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    window.URL.revokeObjectURL(url);
  }

  onMounted(() => {
    loadData();
  });
</script>

<style lang="less" scoped>
  .enter-y {
    transition: all 0.3s ease;
    &:hover {
      transform: translateY(-2px);
    }
  }
</style>
