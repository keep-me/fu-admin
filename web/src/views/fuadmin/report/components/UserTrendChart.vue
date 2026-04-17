<template>
  <div ref="chartRef" :style="{ height, width }"></div>
</template>
<script lang="ts" setup>
  import { onMounted, ref, Ref, watch } from 'vue';
  import { useECharts } from '/@/hooks/web/useECharts';
  import { basicProps } from './props';
  import type { TrendDataItem } from './props';

  const props = defineProps({
    ...basicProps,
    data: {
      type: Array as PropType<TrendDataItem[]>,
      default: () => [],
    },
    title: {
      type: String,
      default: '用户增长趋势',
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

  function updateChart(data: TrendDataItem[]) {
    const xAxisData = data.map((item) => item.date);
    const seriesData = data.map((item) => item.count);

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
          lineStyle: {
            width: 1,
            color: '#019680',
          },
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
        boundaryGap: false,
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
          name: '新增用户',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 6,
          lineStyle: {
            color: '#5ab1ef',
            width: 2,
          },
          itemStyle: {
            color: '#5ab1ef',
          },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                {
                  offset: 0,
                  color: 'rgba(90, 177, 239, 0.4)',
                },
                {
                  offset: 1,
                  color: 'rgba(90, 177, 239, 0.01)',
                },
              ],
            },
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
