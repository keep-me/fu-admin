<template>
  <div ref="chartRef" :style="{ height, width }"></div>
</template>
<script lang="ts" setup>
  import { onMounted, ref, Ref, watch } from 'vue';
  import { useECharts } from '/@/hooks/web/useECharts';
  import { basicProps } from './props';
  import type { DistributionItem } from './props';

  const props = defineProps({
    ...basicProps,
    data: {
      type: Array as PropType<DistributionItem[]>,
      default: () => [],
    },
    title: {
      type: String,
      default: '模块分布',
    },
  });

  const chartRef = ref<HTMLDivElement | null>(null);
  const { setOptions, echarts } = useECharts(chartRef as Ref<HTMLDivElement>);

  watch(
    () => props.data,
    (newData) => {
      if (newData && newData.length > 0) {
        updateChart(newData);
      }
    },
    { deep: true }
  );

  function updateChart(data: DistributionItem[]) {
    const xAxisData = data.map((item) => item.name);
    const seriesData = data.map((item) => item.value);

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
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        data: xAxisData,
        axisLabel: {
          rotate: 45,
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
          name: '操作次数',
          type: 'bar',
          barWidth: '60%',
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#5ab1ef' },
              { offset: 1, color: '#019680' },
            ]),
            borderRadius: [4, 4, 0, 0],
          },
          data: seriesData,
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
