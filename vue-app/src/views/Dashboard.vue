<template>
  <div class="dashboard">
    <main class="main-content">
      <div class="dashboard-grid">
        <div class="card glass map-card">
          <div class="card-header">
            <h3 class="card-title">工厂平面图</h3>
            <span class="card-meta">{{ mapMeta }}</span>
          </div>
          <div ref="mapChart" class="map-container"></div>
          <div class="map-legend">
            <span class="legend-item"><span class="legend-dot normal"></span>正常</span>
            <span class="legend-item"><span class="legend-dot alarm"></span>报警</span>
            <span class="legend-item"><span class="legend-dot offline"></span>离线</span>
          </div>
        </div>

        <div class="card glass chart-card">
          <div class="card-header">
            <h3 class="card-title">报警次数趋势</h3>
            <span class="card-tag">24小时</span>
          </div>
          <LineChart :series="chartSeries" :labels="chartLabels" :height="'200px'" />
        </div>

        <div class="kpi-section">
          <div class="card glass kpi-card">
            <span class="kpi-label">设备总数</span>
            <span class="kpi-value kpi-total">{{ totalDevices }}</span>
          </div>
          <div class="card glass kpi-card">
            <span class="kpi-label">在线设备</span>
            <span class="kpi-value kpi-online">{{ onlineDevices }}</span>
          </div>
          <div class="card glass kpi-card">
            <span class="kpi-label">当前报警</span>
            <span class="kpi-value kpi-alarm">{{ alarmDevices }}</span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import * as echarts from 'echarts'
import { io } from 'socket.io-client'
import api from '../lib/api'
import { getAuthToken } from '../lib/auth'
import LineChart from '../components/LineChart.vue'

const mapChart = ref(null)
const devices = ref([])
const mapMeta = ref('数据加载中...')

const totalDevices = computed(() => devices.value.length)
const onlineDevices = computed(() => devices.value.filter(d => d.online_status === 1).length)
const alarmDevices = computed(() => devices.value.filter(d => d.online_status === 1 && d.alarm_status === 1).length)

const chartLabels = Array.from({ length: 24 }, (_, i) => `${i}:00`)
const chartSeries = ref([])

let mapChartInstance = null

const C = {
  text: '#5c5678',
  textSec: '#9890b0',
  purple: '#b8a9e8',
  green: '#D0F578',
  red: '#f0a0a0',
  offline: '#b0a8c8',
}

function generateAlarmData() {
  const today = []
  const yesterday = []
  for (let i = 0; i < 24; i++) {
    today.push(Math.floor(Math.random() * 10))
    yesterday.push(Math.floor(Math.random() * 8))
  }
  chartSeries.value = [
    {
      name: '今日',
      data: today,
      color: C.purple,
      areaColor: ['rgba(184,169,232,0.18)', 'rgba(184,169,232,0.02)'],
      lineWidth: 3,
    },
    {
      name: '昨日',
      data: yesterday,
      color: C.green,
      areaColor: ['rgba(208,245,120,0.16)', 'rgba(208,245,120,0.02)'],
      lineWidth: 3,
    },
  ]
}

function updateMap() {
  if (!mapChartInstance) return

  const data = devices.value.map(dev => {
    let color = C.offline
    let statusText = '离线'
    if (dev.online_status === 1) {
      if (dev.alarm_status === 1) {
        color = C.red
        statusText = '报警'
      } else {
        color = C.green
        statusText = '正常'
      }
    }
    return {
      name: dev.device_id,
      value: [dev.pos_x || 0, dev.pos_y || 0],
      itemStyle: { color },
      statusText,
      lastSeen: dev.last_seen || '-',
    }
  })

  mapChartInstance.setOption({ series: [{ data }] })
  const now = new Date().toLocaleTimeString('zh-CN', { hour12: false })
  mapMeta.value = `最近更新 ${now}`
}

async function initData() {
  try {
    const res = await api.get('/api/devices')
    devices.value = res.data.devices || []
    updateMap()
  } catch (e) {
    console.error('初始化数据失败:', e)
  }
}

let socket = null

