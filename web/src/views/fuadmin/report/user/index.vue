<template>
  <div class="p-4">
    <Row :gutter="[16, 16]">
      <Col :span="6" v-for="(card, index) in overviewCards" :key="index">
        <Card hoverable>
          <Statistic
            :title="card.title"
            :value="card.value"
            :prefix="card.prefix"
            :value-style="{ color: card.color }"
          />
        </Card>
      </Col>
    </Row>

    <div class="mt-4">
      <Card title="用户增长趋势" class="enter-y">
        <template #extra>
          <Select v-model:value="days" style="width: 120px" @change="loadData">
            <SelectOption :value="7">最近7天</SelectOption>
            <SelectOption :value="30">最近30天</SelectOption>
            <SelectOption :value="90">最近90天</SelectOption>
          </Select>
          <Button type="primary" style="margin-left: 10px" @click="handleExportTrend">
            <DownloadOutlined />
            导出
          </Button>
        </template>
        <UserTrendChart :data="userTrendData" height="350px" title="" />
      </Card>
    </div>

    <Row :gutter="[16, 16]" class="mt-4">
      <Col :span="12">
        <Card title="性别分布" class="enter-y">
          <template #extra>
            <Button type="primary" @click="handleExportDistribution">
              <DownloadOutlined />
              导出
            </Button>
          </template>
          <UserDistributionChart :data="genderData" height="300px" title="" />
        </Card>
      </Col>
      <Col :span="12">
        <Card title="状态分布" class="enter-y">
          <UserDistributionChart :data="statusData" height="300px" title="" />
        </Card>
      </Col>
    </Row>
  </div>
</template>

<script lang="ts" setup>
  import { ref, reactive, onMounted } from 'vue';
  import { Row, Col, Card, Statistic, Select, Button, message } from 'ant-design-vue';
  import { DownloadOutlined } from '@ant-design/icons-vue';
  import UserTrendChart from '../components/UserTrendChart.vue';
  import UserDistributionChart from '../components/UserDistributionChart.vue';
  import {
    getUserOverview,
    getUserTrend,
    getUserDistributionGender,
    getUserDistributionStatus,
    exportUserTrend,
    exportUserDistribution,
  } from '../report.api';
  import type { TrendDataItem, DistributionItem } from '../components/props';

  const days = ref(30);
  const userTrendData = ref<TrendDataItem[]>([]);
  const genderData = ref<DistributionItem[]>([]);
  const statusData = ref<DistributionItem[]>([]);

  const overviewCards = reactive([
    { title: '总用户数', value: 0, color: '#1890ff', prefix: '' },
    { title: '活跃用户', value: 0, color: '#52c41a', prefix: '' },
    { title: '非活跃用户', value: 0, color: '#ff4d4f', prefix: '' },
  ]);

  async function loadData() {
    try {
      const overview = await getUserOverview();
      overviewCards[0].value = overview.total_count || 0;
      overviewCards[1].value = overview.active_count || 0;
      overviewCards[2].value = overview.inactive_count || 0;

      const trendData = await getUserTrend(days.value);
      userTrendData.value = trendData || [];

      const gender = await getUserDistributionGender();
      genderData.value = gender || [];

      const status = await getUserDistributionStatus();
      statusData.value = status || [];
    } catch (error) {
      message.error('加载数据失败');
    }
  }

  async function handleExportTrend() {
    try {
      const response = await exportUserTrend(days.value);
      downloadFile(response, `用户增长趋势_${new Date().toLocaleDateString()}.xlsx`);
      message.success('导出成功');
    } catch (error) {
      message.error('导出失败');
    }
  }

  async function handleExportDistribution() {
    try {
      const response = await exportUserDistribution();
      downloadFile(response, `用户分布统计_${new Date().toLocaleDateString()}.xlsx`);
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
