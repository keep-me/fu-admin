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
      default: '用户分布',
    },
  });

  const chartRef = ref<HTMLDivElement | null>(null);
  const { setOptions } = useECharts(chartRef as Ref<HTMLDivElement>);

  const colors = ['#5ab1ef', '#019680', '#67C23A', '#E6A23C', '#F56C6C', '#909399'];

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
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)',
      },
      legend: {
        orient: 'vertical',
        left: 'left',
        top: 'middle',
      },
      color: colors,
      series: [
        {
          name: props.title,
          type: 'pie',
          radius: ['40%', '70%'],
          center: ['60%', '50%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2,
          },
          label: {
            show: true,
            formatter: '{b}: {d}%',
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 14,
              fontWeight: 'bold',
            },
          },
          labelLine: {
            show: true,
          },
          data: data,
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
