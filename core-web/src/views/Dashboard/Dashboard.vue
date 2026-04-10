<template>
  <div class="dashboard-view">
    <section class="hero-card">
      <div>
        <p class="eyebrow">WELCOME BACK</p>
        <h1>{{ fullName }}</h1>
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
      <article class="stat-card" v-for="stat in stats" :key="stat.label">
        <div class="stat-top">
          <span class="stat-icon">{{ stat.icon }}</span>
          <span class="stat-label">{{ stat.label }}</span>
        </div>
        <h3>{{ stat.value }}</h3>
        <p>{{ stat.sub }}</p>
      </article>
    </section>

    <section class="dashboard-grid">
      <article class="panel">
        <div class="panel-header">
          <h3>Upcoming Events</h3>
        </div>

        <div class="calendar-box">
          <div class="calendar-month">
            <strong>{{ currentMonthYear }}</strong>
          </div>

          <div class="calendar-grid">
            <span
              v-for="day in weekdays"
              :key="day"
              class="calendar-weekday"
            >
              {{ day }}
            </span>

            <span
              v-for="(date, i) in calendarDays"
              :key="i"
              class="calendar-date"
              :class="{ active: date.isToday, muted: date.muted }"
            >
              {{ date.day }}
            </span>
          </div>

          <p class="calendar-note">No upcoming holidays marked.</p>
        </div>
      </article>

      <article class="panel">
        <div class="panel-header">
          <h3>Quick Actions</h3>
        </div>

        <div class="quick-actions">
          <button
            v-for="action in dashboardData?.quick_actions || []"
            :key="action.label"
            class="quick-btn"
            @click="goToRoute(action.route)"
          >
            {{ action.label }}
          </button>
        </div>
      </article>

      <article class="panel">
        <div class="panel-header">
          <h3>Recent Activity</h3>
          <span class="panel-tag">Today</span>
        </div>

        <div
          v-if="dashboardData?.recent_activity?.length"
          class="activity-list"
        >
          <div
            v-for="(item, index) in dashboardData.recent_activity"
            :key="index"
            class="activity-item"
          >
            <span class="activity-dot"></span>
            <div class="activity-content">
              <strong>{{ item.title }}</strong>
              <p>{{ item.description }}</p>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          No recent activity available.
        </div>
      </article>
    </section>
  </div>
</template>

<script>
export default {
  name: "DashboardView",
  props: {
    user: {
      type: Object,
      default: null,
    },
    dashboardData: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      currentDate: new Date(),
      calendarDays: [],
      weekdays: ["S", "M", "T", "W", "T", "F", "S"],
    };
  },
  computed: {
    fullName() {
      return this.dashboardData?.profile?.full_name || this.user?.first_name || "User";
    },
    currentMonthYear() {
      return this.currentDate
        .toLocaleString("default", {
          month: "long",
          year: "numeric",
        })
        .toUpperCase();
    },
    stats() {
      const d = this.dashboardData;

      return [
        {
          label: "Employees",
          value: d?.employees?.total || 0,
          icon: "👥",
          sub: "Total employees",
        },
        {
          label: "Attendance",
          value: d?.attendance?.present || 0,
          icon: "🕘",
          sub: "Present today",
        },
        {
          label: "Leave Requests",
          value: d?.leave_requests?.pending || 0,
          icon: "🗓️",
          sub: "Pending approvals",
        },
        {
          label: "Roles",
          value: d?.roles?.count || 0,
          icon: "🛡️",
          sub: d?.roles?.primary || "Employee",
        },
      ];
    },
  },
  mounted() {
    this.generateCalendar();
  },
  methods: {
    generateCalendar() {
      const year = this.currentDate.getFullYear();
      const month = this.currentDate.getMonth();
      const firstDay = new Date(year, month, 1).getDay();
      const daysInMonth = new Date(year, month + 1, 0).getDate();

      const today = new Date();
      const currentDay = today.getDate();
      const currentMonth = today.getMonth();
      const currentYear = today.getFullYear();

      const leadingDays = Array.from({ length: firstDay }, () => ({
        day: "",
        muted: true,
        isToday: false,
      }));

      const monthDays = Array.from({ length: daysInMonth }, (_, i) => ({
        day: i + 1,
        muted: false,
        isToday:
          i + 1 === currentDay &&
          month === currentMonth &&
          year === currentYear,
      }));

      this.calendarDays = [...leadingDays, ...monthDays];
    },
    goToRoute(path) {
      if (!path || this.$route.path === path) return;
      this.$router.push(path);
    },
  },
};
</script>

<style scoped src="./Dashboard.css"></style>