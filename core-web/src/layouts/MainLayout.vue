<template>
  <div class="app-viewport">
    <div class="dashboard-layout" :class="{ collapsed: isSidebarCollapsed }">
      <aside class="sidebar">
        <div class="sidebar-top">
          <div class="sidebar-brand">
            <img :src="logo" alt="Logo" class="sidebar-logo" />
            <div v-if="!isSidebarCollapsed" class="sidebar-brand-text">
              <h2>CORE</h2>
            </div>
          </div>

          <button
            type="button"
            class="sidebar-toggle-inside"
            @click="toggleSidebar"
          >
            {{ isSidebarCollapsed ? ">" : "<" }}
          </button>
        </div>

        <nav class="sidebar-nav">
          <p v-if="!isSidebarCollapsed" class="sidebar-section-title">
            Overview
          </p>

          <button
            v-for="(item, index) in sidebarLinks"
            :key="index"
            type="button"
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
            <h2>{{ currentPageTitle }}</h2>
            <p>System Connected</p>
          </div>

          <div class="user-dropdown-container" ref="userDropdown">
            <button
              type="button"
              class="user-pill"
              @click.stop="toggleUserMenu"
            >
              <div class="user-avatar">
                <img
                  v-if="user?.profile_photo"
                  :src="formatImageUrl(user.profile_photo)"
                  alt="User Avatar"
                />
                <span v-else>{{ userInitials }}</span>
              </div>

              <div class="user-meta">
                <strong>{{ userName }}</strong>
              </div>

              <span class="chevron-icon" :class="{ rotated: showUserMenu }">
                ⌄
              </span>
            </button>

            <transition name="fade">
              <div v-if="showUserMenu" class="dropdown-menu">
                <button
                  type="button"
                  class="dropdown-item dropdown-item-primary"
                  @click="goToRoute('/profile')"
                >
                  <span class="dropdown-icon">👤</span>
                  <span>Profile</span>
                </button>

                <button
                  type="button"
                  class="dropdown-item"
                  @click="handleLogout"
                >
                  <span class="dropdown-icon">↪</span>
                  <span>Logout</span>
                </button>
              </div>
            </transition>
          </div>
        </header>

        <main class="content">
          <router-view 
            :user="user" 
            :dashboardData="dashboardData" 
            @refresh-user="fetchInitialData" 
          />
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import { getMe, logoutUser } from '../services/auth.js';
import { getDashboardSummary } from '../services/dashboard.js';
import logoImg from "../assets/login/logo2.png";

export default {
  name: "MainLayout",
  data() {
    return {
      user: null,
      dashboardData: null,
      logo: logoImg,
      isSidebarCollapsed: false,
      showUserMenu: false,
    };
  },
  computed: {
    userName() {
      return (
        this.dashboardData?.profile?.full_name ||
        this.user?.first_name ||
        "User"
      );
    },
    userInitials() {
      const first = this.user?.first_name?.[0] || "";
      const last = this.user?.last_name?.[0] || "";
      return (first + last || this.user?.email?.[0] || "U").toUpperCase();
    },
    currentPageTitle() {
      return this.$route.name?.toUpperCase() || "CORE HUB";
    },
    sidebarLinks() {
      return this.dashboardData?.sidebar || [];
    },
  },
  async mounted() {
    document.addEventListener("click", this.handleClickOutside);
    // Initialize data on mount
    await this.fetchInitialData();
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
  methods: {
    async fetchInitialData() {
      try {
        const [userRes, dashRes] = await Promise.all([
          getMe(),
          getDashboardSummary()
        ]);
        this.user = userRes;
        this.dashboardData = dashRes.data;
      } catch (err) {
        console.error("Data fetch failed:", err);
        // Redirect to login if unauthorized
        if (err.response?.status === 401) {
          localStorage.clear();
          this.$router.push("/");
        }
      }
    },
    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
    },
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu;
    },
    formatImageUrl(url) {
      if (!url) return null;
      if (url.startsWith('http')) return url;
      return `http://127.0.0.1:8002${url}`;
    },
    handleClickOutside(event) {
      if (
        this.$refs.userDropdown &&
        !this.$refs.userDropdown.contains(event.target)
      ) {
        this.showUserMenu = false;
      }
    },
    goToRoute(path) {
      this.showUserMenu = false;
      if (!path || this.$route.path === path) return;
      this.$router.push(path);
    },
    formatIcon(icon) {
      const map = {
        home: "⌂",
        users: "👥",
        building: "🏢",
        clock: "🕘",
        calendar: "🗓️",
        shield: "🛡️",
        settings: "⚙️",
      };
      return map[icon] || "•";
    },
    async handleLogout() {
      try {
        await logoutUser();
      } catch (err) {
        console.warn("Logout failed, clearing local session.");
      } finally {
        localStorage.clear();
        this.$router.push("/");
      }
    },
  },
};
</script>

<style scoped src="./Main.css"></style>