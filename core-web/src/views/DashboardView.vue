<template>
  <div class="dashboard-page">
    <header class="navbar">
      <div class="brand">
        <img :src="logo" alt="HRIS Logo" />
        <div class="brand-text">
          <h2>HRIS Dashboard</h2>
          <p>Temporary dashboard</p>
        </div>
      </div>

      <button type="button" class="logout-btn" @click="handleLogout">
        Logout
      </button>
    </header>

    <main class="content">
      <section class="hero">
        <h1>Welcome, {{ userDisplay }}</h1>
        <p>Connected to your DRF JWT authentication system.</p>
      </section>

      <section class="cards">
        <div class="info-card">
          <h3>Employees</h3>
          <p>Temporary stats</p>
          <strong>124</strong>
        </div>

        <div class="info-card">
          <h3>Attendance</h3>
          <p>Temporary stats</p>
          <strong>96 Present Today</strong>
        </div>

        <div class="info-card">
          <h3>Leave Requests</h3>
          <p>Temporary stats</p>
          <strong>8 Pending</strong>
        </div>

        <div class="info-card">
          <h3>Roles</h3>
          <p>Temporary stats</p>
          <strong>Admin / HR / Employee</strong>
        </div>
      </section>

      <section class="user-box">
        <h3>User Data</h3>
        <pre>{{ formattedUser }}</pre>
      </section>
    </main>
  </div>
</template>

<script>
import { getMe, logoutUser } from "../services/auth";
import logo from "../assets/login/logo.png";

export default {
  name: "DashboardView",
  data() {
    return {
      user: null,
      logo,
    };
  },
  computed: {
    userDisplay() {
      if (!this.user) return "User";
      return this.user.first_name || this.user.email || "User";
    },
    formattedUser() {
      return this.user ? JSON.stringify(this.user, null, 2) : "Loading...";
    },
  },
  async mounted() {
    try {
      this.user = await getMe();
    } catch (err) {
      localStorage.clear();
      this.$router.push("/");
    }
  },
  methods: {
    async handleLogout() {
      try {
        await logoutUser();
      } catch (err) {
        console.log("Backend logout failed, clearing local session anyway.");
      } finally {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user_data");
        this.$router.push("/");
      }
    },
  },
};
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #18398d 0%, #d18aad 100%);
  color: white;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 28px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.brand img {
  width: 56px;
  height: 56px;
  object-fit: contain;
}

.brand-text h2 {
  margin: 0;
  font-size: 24px;
}

.brand-text p {
  margin: 4px 0 0;
  opacity: 0.85;
}

.logout-btn {
  border: none;
  border-radius: 12px;
  background: white;
  color: #18398d;
  padding: 10px 18px;
  font-weight: 700;
  cursor: pointer;
}

.content {
  padding: 30px;
}

.hero h1 {
  margin: 0 0 10px;
  font-size: 38px;
}

.hero p {
  margin: 0;
  opacity: 0.9;
}

.cards {
  margin-top: 28px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}

.info-card {
  border-radius: 20px;
  padding: 22px;
  backdrop-filter: blur(14px);
}

.info-card h3 {
  margin-top: 0;
}

.user-box {
  margin-top: 28px;
  border-radius: 20px;
  padding: 24px;
}

pre {
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
}
</style>