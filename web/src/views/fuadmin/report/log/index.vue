<template>
  <div class="p-4">
    <Row :gutter="[16, 16]">
      <Col :span="6" v-for="(card, index) in overviewCards" :key="index">
        <Card hoverable>
          <Statistic
            :title="card.title"
            :value="card.value"
            :value-style="{ color: card.color }"
          >
            <template #suffix>
              <span v-if="card.suffix">{{ card.suffix }}</span>
            </template>
          </Statistic>
        </Card>
      </Col>
    </Row>

    <div class="mt-4">
      <Card title="操作日志趋势" class="enter-y">
        <template #extra>
          <Select v-model:value="days" style="width: 120px" @change="loadData">
            <SelectOption :value="7">最近7天</SelectOption>
            <SelectOption :value="30">最近30天</SelectOption>
            <SelectOption :value="90">最近90天</SelectOption>
          </Select>
          <Button type="primary" style="margin-left: 10px" @click="handleExportOperation">
            <DownloadOutlined />
            导出操作日志
          </Button>
        </template>
        <LogTrendChart :data="operationTrendData" height="350px" title="" />
      </Card>
    </div>

    <Row :gutter="[16, 16]" class="mt-4">
      <Col :span="12">
        <Card title="登录日志趋势" class="enter-y">
          <template #extra>
            <Button type="primary" @click="handleExportLogin">
              <DownloadOutlined />
              导出登录日志
            </Button>
          </template>
          <UserTrendChart :data="loginTrendData" height="300px" title="" />
        </Card>
      </Col>
      <Col :span="12">
        <Card title="操作模块分布" class="enter-y">
          <ModuleChart :data="moduleData" height="300px" title="" />
        </Card>
      </Col>
    </Row>
  </div>
</template>

<script lang="ts" setup>
  import { ref, reactive, onMounted } from 'vue';
  import { Row, Col, Card, Statistic, Select, Button, message } from 'ant-design-vue';
  import { DownloadOutlined } from '@ant-design/icons-vue';
  import LogTrendChart from '../components/LogTrendChart.vue';
  import UserTrendChart from '../components/UserTrendChart.vue';
  import ModuleChart from '../components/ModuleChart.vue';
  import {
    getLogOverview,
    getLogOperationTrend,
    getLogLoginTrend,
    getLogOperationModules,
    exportLogOperation,
    exportLogLogin,
  } from '../report.api';
  import type { LogTrendDataItem, TrendDataItem, DistributionItem } from '../components/props';

  const days = ref(30);
  const operationTrendData = ref<LogTrendDataItem[]>([]);
  const loginTrendData = ref<TrendDataItem[]>([]);
  const moduleData = ref<DistributionItem[]>([]);

  const overviewCards = reactive([
    { title: '操作次数', value: 0, color: '#1890ff', suffix: '' },
    { title: '登录次数', value: 0, color: '#52c41a', suffix: '' },
    { title: '成功次数', value: 0, color: '#1890ff', suffix: '' },
    { title: '失败次数', value: 0, color: '#ff4d4f', suffix: '' },
  ]);

  async function loadData() {
    try {
      const overview = await getLogOverview(days.value);
      overviewCards[0].value = overview.operation_count || 0;
      overviewCards[1].value = overview.login_count || 0;
      overviewCards[2].value = overview.success_count || 0;
      overviewCards[3].value = overview.fail_count || 0;

      const operationTrend = await getLogOperationTrend(days.value);
      operationTrendData.value = operationTrend || [];

      const loginTrend = await getLogLoginTrend(days.value);
      loginTrendData.value = loginTrend || [];

      const modules = await getLogOperationModules(days.value);
      moduleData.value = modules || [];
    } catch (error) {
      message.error('加载数据失败');
    }
  }

  async function handleExportOperation() {
    try {
      const response = await exportLogOperation(days.value);
      downloadFile(response, `操作日志趋势_${new Date().toLocaleDateString()}.xlsx`);
      message.success('导出成功');
    } catch (error) {
      message.error('导出失败');
    }
  }

  async function handleExportLogin() {
    try {
      const response = await exportLogLogin(days.value);
      downloadFile(response, `登录日志趋势_${new Date().toLocaleDateString()}.xlsx`);
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
