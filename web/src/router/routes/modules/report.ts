import type { AppRouteModule } from '/@/router/types';
import { LAYOUT } from '/@/router/constant';

const report: AppRouteModule = {
  path: '/report',
  name: 'Report',
  component: LAYOUT,
  redirect: '/report/user',
  meta: {
    orderNo: 50,
    icon: 'ant-design:bar-chart-outlined',
    title: '数据报表',
  },
  children: [
    {
      path: 'user',
      name: 'ReportUser',
      component: () => import('/@/views/fuadmin/report/user/index.vue'),
      meta: {
        title: '用户统计',
        icon: 'ant-design:user-outlined',
      },
    },
    {
      path: 'log',
      name: 'ReportLog',
      component: () => import('/@/views/fuadmin/report/log/index.vue'),
      meta: {
        title: '操作日志统计',
        icon: 'ant-design:file-text-outlined',
      },
    },
    {
      path: 'org',
      name: 'ReportOrg',
      component: () => import('/@/views/fuadmin/report/org/index.vue'),
      meta: {
        title: '部门/角色统计',
        icon: 'ant-design:apartment-outlined',
      },
    },
    {
      path: 'manage',
      name: 'ReportManage',
      component: () => import('/@/views/fuadmin/report/manage/index.vue'),
      meta: {
        title: '报表管理',
        icon: 'ant-design:setting-outlined',
      },
    },
  ],
};

export default report;
