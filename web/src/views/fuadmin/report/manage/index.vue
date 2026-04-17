<template>
  <div class="p-4">
    <Card title="报表定时任务管理" class="enter-y">
      <Alert
        message="定时任务说明"
        description="通过配置定时任务，可以定期自动生成数据报表。以下是可用的报表生成任务，您可以在系统定时任务页面配置执行周期。"
        type="info"
        show-icon
        style="margin-bottom: 20px"
      />

      <Row :gutter="[16, 16]" class="mb-4">
        <Col :span="8">
          <Card hoverable>
            <template #title>
              <div class="task-title">
                <UserOutlined class="task-icon" style="color: #1890ff" />
                <span>用户统计报表</span>
              </div>
            </template>
            <p style="color: #666; margin-bottom: 16px">
              任务名称: system.tasks.generate_user_report
            </p>
            <p style="color: #666; margin-bottom: 16px">
              功能说明: 自动生成用户增长趋势和用户分布统计报表
            </p>
            <Space>
              <Button type="primary" @click="execTask('system.tasks.generate_user_report')">
                立即执行
              </Button>
            </Space>
          </Card>
        </Col>

        <Col :span="8">
          <Card hoverable>
            <template #title>
              <div class="task-title">
                <FileTextOutlined class="task-icon" style="color: #52c41a" />
                <span>日志统计报表</span>
              </div>
            </template>
            <p style="color: #666; margin-bottom: 16px">
              任务名称: system.tasks.generate_log_report
            </p>
            <p style="color: #666; margin-bottom: 16px">
              功能说明: 自动生成操作日志和登录日志统计报表
            </p>
            <Space>
              <Button type="primary" @click="execTask('system.tasks.generate_log_report')">
                立即执行
              </Button>
            </Space>
          </Card>
        </Col>

        <Col :span="8">
          <Card hoverable>
            <template #title>
              <div class="task-title">
                <ApartmentOutlined class="task-icon" style="color: #E6A23C" />
                <span>组织统计报表</span>
              </div>
            </template>
            <p style="color: #666; margin-bottom: 16px">
              任务名称: system.tasks.generate_org_report
            </p>
            <p style="color: #666; margin-bottom: 16px">
              功能说明: 自动生成部门和角色统计报表
            </p>
            <Space>
              <Button type="primary" @click="execTask('system.tasks.generate_org_report')">
                立即执行
              </Button>
            </Space>
          </Card>
        </Col>
      </Row>

      <Divider />

      <div style="margin-top: 20px">
        <h3 style="margin-bottom: 16px">配置定时任务</h3>
        <Alert
          message="如何配置定时任务"
          type="info"
          show-icon
        >
          <template #description>
            <ol style="padding-left: 20px; margin: 0">
              <li>进入「系统管理」→「定时任务」页面</li>
              <li>创建新的定时任务，选择需要执行的任务名称</li>
              <li>配置执行频率（Cron表达式或间隔时间）</li>
              <li>启用任务后，系统将自动按照设定的时间生成报表</li>
              <li>生成的报表将保存在服务器 reports 目录下</li>
            </ol>
          </template>
        </Alert>
      </div>
    </Card>

    <Card title="报表统计总览" class="mt-4 enter-y">
      <Row :gutter="[16, 16]">
        <Col :span="6">
          <Card hoverable>
            <Statistic title="用户统计报表" value="可用">
              <template #prefix>
                <CheckCircleOutlined style="color: #52c41a" />
              </template>
            </Statistic>
          </Card>
        </Col>
        <Col :span="6">
          <Card hoverable>
            <Statistic title="日志统计报表" value="可用">
              <template #prefix>
                <CheckCircleOutlined style="color: #52c41a" />
              </template>
            </Statistic>
          </Card>
        </Col>
        <Col :span="6">
          <Card hoverable>
            <Statistic title="组织统计报表" value="可用">
              <template #prefix>
                <CheckCircleOutlined style="color: #52c41a" />
              </template>
            </Statistic>
          </Card>
        </Col>
        <Col :span="6">
          <Card hoverable>
            <Statistic title="数据导出功能" value="支持Excel">
              <template #prefix>
                <CheckCircleOutlined style="color: #52c41a" />
              </template>
            </Statistic>
          </Card>
        </Col>
      </Row>
    </Card>
  </div>
</template>

<script lang="ts" setup>
  import { message, Card, Row, Col, Statistic, Alert, Button, Space, Divider } from 'ant-design-vue';
  import {
    UserOutlined,
    FileTextOutlined,
    ApartmentOutlined,
    CheckCircleOutlined,
  } from '@ant-design/icons-vue';
  import { defHttp } from '/@/utils/http/axios';

  async function execTask(taskName: string) {
    try {
      await defHttp.post({
        url: '/api/system/periodic_task/immediate/exec',
        params: { task: taskName },
      });
      message.success('任务已提交执行，请稍候查看生成的报表');
    } catch (error) {
      message.error('任务执行失败，请确保Celery服务已启动');
    }
  }
</script>

<style lang="less" scoped>
  .enter-y {
    transition: all 0.3s ease;
    &:hover {
      transform: translateY(-2px);
    }
  }

  .task-title {
    display: flex;
    align-items: center;
  }

  .task-icon {
    font-size: 20px;
    margin-right: 8px;
  }

  .mt-4 {
    margin-top: 16px;
  }

  .mb-4 {
    margin-bottom: 16px;
  }
</style>
