import { defHttp } from '/@/utils/http/axios';

enum Api {
  UserOverview = '/api/system/report/user/overview',
  UserTrend = '/api/system/report/user/trend',
  UserDistributionGender = '/api/system/report/user/distribution/gender',
  UserDistributionStatus = '/api/system/report/user/distribution/status',
  UserDistributionType = '/api/system/report/user/distribution/type',
  LogOverview = '/api/system/report/log/overview',
  LogOperationTrend = '/api/system/report/log/operation/trend',
  LogLoginTrend = '/api/system/report/log/login/trend',
  LogOperationModules = '/api/system/report/log/operation/modules',
  DeptOverview = '/api/system/report/dept/overview',
  DeptDistribution = '/api/system/report/dept/distribution',
  RoleOverview = '/api/system/report/role/overview',
  RoleDistribution = '/api/system/report/role/distribution',
  ExportUserTrend = '/api/system/export/user/trend/excel',
  ExportUserDistribution = '/api/system/export/user/distribution/excel',
  ExportLogOperation = '/api/system/export/log/operation/excel',
  ExportLogLogin = '/api/system/export/log/login/excel',
  ExportDept = '/api/system/export/dept/excel',
  ExportRole = '/api/system/export/role/excel',
}

export function getUserOverview() {
  return defHttp.get({ url: Api.UserOverview });
}

export function getUserTrend(days: number = 30) {
  return defHttp.get({ url: Api.UserTrend, params: { days } });
}

export function getUserDistributionGender() {
  return defHttp.get({ url: Api.UserDistributionGender });
}

export function getUserDistributionStatus() {
  return defHttp.get({ url: Api.UserDistributionStatus });
}

export function getUserDistributionType() {
  return defHttp.get({ url: Api.UserDistributionType });
}

export function getLogOverview(days: number = 30) {
  return defHttp.get({ url: Api.LogOverview, params: { days } });
}

export function getLogOperationTrend(days: number = 30) {
  return defHttp.get({ url: Api.LogOperationTrend, params: { days } });
}

export function getLogLoginTrend(days: number = 30) {
  return defHttp.get({ url: Api.LogLoginTrend, params: { days } });
}

export function getLogOperationModules(days: number = 30) {
  return defHttp.get({ url: Api.LogOperationModules, params: { days } });
}

export function getDeptOverview() {
  return defHttp.get({ url: Api.DeptOverview });
}

export function getDeptDistribution() {
  return defHttp.get({ url: Api.DeptDistribution });
}

export function getRoleOverview() {
  return defHttp.get({ url: Api.RoleOverview });
}

export function getRoleDistribution() {
  return defHttp.get({ url: Api.RoleDistribution });
}

export function exportUserTrend(days: number = 30) {
  return defHttp.get({ url: Api.ExportUserTrend, params: { days }, { isReturnNativeResponse: true });
}

export function exportUserDistribution() {
  return defHttp.get({ url: Api.ExportUserDistribution, {}, { isReturnNativeResponse: true });
}

export function exportLogOperation(days: number = 30) {
  return defHttp.get({ url: Api.ExportLogOperation, params: { days }, { isReturnNativeResponse: true });
}

export function exportLogLogin(days: number = 30) {
  return defHttp.get({ url: Api.ExportLogLogin, params: { days }, { isReturnNativeResponse: true });
}

export function exportDept() {
  return defHttp.get({ url: Api.ExportDept, {}, { isReturnNativeResponse: true });
}

export function exportRole() {
  return defHttp.get({ url: Api.ExportRole, {}, { isReturnNativeResponse: true });
}
