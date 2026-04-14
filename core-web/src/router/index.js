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

export default router;