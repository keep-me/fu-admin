<template>
  <div ref="chartRef" :style="{ height, width }"></div>
</template>
<script lang="ts" setup>
  import { onMounted, ref, Ref, watch } from 'vue';
  import { useECharts } from '/@/hooks/web/useECharts';
  import { basicProps } from './props';
  import type { LogTrendDataItem } from './props';

  const props = defineProps({
    ...basicProps,
    data: {
      type: Array as PropType<LogTrendDataItem[]>,
      default: () => [],
    },
    title: {
      type: String,
      default: '操作日志趋势',
    },
  });

  const chartRef = ref<HTMLDivElement | null>(null);
  const { setOptions } = useECharts(chartRef as Ref<HTMLDivElement>);

  watch(
    () => props.data,
    (newData) => {
      if (newData && newData.length > 0) {
        updateChart(newData);
      }
    },
    { deep: true }
  );

  function updateChart(data: LogTrendDataItem[]) {
    const xAxisData = data.map((item) => item.date);
    const successData = data.map((item) => item.success_count);
    const failData = data.map((item) => item.fail_count);

    setOptions({
      title: {
        text: props.title,
        left: 'center',
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold',
        },
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow',
        },
      },
      legend: {
        data: ['成功', '失败'],
        top: 30,
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        top: 80,
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        data: xAxisData,
        axisLabel: {
          rotate: 45,
          interval: Math.floor(xAxisData.length / 7) || 0,
        },
      },
      yAxis: {
        type: 'value',
        splitLine: {
          lineStyle: {
            type: 'dashed',
          },
        },
      },
      series: [
        {
          name: '成功',
          type: 'bar',
          stack: 'total',
          barWidth: '40%',
          itemStyle: {
            color: '#67C23A',
          },
          data: successData,
        },
        {
          name: '失败',
          type: 'bar',
          stack: 'total',
          barWidth: '40%',
          itemStyle: {
            color: '#F56C6C',
          },
          data: failData,
        },
      ],
    });
  }

  onMounted(() => {
    if (props.data && props.data.length > 0) {
      updateChart(props.data);
    }
  });
</script>
