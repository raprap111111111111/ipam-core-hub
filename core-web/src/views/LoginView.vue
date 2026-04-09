<template>
  <div class="login-page">
    <!-- Decorative background layers -->
    <div class="aurora aurora-1"></div>
    <div class="aurora aurora-2"></div>
    <div class="aurora aurora-3"></div>
    <div class="stars"></div>
    <div class="grid-glow"></div>

    <!-- Enhanced Shooting Stars -->
    <div class="shooting-star star-1"></div>
    <div class="shooting-star star-2"></div>
    <div class="shooting-star star-3"></div>
    <div class="shooting-star star-4"></div>
    <div class="shooting-star star-5"></div>

    <div class="login-layout">
      <!-- Left illustration -->
      <div class="left-panel">
        <div class="illustration-wrap">
          <img
            class="left-illustration"
            :src="hrisHuman"
            alt="HRIS Human Illustration"
          />
        </div>
      </div>

      <!-- Right login card -->
      <div class="right-panel">
        <div class="login-card">
          <!-- Brand / Logo Only - No Badge -->
          <div class="logo-section">
            <img class="logo" :src="logo" alt="HRIS Logo" />
          </div>

          <!-- Welcome -->
          <div class="welcome-section">
            <h1>Welcome Back!</h1>
            <p>Please sign in to your account</p>
          </div>

          <!-- Form -->
          <form class="login-form" @submit.prevent="handleLogin">
            <div class="input-wrapper">
              <span class="input-icon">👤</span>
              <input
                v-model="form.email"
                type="text"
                placeholder="Email or Username"
                autocomplete="username"
                required
              />
            </div>

            <div class="input-wrapper">
              <span class="input-icon">🔒</span>
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Password"
                autocomplete="current-password"
                required
              />
              <button
                type="button"
                class="toggle-password"
                @click="togglePassword"
                aria-label="Toggle password visibility"
              >
                {{ showPassword ? "🙈" : "👁" }}
              </button>
            </div>

            <div class="forgot-row">
              <a href="#">Forgot Password?</a>
            </div>

            <button class="login-btn" type="submit" :disabled="loading">
              <span class="btn-shine"></span>
              <span class="btn-text">{{ loading ? "Signing in..." : "Login" }}</span>
            </button>

            <p v-if="error" class="error-message">{{ error }}</p>

            <div class="help-text">
              <span></span>
              <p>Need help? Contact Admin</p>
              <span></span>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { loginUser } from "../services/auth";
import hrisHuman from "../assets/login/hris_human.png";
import logo from "../assets/login/logo.png";

