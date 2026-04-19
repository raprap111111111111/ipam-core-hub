import { createRouter, createWebHistory } from 'vue-router';
import MainLayout from '../layouts/MainLayout.vue';
import DashboardView from '../views/Dashboard/Dashboard.vue';
import ProfileView from '../views/Profile/Profile.vue';

const routes = [
  {
    path: '/',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/dashboard',
    component: MainLayout,
    children: [
      {
        path: '', 
        name: 'dashboard',
        component: DashboardView
      },

      {
        path: '/profile', // Add a leading slash to make it top-level under the layout
        name: 'profile',
        component: ProfileView
      },

      {
        path: '/employees',
        name: 'employees',
        component: () => import('../views/Employees/EmployeesView.vue')
      },

      {
        path: '/companies',
        name: 'companies',
        component: () => import('../views/Companies/CompaniesView.vue')
      }
      
      // COMMENT THIS OUT UNTIL YOU CREATE THE FILE
      // {
      //   path: '/employees',
      //   name: 'employees',
      //   component: () => import('../views/EmployeesView.vue')
      // }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// --- ADD THIS BLOCK HERE ---
router.beforeEach((to, from, next) => {
  // 1. Get the token from storage
  const token = localStorage.getItem("access_token");

  // 2. If trying to access a protected page (like dashboard) without a token
  if (to.path !== '/' && !token) {
    next({ name: 'login' }); // Force them to login page
  } 
  // 3. If they are already logged in and try to go to the login page
  else if (to.path === '/' && token) {
    next({ name: 'dashboard' }); // Skip login and go to dashboard
  } 
  // 4. Otherwise, let them through
  else {
    next();
  }
});

export default router;