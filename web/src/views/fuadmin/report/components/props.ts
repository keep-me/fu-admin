import { PropType } from 'vue';

export interface BasicProps {
  width: string;
  height: string;
}

export const basicProps = {
  width: {
    type: String as PropType<string>,
    default: '100%',
  },
  height: {
    type: String as PropType<string>,
    default: '280px',
  },
};

export interface TrendDataItem {
  date: string;
  count: number;
}

export interface DistributionItem {
  name: string;
  value: number;
}

export interface LogTrendDataItem {
  date: string;
  success_count: number;
  fail_count: number;
}

export interface DeptDistributionItem {
  name: string;
  user_count: number;
}

export interface RoleDistributionItem {
  name: string;
  user_count: number;
}
