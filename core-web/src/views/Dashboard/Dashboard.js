import { getMe, logoutUser } from "../../services/auth";
import { getDashboardSummary } from "../../services/dashboard";
import logoImg from "../../assets/login/logo2.png";

export default {
  name: "DashboardView",
  data() {
    return {
      user: null,
      dashboard: null,
      logo: logoImg,
      isSidebarCollapsed: false,
      showUserMenu: false,
      currentDate: new Date(),
      calendarDays: [],
    };
  },
  computed: {
    userDisplay() {
      return (
        this.dashboard?.profile?.full_name ||
        this.user?.first_name ||
        this.user?.email ||
        "User"
      );
    },
    fullName() {
      return this.dashboard?.profile?.full_name || "Loading...";
    },
    userInitials() {
      if (this.dashboard?.profile?.initials) {
        return this.dashboard.profile.initials;
      }
      if (!this.user) return "U";
      const first = this.user.first_name?.[0] || "";
      const last = this.user.last_name?.[0] || "";
      return (first + last || this.user.email?.[0] || "U").toUpperCase();
    },
    userRoleDisplay() {
      return this.dashboard?.profile?.role || "Admin";
    },
    currentMonthYear() {
      return this.currentDate
        .toLocaleString("default", { month: "long", year: "numeric" })
        .toUpperCase();
    },
  },
  async mounted() {
    this.generateCalendar();
    document.addEventListener("click", this.handleClickOutside);

    try {
      this.user = await getMe();
    } catch (err) {
      localStorage.clear();
      this.$router.push("/");
      return;
    }

    try {
      this.dashboard = await getDashboardSummary();
      if (this.dashboard.permissions) {
        localStorage.setItem("permissions", JSON.stringify(this.dashboard.permissions));
      }
    } catch (err) {
      console.error("Dashboard data failed to load:", err);
      this.setDefaultDashboardData();
    }
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
  methods: {
    toggleUserMenu(event) {
      event.stopPropagation();
      this.showUserMenu = !this.showUserMenu;
    },
    closeUserMenu() {
      this.showUserMenu = false;
    },
    handleClickOutside(event) {
      if (!this.$el.contains(event.target)) return;
      const dropdown = this.$el.querySelector(".user-dropdown-container");
      if (dropdown && !dropdown.contains(event.target)) {
        this.closeUserMenu();
      }
    },

    generateCalendar() {
      const year = this.currentDate.getFullYear();
      const month = this.currentDate.getMonth();
      const firstDay = new Date(year, month, 1).getDay();
      const daysInMonth = new Date(year, month + 1, 0).getDate();
      const today = new Date().getDate();
      const currentMonth = new Date().getMonth();
      const currentYear = new Date().getFullYear();

      let days = [];
      for (let i = 0; i < firstDay; i++) {
        days.push({ day: "", isToday: false, muted: true });
      }
      for (let i = 1; i <= daysInMonth; i++) {
        days.push({
          day: i,
          isToday: i === today && month === currentMonth && year === currentYear,
          muted: false,
        });
      }
      this.calendarDays = days;
    },

    async handleLogout() {
      try {
        await logoutUser();
      } catch (err) {
        console.warn("Backend logout failed, clearing local session.");
      } finally {
        localStorage.clear();
        this.$router.push("/");
      }
    },

    goToRoute(path) {
      this.closeUserMenu();
      if (!path || this.$route.path === path) return;
      this.$router.push(path);
    },

    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
    },

    formatIcon(icon) {
      const iconMap = {
        home: "⌂",
        users: "👥",
        building: "🏢",
        clock: "🕘",
        calendar: "🗓️",
        shield: "🛡️",
        settings: "⚙️",
      };
      return iconMap[icon] || "•";
    },

    setDefaultDashboardData() {
      this.dashboard = {
        employees: { total: 0 },
        attendance: { present: 0 },
        leave_requests: { pending: 0 },
        roles: { count: 0, primary: "Employee" },
        profile: {
          full_name: this.user?.first_name || "User",
          role: "Admin",
        },
        quick_actions: [],
        recent_activity: [],
      };
    },
  },
};