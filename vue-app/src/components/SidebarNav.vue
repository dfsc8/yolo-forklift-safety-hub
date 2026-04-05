<template>
  <nav class="sidebar glass">
    <div class="sidebar-brand">
      <img src="/logo.png" alt="智盾" class="brand-logo" />
      <span class="brand-name">智盾</span>
    </div>
    <div class="sidebar-menu">
      <router-link to="/" class="menu-item" active-class="active">
        <span class="menu-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
          </svg>
        </span>
        <span>仪表盘</span>
      </router-link>
      <router-link to="/devices" class="menu-item" active-class="active">
        <span class="menu-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z"/>
            <path d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0"/>
          </svg>
        </span>
        <span>设备列表</span>
      </router-link>
      <router-link to="/logs" class="menu-item" active-class="active">
        <span class="menu-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
        </span>
        <span>业务日志</span>
      </router-link>
    </div>
  </nav>
</template>

<script setup>
</script>

<style scoped>
.sidebar {
  width: 220px;
  flex-shrink: 0;
  padding: 28px 0 24px;
  display: flex;
  flex-direction: column;
  border-radius: 0 24px 24px 0;
  position: relative;
  z-index: 1;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: none;
  border-right: 1px solid rgba(255, 255, 255, 0.25);
  box-shadow:
    0 8px 32px rgba(140, 120, 180, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 24px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  margin-bottom: 8px;
}

.brand-logo {
  width: 36px;
  height: 36px;
  object-fit: contain;
  border-radius: 10px;
}

.brand-name {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: #3a3550;
}

.sidebar-menu {
  flex: 1;
  padding: 16px 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  border-radius: 16px;
  color: #8a8aa8;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.25s ease;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #5c5678;
}

.menu-item.active {
  background: rgba(255, 255, 255, 0.25);
  color: #3a3550;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.menu-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.12);
  flex-shrink: 0;
}

.menu-item.active .menu-icon {
  background: rgba(255, 255, 255, 0.22);
}

.menu-icon svg {
  width: 16px;
  height: 16px;
}
</style>
