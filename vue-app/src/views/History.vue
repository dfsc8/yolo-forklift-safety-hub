<template>
  <div class="history-page">
    <main class="main-content-inner">

      <!-- Header -->
      <div class="card glass trend-card">
        <div class="card-header">
          <h3 class="card-title">报警历史</h3>
          <span class="card-meta">历史记录</span>
        </div>

        <!-- 控制区：分页/刷新 -->
        <div class="controls">
          <button @click="fetchHistory">刷新</button>
        </div>

        <!-- 历史表格 -->
        <table class="history-table">
          <thead>
            <tr>
              <th>时间</th>
              <th>设备</th>
              <th>报警类型</th>
              <th>状态</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in historyData" :key="item.id">
              <td>{{ item.time }}</td>
              <td>{{ item.device }}</td>
              <td>{{ item.type }}</td>
              <td>{{ item.status }}</td>
            </tr>
          </tbody>
        </table>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../lib/api'

const historyData = ref([])

async function fetchHistory() {
  try {
    const res = await api.get('/api/history') // 后端接口
    historyData.value = res.data || []
  } catch (e) {
    console.error('历史数据加载失败', e)
  }
}

onMounted(fetchHistory)
</script>

<style scoped>
.main-content-inner {
  padding: 28px 32px;
}

.card.trend-card {
  padding: 20px;
  animation: fade-in 0.6s ease;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.controls {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 16px;
}

.controls button {
  padding: 6px 12px;
  border-radius: 10px;
  border: none;
  background: rgba(184,169,232,0.2);
  cursor: pointer;
  transition: all 0.2s;
}

.controls button:hover {
  background: rgba(184,169,232,0.35);
}

.history-table {
  width: 100%;
  border-collapse: collapse;
}

.history-table th,
.history-table td {
  padding: 8px 12px;
  border-bottom: 1px solid rgba(184,169,232,0.2);
  color: #000;
}

.history-table th {
  font-weight: bold;
  text-align: left;
}
</style>
