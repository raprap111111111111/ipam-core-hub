<template>
  <div class="dashboard-page">
    <div class="dashboard-layout" :class="{ collapsed: isSidebarCollapsed }">
      
      <aside class="sidebar">
        <div class="sidebar-top">
          <div class="sidebar-brand">
            <img :src="logo" alt="HRIS Logo" class="sidebar-logo" />
            <div v-if="!isSidebarCollapsed" class="sidebar-brand-text">
              <h2>HRIS</h2>
            </div>
          </div> 
          
          <button 
            class="sidebar-toggle-inside" 
            @click="toggleSidebar" 
            type="button"
          >
            {{ isSidebarCollapsed ? ">" : "<" }}
          </button>
        </div> 

        <nav class="sidebar-nav">
          <p v-if="!isSidebarCollapsed" class="sidebar-section-title">Overview</p>
          <button
            v-for="(item, index) in dashboard?.sidebar || []"
            :key="index"
            class="sidebar-link"
            :class="{ active: $route.path === item.path }"
            @click="goToRoute(item.path)"
          >
            <span class="sidebar-icon">{{ formatIcon(item.icon) }}</span>
            <span v-if="!isSidebarCollapsed" class="sidebar-label">
              {{ item.label }}
            </span>
          </button>
        </nav>
      </aside>

      <div class="dashboard-shell">
        
        <header class="navbar">
  <div class="page-heading">
    <h2>Dashboard</h2>
    <p>Overview of your HRIS workspace</p>
  </div>

  <div class="user-dropdown-container">
    <button
      type="button"
      class="user-pill"
      @click.stop="toggleUserMenu"
    >
      <div class="user-avatar">
        <img v-if="user?.profile_photo" :src="user.profile_photo" alt="Avatar" />
        <span v-else>{{ userInitials }}</span>
      </div>

      <div class="user-meta">
        <strong>{{ userDisplay }}</strong>
      </div>

      <span class="chevron-icon" :class="{ rotated: showUserMenu }">⌄</span>
    </button>

    <transition name="fade">
      <div v-if="showUserMenu" class="dropdown-menu">
        <button class="dropdown-item primary" @click="goToRoute('/profile')">
          <span class="icon">👤</span>
          <span>Profile</span>
        </button>

        <button class="dropdown-item" @click="handleLogout">
          <span class="icon">↪</span>
          <span>Logout</span>
        </button>
      </div>
    </transition>
  </div>
</header>

        <main class="content">
          <section class="hero-card">
            <div>
              <p class="eyebrow">Welcome back</p>
              <h1>{{ userDisplay }}</h1>
              <p class="hero-subtext">
                Here’s a quick overview of your HRIS workspace today.
              </p>
            </div>

            <div class="hero-badge">
              <span class="dot"></span>
              System Connected
            </div>
          </section>

          <section class="stats-grid">
            <article class="stat-card">
              <div class="stat-top">
                <span class="stat-icon">👥</span>
                <span class="stat-label">Employees</span>
              </div>
              <h3>{{ dashboard?.employees?.total || 0 }}</h3>
              <p>Total employees</p>
            </article>

            <article class="stat-card">
              <div class="stat-top">
                <span class="stat-icon">🕘</span>
                <span class="stat-label">Attendance</span>
              </div>
              <h3>{{ dashboard?.attendance?.present || 0 }}</h3>
              <p>Present today</p>
            </article>

            <article class="stat-card">
              <div class="stat-top">
                <span class="stat-icon">🗓️</span>
                <span class="stat-label">Leave Requests</span>
              </div>
              <h3>{{ dashboard?.leave_requests?.pending || 0 }}</h3>
              <p>Pending approvals</p>
            </article>

            <article class="stat-card">
              <div class="stat-top">
                <span class="stat-icon">🛡️</span>
                <span class="stat-label">Roles</span>
              </div>
              <h3>{{ dashboard?.roles?.count || 0 }}</h3>
              <p>{{ dashboard?.roles?.primary || "Employee" }}</p>
            </article>
          </section>

          <section class="dashboard-grid">
            
            <article class="panel calendar-panel">
              <div class="panel-header">
                <h3>Upcoming Events</h3>
              </div>
              <div class="calendar-box">
                <div class="calendar-month">
                  <strong>{{ currentMonthYear }}</strong>
                </div>
                <div class="calendar-grid">
                  <span class="calendar-weekday" v-for="d in ['S','M','T','W','T','F','S']" :key="d">{{d}}</span>
                  <span
                    v-for="(date, idx) in calendarDays"
                    :key="idx"
                    class="calendar-date"
                    :class="{ active: date.isToday, muted: date.muted }"
                  >
                    {{ date.day }}
                  </span>
                </div>
                <p class="calendar-note">No upcoming holidays marked.</p>
              </div>
            </article>

            <article class="panel quick-panel">
              <div class="panel-header">
                <h3>Quick Actions</h3>
              </div>
              <div class="quick-actions">
                <button
                  v-for="(action, index) in dashboard?.quick_actions || []"
                  :key="index"
                  class="quick-btn"
                  @click="goToRoute(action.route)"
                >
                  {{ action.label }}
                </button>
              </div>
            </article>

            <article class="panel activity-panel">
              <div class="panel-header">
                <h3>Recent Activity</h3>
                <span class="panel-tag">Today</span>
              </div>
              <div v-if="dashboard?.recent_activity?.length" class="activity-list">
                <div v-for="(item, index) in dashboard.recent_activity" :key="index" class="activity-item">
                  <span class="activity-dot" :class="{ purple: index === 0 }"></span>
                  <div class="activity-content">
                    <strong>{{ item.title }}</strong>
                    <p>{{ item.description }}</p>
                  </div>
                </div>
              </div>
              <div v-else class="empty-state">No recent activity available.</div>
            </article>

          </section>
        </main>
      </div>
    </div>
  </div>
</template>

<script src="./Dashboard.js"></script>
<style scoped src="./Dashboard.css"></style>