onMounted(() => {
  mapChartInstance = echarts.init(mapChart.value)
  mapChartInstance.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255,255,255,0.85)',
      borderColor: 'rgba(255,255,255,0.3)',
      borderWidth: 1,
      textStyle: { color: C.text, fontSize: 12 },
      formatter: p => `<strong>${p.data.name}</strong><br/>状态: ${p.data.statusText}<br/>最后更新: ${p.data.lastSeen}`,
    },
    xAxis: { min: 0, max: 1920, show: false },
    yAxis: { min: 0, max: 1080, inverse: true, show: false },
    graphic: [{
      type: 'image',
      id: 'background',
      left: 0,
      top: 0,
      style: {
        image: '/Dashboard.png',
        width: 1920,
        height: 1080,
        opacity: 0.45,
      },
    }],
    series: [{
      type: 'scatter',
      symbolSize: 32,
      data: [],
    }],
  })

  generateAlarmData()
  initData()

  socket = io({ auth: { token: getAuthToken() } })
  socket.on('position_update', data => {
    devices.value = data || []
    updateMap()
  })

  const resizeHandler = () => {
    mapChartInstance?.resize()
  }
  window.addEventListener('resize', resizeHandler)

  onUnmounted(() => {
    window.removeEventListener('resize', resizeHandler)
    mapChartInstance?.dispose()
    socket?.disconnect()
  })
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  position: relative;
}

.main-content {
  padding: 28px 32px;
  overflow-y: auto;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 260px;
  grid-template-rows: auto auto;
  gap: 24px;
  grid-template-areas:
    "map kpi"
    "chart kpi";
  animation: grid-reveal 0.8s cubic-bezier(0.4, 0, 0.2, 1) both;
}

@keyframes grid-reveal {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

.glass {
  background: rgba(255, 255, 255, 0.18);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow:
    0 8px 32px rgba(140, 120, 180, 0.10),
    inset 0 1px 0 rgba(255, 255, 255, 0.35);
  transition: box-shadow 0.4s cubic-bezier(0.4, 0, 0.2, 1), transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.card {
  border-radius: 24px;
  padding: 24px;
}

.card:hover {
  box-shadow:
    0 16px 48px rgba(140, 120, 180, 0.18),
    inset 0 1px 0 rgba(255, 255, 255, 0.4);
  transform: translateY(-3px);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.card-title {
  font-family: 'Outfit', sans-serif;
  font-size: 16px;
  font-weight: 600;
  color: #3a3550;
  letter-spacing: 0.01em;
}

.card-meta {
  font-size: 11px;
  color: #8a8aa8;
  background: rgba(255, 255, 255, 0.25);
  padding: 5px 12px;
  border-radius: 999px;
  backdrop-filter: blur(4px);
}

.card-tag {
  font-size: 11px;
  color: #8a8aa8;
  background: rgba(255, 255, 255, 0.25);
  padding: 5px 12px;
  border-radius: 999px;
  backdrop-filter: blur(4px);
}

.map-card {
  grid-area: map;
}

.map-container {
  width: 100%;
  height: 420px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.08);
  box-shadow: inset 0 2px 8px rgba(140, 120, 180, 0.06);
  overflow: hidden;
}

.map-legend {
  display: flex;
  justify-content: center;
  gap: 28px;
  margin-top: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #8a8aa8;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  box-shadow: 0 0 6px currentColor;
}

.legend-dot.normal { background: #a8e6cf; color: #a8e6cf; }
.legend-dot.alarm { background: #f0a0a0; color: #f0a0a0; }
.legend-dot.offline { background: #b0a8c8; color: #b0a8c8; }

.chart-card {
  grid-area: chart;
}

.kpi-section {
  grid-area: kpi;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.kpi-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 28px 20px;
  text-align: center;
  cursor: default;
  transition: box-shadow 0.4s cubic-bezier(0.4, 0, 0.2, 1), transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.kpi-card:hover {
  transform: translateY(-2px) scale(1.02);
}

.kpi-label {
  font-family: 'Outfit', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #8a8aa8;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.kpi-value {
  font-family: 'Outfit', sans-serif;
  font-size: 48px;
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.03em;
}

.kpi-total {
  color: #b8a9e8;
  text-shadow: 0 0 20px rgba(184, 169, 232, 0.3);
}

.kpi-online {
  color: #a8e6cf;
  text-shadow: 0 0 20px rgba(168, 230, 207, 0.3);
}

.kpi-alarm {
  color: #f0a0a0;
  text-shadow: 0 0 20px rgba(240, 160, 160, 0.3);
  animation: alarmPulse 2.5s ease-in-out infinite;
}

@keyframes alarmPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.03); }
}

@media (max-width: 1200px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
    grid-template-areas:
      "map"
      "chart"
      "kpi";
  }

  .kpi-section {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .kpi-card {
    flex: 1;
    min-width: 160px;
  }

  .map-container { height: 360px; }
}

@media (max-width: 768px) {
  .main-content {
    padding: 16px;
  }

  .kpi-section {
    flex-direction: column;
  }

  .map-container { height: 280px; }
}
</style>
