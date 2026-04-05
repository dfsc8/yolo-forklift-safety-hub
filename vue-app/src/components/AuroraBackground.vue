<template>
  <div class="aurora-canvas">
    <div class="aurora-bands">
      <div class="aurora-band band-1"></div>
      <div class="aurora-band band-2"></div>
      <div class="aurora-band band-3"></div>
      <div class="aurora-band band-4"></div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.aurora-canvas {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}

.aurora-bands {
  position: absolute;
  inset: 0;
}

.aurora-band {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
}

.band-1 {
  width: 900px;
  height: 600px;
  top: -15%;
  left: -10%;
  background: radial-gradient(circle, rgba(30, 58, 138, 0.55), transparent 70%);
}

.band-2 {
  width: 1000px;
  height: 700px;
  top: 5%;
  right: -20%;
  background: radial-gradient(circle, rgba(88, 28, 135, 0.45), transparent 70%);
}

.band-3 {
  width: 700px;
  height: 500px;
  bottom: -20%;
  left: 10%;
  background: radial-gradient(circle, rgba(37, 99, 235, 0.5), transparent 70%);
}

.band-4 {
  width: 600px;
  height: 450px;
  top: 40%;
  left: 40%;
  background: radial-gradient(circle, rgba(126, 34, 206, 0.4), transparent 70%);
}
</style>