export default {
  name: "LoginView",

  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      loading: false,
      error: "",
      showPassword: false,
      hrisHuman,
      logo,
    };
  },

  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword;
    },

    async handleLogin() {
      this.loading = true;
      this.error = "";

      try {
        const data = await loginUser({
          email: this.form.email,
          password: this.form.password,
        });

        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);
        localStorage.setItem("user_data", JSON.stringify(data.user));

        this.$router.push("/dashboard");
      } catch (err) {
        this.error =
          err?.response?.data?.detail ||
          err?.response?.data?.error ||
          err?.response?.data?.non_field_errors?.[0] ||
          "Invalid login credentials.";

        console.error("Login failed:", err);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* =========================================================
   DEBUG / THEME TOKENS
   ---------------------------------------------------------
   Change values here first.
   This is your "easy debugger / design controller".
   ========================================================= */
:global(:root) {
  /* Main colors */
  --color-primary: #3f6bff;
  --color-secondary: #66e7ff;
  --color-accent: #c488d8;
  --color-bg-deep: #0d1b52;
  --color-bg-mid: #1f46a9;
  --color-bg-soft: #5f63bf;
  --color-bg-pink: #b77cb2;

  /* Text colors */
  --color-text-main: #ffffff;
  --color-text-soft: rgba(255, 255, 255, 0.9);
  --color-text-muted: rgba(255, 255, 255, 0.78);

  /* Card / glass */
  --card-bg-top: rgba(255, 255, 255, 0.11);
  --card-bg-bottom: rgba(255, 255, 255, 0.06);
  --card-border: rgba(255, 255, 255, 0.14);
  --card-shadow: rgba(7, 15, 45, 0.3);

  /* Inputs */
  --input-bg: rgba(7, 18, 58, 0.26);
  --input-bg-focus: rgba(8, 22, 66, 0.36);
  --input-border: rgba(255, 255, 255, 0.12);
  --input-focus: rgba(109, 239, 255, 0.48);

  /* Sizing */
  --card-max-width: 520px;
 --logo-width: 260px;         /* Bigger logo */
  --logo-badge-width: 960px;     /* Adjusted badge */
  --input-height: 54px;
  --button-height: 54px;
  --card-radius: 30px;
  --input-radius: 18px;
  --button-radius: 18px;

  /* Spacing */
  --card-padding-top: 16px;
  --card-padding-x: 24px;
  --card-padding-bottom: 20px;
  --welcome-gap-top: 10px;
  --welcome-gap-bottom: 16px;

  /* Typography */
  --brand-title-size: 2rem;
  --welcome-title-max: 3.15rem;
  --welcome-title-min: 1.9rem;
  --body-font: Inter, Arial, sans-serif;
}

/* =========================================================
   Global reset
   ========================================================= */
:global(html),
:global(body),
:global(#app) {
  margin: 0;
  padding: 0;
  width: 100%;
  min-height: 100%;
  overflow-x: hidden;
}

:global(body) {
  font-family: var(--body-font);
  background: var(--color-bg-deep);
}

* {
  box-sizing: border-box;
}

/* =========================================================
   Page background
   ========================================================= */
.login-page {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow: hidden;
  background:
    radial-gradient(circle at 15% 15%, rgba(72, 134, 255, 0.22), transparent 22%),
    radial-gradient(circle at 85% 18%, rgba(255, 153, 212, 0.18), transparent 24%),
    radial-gradient(circle at 50% 90%, rgba(123, 97, 255, 0.12), transparent 24%),
    linear-gradient(
      135deg,
      var(--color-bg-deep) 0%,
      var(--color-bg-mid) 34%,
      var(--color-bg-soft) 62%,
      var(--color-bg-pink) 100%
    );
}

/* =========================================================
   Aurora
   ========================================================= */
.aurora {
  position: absolute;
  border-radius: 999px;
  filter: blur(70px);
  opacity: 0.45;
  pointer-events: none;
  animation: drift 16s ease-in-out infinite alternate;
}

.aurora-1 {
  top: -8%;
  left: -10%;
  width: 420px;
  height: 420px;
  background: rgba(70, 200, 255, 0.16);
}

.aurora-2 {
  right: -6%;
  top: 10%;
  width: 380px;
  height: 380px;
  background: rgba(255, 152, 207, 0.16);
  animation-duration: 20s;
}

.aurora-3 {
  bottom: -10%;
  left: 35%;
  width: 400px;
  height: 400px;
  background: rgba(121, 109, 255, 0.14);
  animation-duration: 18s;
}

/* =========================================================
   Stars / grid
   ========================================================= */
.stars {
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.9;
  background-image:
    radial-gradient(circle at 8% 18%, rgba(255,255,255,0.75) 0 1.1px, transparent 1.8px),
    radial-gradient(circle at 20% 72%, rgba(255,255,255,0.5) 0 1.2px, transparent 2px),
    radial-gradient(circle at 32% 28%, rgba(255,255,255,0.75) 0 1px, transparent 2px),
    radial-gradient(circle at 48% 14%, rgba(255,255,255,0.45) 0 1px, transparent 2px),
    radial-gradient(circle at 57% 78%, rgba(255,255,255,0.7) 0 1px, transparent 2px),
    radial-gradient(circle at 68% 25%, rgba(255,255,255,0.65) 0 1.2px, transparent 2px),
    radial-gradient(circle at 79% 54%, rgba(255,255,255,0.5) 0 1px, transparent 2px),
    radial-gradient(circle at 88% 20%, rgba(255,255,255,0.8) 0 1.2px, transparent 2px),
    radial-gradient(circle at 92% 72%, rgba(255,255,255,0.55) 0 1px, transparent 2px);
  animation: twinkle 6s ease-in-out infinite alternate;
}

.grid-glow {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 64px 64px;
  mask-image: radial-gradient(circle at center, black 35%, transparent 92%);
  opacity: 0.18;
}

/* =========================================================
   Shooting stars
   ========================================================= */
.shooting-star {
  position: absolute;
  width: 180px;
  height: 2px;
  border-radius: 999px;
  pointer-events: none;
  opacity: 0;
  background: linear-gradient(
    90deg,
    rgba(255,255,255,0),
    rgba(255,255,255,0.95),
    rgba(120,220,255,0.8),
    rgba(255,255,255,0)
  );
  box-shadow: 0 0 12px rgba(255,255,255,0.45);
  transform: rotate(-25deg);
}

.star-1 {
  top: 14%;
  left: 12%;
  animation: shootingStar 7s linear infinite;
}

.star-2 {
  top: 28%;
  left: 52%;
  animation: shootingStar 9s linear infinite 2s;
}

.star-3 {
  top: 8%;
  left: 70%;
  animation: shootingStar 11s linear infinite 4s;
}

/* =========================================================
   Layout
   ========================================================= */
.login-layout {
  position: relative;
  z-index: 2;
  min-height: 100vh;
  width: 100%;
  display: grid;
  grid-template-columns: minmax(320px, 1.1fr) minmax(380px, 0.9fr);
  align-items: center;
  gap: 28px;
  padding: 24px 36px;
}

.left-panel,
.right-panel {
  min-width: 0;
}

.left-panel {
  display: flex;
  align-items: center;
  justify-content: center;
}

.illustration-wrap {
  width: 100%;
  max-width: 700px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.left-illustration {
  width: min(100%, 620px);
  max-height: 76vh;
  object-fit: contain;
  filter: drop-shadow(0 24px 40px rgba(7, 14, 42, 0.28));
  animation: floatHuman 6s ease-in-out infinite;
  transform-origin: center bottom;
}

.right-panel {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* =========================================================
   Card
   ========================================================= */
.login-card {
  width: min(100%, var(--card-max-width));
  padding: var(--card-padding-top) var(--card-padding-x) var(--card-padding-bottom);
  border-radius: var(--card-radius);
  background: linear-gradient(180deg, var(--card-bg-top) 0%, var(--card-bg-bottom) 100%);
  border: 1px solid var(--card-border);
  backdrop-filter: blur(18px) saturate(120%);
  box-shadow:
    0 24px 60px var(--card-shadow),
    inset 0 1px 0 rgba(255,255,255,0.12);
  color: var(--color-text-main);
  animation: cardFadeIn 0.8s ease-out;
}

/* =========================================================
   Logo / brand
   ========================================================= */
.logo-section {
  text-align: center;
  padding: 0 0 4px 0;
  border-bottom: none;
  background: transparent;
  box-shadow: none;
  overflow: visible;
}


/*
  If the PNG itself has transparent empty space,
  this negative bottom margin visually compensates for it.
*/
.logo {
  width: 320px;
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0 auto -22px;
  object-fit: contain;
  background: transparent;
  box-shadow: none;
  filter: none;
  transform: none;
  transform-origin: center center;
}


.brand-title {
  margin: 4px 0 2px;
  font-size: var(--brand-title-size);
  line-height: 1;
  font-weight: 800;
  letter-spacing: 0.04em;
  color: var(--color-text-main);
}

.system-name {
  margin: 0;
  font-size: 13px;
  color: rgba(255,255,255,0.85);
  letter-spacing: 0.01em;
}

/* =========================================================
   Welcome
   ========================================================= */
/* Adjust spacing after removing badge */
.welcome-section {
  text-align: center;
  margin: 20px 0 22px 0;
}

.welcome-section h1 {
  margin: 0 0 6px;
  font-size: clamp(var(--welcome-title-min), 3.4vw, var(--welcome-title-max));
  line-height: 1;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.welcome-section p {
  margin: 0;
  font-size: clamp(0.95rem, 1.3vw, 1.08rem);
  color: var(--color-text-soft);
}

/* =========================================================
   Form
   ========================================================= */
.login-form {
  display: flex;
  flex-direction: column;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  min-height: var(--input-height);
  margin-bottom: 14px;
  border-radius: var(--input-radius);
  border: 1px solid var(--input-border);
  background: var(--input-bg, rgba(7, 18, 58, 0.26));
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.06);
  transition: border-color 0.22s ease, transform 0.22s ease, background 0.22s ease;
}

.input-wrapper:focus-within {
  border-color: var(--input-focus);
  background: var(--input-bg-focus);
  transform: translateY(-1px);
}

.input-icon {
  width: 50px;
  text-align: center;
  font-size: 18px;
  opacity: 0.95;
}

.input-wrapper input {
  flex: 1;
  height: var(--input-height);
  border: 0;
  outline: none;
  background-color: transparent !important;
  appearance: none;
  color: var(--color-text-main);
  font-size: 1rem;
  padding-right: 14px;
}

.input-wrapper input::placeholder {
  color: var(--color-text-muted);
}

.toggle-password {
  border: 0;
  background: transparent;
  color: var(--color-text-main);
  font-size: 18px;
  padding: 0 16px 0 8px;
  cursor: pointer;
  opacity: 0.92;
}

.forgot-row {
  display: flex;
  justify-content: flex-end;
  margin: -2px 0 14px;
}

.forgot-row a {
  color: rgba(255,255,255,0.95);
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
}

.forgot-row a:hover {
  text-decoration: underline;
}

/* =========================================================
   Button
   ========================================================= */
.login-btn {
  position: relative;
  overflow: hidden;
  height: var(--button-height);
  border: 0;
  border-radius: var(--button-radius);
  background: linear-gradient(90deg, var(--color-secondary) 0%, var(--color-primary) 100%);
  color: var(--color-text-main);
  font-size: 1.55rem;
  font-weight: 800;
  letter-spacing: 0.01em;
  cursor: pointer;
  box-shadow: 0 14px 30px rgba(35, 84, 255, 0.3);
  transition: transform 0.22s ease, box-shadow 0.22s ease, opacity 0.22s ease;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 18px 34px rgba(35, 84, 255, 0.36);
}

.login-btn:disabled {
  opacity: 0.72;
  cursor: not-allowed;
  transform: none;
}

.btn-text {
  position: relative;
  z-index: 2;
}

.btn-shine {
  position: absolute;
  top: 0;
  left: -35%;
  width: 30%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255,255,255,0.26),
    transparent
  );
  transform: skewX(-22deg);
  animation: shine 3.2s linear infinite;
}

/* =========================================================
   Messages / footer
   ========================================================= */
.error-message {
  margin: 14px 0 0;
  padding: 12px 14px;
  border-radius: 14px;
  background: rgba(255, 88, 88, 0.14);
  border: 1px solid rgba(255,255,255,0.12);
  font-size: 14px;
  color: var(--color-text-main);
}

.help-text {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 16px;
}

.help-text span {
  flex: 1;
  height: 1px;
  background: rgba(255,255,255,0.12);
}

.help-text p {
  margin: 0;
  font-size: 13px;
  color: var(--color-text-soft);
  white-space: nowrap;
}

/* =========================================================
   Animations
   ========================================================= */
@keyframes floatHuman {
  0% {
    transform: translateY(0px) scale(1);
    filter: drop-shadow(0 24px 40px rgba(7, 14, 42, 0.26));
  }
  50% {
    transform: translateY(-10px) scale(1.012);
    filter: drop-shadow(0 30px 46px rgba(7, 14, 42, 0.34));
  }
  100% {
    transform: translateY(0px) scale(1);
    filter: drop-shadow(0 24px 40px rgba(7, 14, 42, 0.26));
  }
}

@keyframes drift {
  0% { transform: translate3d(0, 0, 0) scale(1); }
  50% { transform: translate3d(16px, -18px, 0) scale(1.03); }
  100% { transform: translate3d(-10px, 10px, 0) scale(0.98); }
}

@keyframes twinkle {
  0% { opacity: 0.72; }
  100% { opacity: 1; }
}

@keyframes shine {
  0% { left: -35%; }
  100% { left: 125%; }
}

@keyframes cardFadeIn {
  from {
    opacity: 0;
    transform: translateY(18px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes shootingStar {
  0% {
    opacity: 0;
    transform: translate3d(0, 0, 0) rotate(-25deg) scaleX(0.5);
  }
  8% {
    opacity: 1;
  }
  30% {
    opacity: 1;
    transform: translate3d(220px, 120px, 0) rotate(-25deg) scaleX(1);
  }
  100% {
    opacity: 0;
    transform: translate3d(320px, 190px, 0) rotate(-25deg) scaleX(0.7);
  }
}

/* =========================================================
   Responsive
   ========================================================= */
@media (max-width: 1180px) {
  :global(:root) {
    --card-max-width: 620px;
    --logo-width: 150px;
  }

  .login-layout {
    grid-template-columns: 1fr;
    justify-items: center;
    padding: 20px 18px;
    gap: 16px;
  }

  .left-panel {
    order: 2;
    width: 100%;
  }

  .right-panel {
    order: 1;
    width: 100%;
  }

  .left-illustration {
    width: min(100%, 430px);
    max-height: 32vh;
  }
}

@media (max-width: 640px) {
  :global(:root) {
    --card-padding-top: 16px;
    --card-padding-x: 14px;
    --card-padding-bottom: 18px;
    --logo-width: 135px;
    --logo-badge-width: 190px;
    --input-height: 50px;
    --button-height: 50px;
    --card-radius: 22px;
    --input-radius: 14px;
    --button-radius: 16px;
    --brand-title-size: 1.65rem;
  }

  .login-layout {
    padding: 14px 12px;
    gap: 12px;
  }

  .left-illustration {
    width: min(100%, 320px);
    max-height: 24vh;
  }

  .help-text p {
    font-size: 12px;
  }
}
</style>