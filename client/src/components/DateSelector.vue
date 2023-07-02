<template>

    <div class="block">
      <span class="demonstration">选择日期</span>
      <el-date-picker
        v-model="selectedDate"
        type="datetimerange"
        :shortcuts="shortcuts"
        range-separator="到"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        @change="handleDateChange"
      ></el-date-picker>
    </div>
  </template>

<script>
import { ref, onMounted } from 'vue';

export default {
  setup(_, { emit }) {
    const selectedDate = ref([new Date(2022, 10, 10, 10, 10), new Date(2023, 11, 11, 10, 10)]);

    const handleDateChange = (value) => {
      emit('date-selected', value);
    };
      const shortcuts = [
        {
          text: 'Last week',
          value: () => {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
            return [start, end];
          },
        },
        {
          text: 'Last month',
          value: () => {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
            return [start, end];
          },
        },
        {
          text: 'Last 3 months',
          value: () => {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
            return [start, end];
          },
        },
      ];
      onMounted(() => {
      handleDateChange(selectedDate.value);
    });
      return {
        selectedDate,
        // value2,
        handleDateChange,
        shortcuts,
      };
    },
  };
  </script>
  
  <style scoped>
  .block {
    padding: 30px 0;
    text-align: center;
    border-right: solid 1px var(--el-border-color);
    flex: 1;
  }
  .block:last-child {
    border-right: none;
  }
  .block .demonstration {
    display: block;
    color: var(--el-text-color-secondary);
    font-size: 14px;
    margin-bottom: 20px;
  }
  </style>
  