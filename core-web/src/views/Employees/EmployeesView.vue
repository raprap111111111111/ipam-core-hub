<template>
  <div class="employees-container">
    <div class="workforce-card">
      
      <div class="card-header">
        <div class="title-group">
          <h1 class="main-title">Workforce Management</h1>
          <p class="sub-title">Core Hub Workforce</p>
        </div>
        <div class="header-actions">
          <button class="btn btn-primary" @click="handleAddEmployee">+ Add Employee</button>
          
          <div class="dropdown-wrapper" style="position: relative;">
            <button class="btn btn-secondary" @click="toggleBulk">
              Bulk Actions ⌄
            </button>
              <div v-if="isBulkOpen" class="custom-dropdown-menu">
              <button @click="confirmBulkDelete">Delete Selected</button>
              <button @click="handleBulkAction('status')">Change Status</button>
            </div>
          </div>
        </div>
      </div>

      <div class="table-controls">
            <div class="search-wrapper">
            <span class="search-icon">🔍</span>
            <input 
                type="text" 
                v-model="searchQuery" 
                placeholder="Search..." 
                @keyup.enter="handleSearch" 
            />
            <button class="btn btn-primary search-btn" @click="handleSearch">
                Search
            </button>
            </div>
        
        <div class="filter-tabs">
          <button 
            v-for="tab in tabs" :key="tab"
            :class="['tab-btn', { active: currentTab === tab }]"
            @click="currentTab = tab"
          >{{ tab }}</button>
        </div>
        <button class="btn btn-secondary">Export ⌄</button>
      </div>

      <div class="table-responsive">
        <table class="employee-table">
          <thead>
            <tr>
              <th>
                <input 
                  type="checkbox" 
                  @change="toggleSelectAll" 
                  :checked="selectedIds.length === filteredEmployees.length && filteredEmployees.length > 0" 
                />
              </th>
              <th>Photo</th>
              <th @click="handleSort('first_name')" class="sortable-header">
                Name 
                <span>{{ sortConfig.key === 'first_name' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : '' }}</span>
              </th>
              <th @click="handleSort('employee_id')" class="sortable-header">
                Employee ID
                <span>{{ sortConfig.key === 'employee_id' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : '' }}</span>
              </th>
              <th @click="handleSort('hired_at')" class="sortable-header">
                Hired At
                <span>{{ sortConfig.key === 'hired_at' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : '' }}</span>
              </th>
              <th>Department</th>
              <th>Status</th>
              <th>Verification</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
           <tr v-if="isLoading">
            <td colspan="8" style="text-align: center; padding: 40px;">Loading...</td>
          </tr>
          <tr v-else v-for="emp in filteredEmployees" :key="emp.id">
              <td>
                <input 
                  type="checkbox" 
                  :checked="selectedIds.includes(emp.id)" 
                  @change="toggleSelect(emp.id)" 
                />
              </td>

              <td>
                <div style="display: flex; align-items: center; gap: 10px;">
                  <div 
                    class="user-avatar shadow-sm"
                    :style="{ 
                      backgroundColor: !formatImageUrl(emp.profile_photo) 
                        ? `${getCompanyColor(emp.company)} !important` 
                        : 'transparent !important' 
                    }"
                  >
                    <span v-if="!formatImageUrl(emp.profile_photo)" class="initials-text">
                      {{ getInitials(emp) }}
                    </span>
                    <img v-if="formatImageUrl(emp.profile_photo)" :src="formatImageUrl(emp.profile_photo)" class="emp-avatar" />
                  </div>
                </div>
              </td>

              <td class="bold-text">{{ emp.first_name }} {{ emp.last_name }}</td>
              
              <td class="text-soft">{{ emp.employee_id }}</td>
              
              <td>{{ formatDate(emp.hired_at) }}</td>
              
              <td>{{ emp.department_name || emp.department }}</td>
              
              <td>
                <span :class="['status-badge', emp.is_active ? 'active' : 'offboarded']">
                  {{ emp.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              
              <td>TIN, SSS <i class="check-icon">✓</i></td>
              <td class="actions-cell">
                  <div class="action-buttons">
                    <button class="action-btn edit" @click="handleEditEmployee(emp)" title="Edit">
                      ✏️
                    </button>
                    <button class="action-btn delete" @click="confirmDelete(emp)" title="Delete">
                      🗑️
                    </button>
                  </div>
                </td>
            </tr>
          <tr v-if="!isLoading && filteredEmployees.length === 0">
            <td colspan="8" style="text-align: center; padding: 40px; color: grey;">No employees found.</td>
          </tr>
        </tbody>
        </table>
      </div>

<div class="pagination-footer" v-if="pagination.totalPages > 1">
  <button 
    :disabled="pagination.current === 1" 
    @click="fetchEmployees(pagination.current - 1)" 
    class="page-btn"
  >
    Prev
  </button>

  <span class="page-info">
    Page {{ pagination.current }} of {{ pagination.totalPages }}
  </span>

  <button 
    :disabled="pagination.current === pagination.totalPages" 
    @click="fetchEmployees(pagination.current + 1)" 
    class="page-btn"
  >
    Next
  </button>
</div>

    </div>
  </div>

<Teleport to="body">
  <div v-if="isModalOpen || isDeleteModalOpen" class="modal-overlay" @click.self="isModalOpen = false; isDeleteModalOpen = false">
    
    <div v-if="isModalOpen" class="modal-content large-modal shadow-lg">
      <div class="modal-header">
        <h2>{{ isEditing ? 'Edit Employee Profile' : 'Create New Employee Profile' }}</h2>
        <button class="close-x" @click="isModalOpen = false">&times;</button>
      </div>

      <form @submit.prevent="submitEmployee" class="employee-form">
        <div class="form-grid">
          <div class="form-group">
            <label>First Name *</label>
            <input type="text" v-model="newEmp.first_name" required />
          </div>
          <div class="form-group">
            <label>Last Name *</label>
            <input type="text" v-model="newEmp.last_name" required />
          </div>
          <div class="form-group">
            <label>Company *</label>
            <select v-model="newEmp.company" required>
                <option value="" disabled>Select Company</option>
                <option v-for="co in companies" :key="co.id" :value="co.id">{{ co.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Branch *</label>
            <select v-model="newEmp.branch" required>
                <option value="" disabled>Select Branch</option>
                <option v-for="br in branches" :key="br.id" :value="br.id">{{ br.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Department *</label>
            <select v-model="newEmp.department" required>
                <option value="" disabled>Select Department</option>
                <option v-for="dept in departments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Designation *</label>
            <select v-model="newEmp.designation" required>
              <option value="" disabled>Select Designation</option>
              <option v-for="des in designations" :key="des.id" :value="des.id">{{ des.name }}</option>
            </select>
          </div>
        </div>

        <div class="modal-actions">
          <button type="button" class="btn btn-secondary" @click="isModalOpen = false">Cancel</button>
          <button type="submit" class="btn btn-primary" :disabled="isLoading">
             {{ isLoading ? 'Saving...' : 'Save Employee' }}
          </button>
        </div>
      </form>
    </div>

    <div v-if="isDeleteModalOpen" class="modal-content confirm-modal shadow-lg">
      <div class="confirm-icon-wrapper">
        <span class="warning-icon">⚠️</span>
      </div>
      <h2 class="confirm-title">Confirm Deletion</h2>
      <p class="confirm-message" v-if="itemToDelete">
        Are you sure you want to delete <strong>{{ itemToDelete.first_name }} {{ itemToDelete.last_name }}</strong>?
      </p>
      <p class="confirm-message" v-else>
        Are you sure you want to delete <strong>{{ selectedIds.length }}</strong> selected employees?
      </p>
      <p class="warning-subtext">This action is permanent and cannot be undone.</p>
      <div class="modal-actions full-width">
        <button class="btn btn-secondary" @click="isDeleteModalOpen = false">Cancel</button>
        <button class="btn btn-danger" @click="executeDelete" :disabled="isLoading">
          {{ isLoading ? 'Deleting...' : 'Delete Permanently' }}
        </button>
      </div>
    </div>

  </div>
</Teleport>
</template>

<script setup>
import { useEmployees } from './useEmployees';
import './Employees.css';

// Inside <script setup>
const {
  searchQuery, handleSearch, currentTab, isLoading, tabs,
  filteredEmployees, pagination, fetchEmployees,
  isModalOpen, isBulkOpen, isEditing, toggleBulk,
  handleAddEmployee, handleEditEmployee, submitEmployee,
  newEmp, companies, branches, departments, designations,
  sortConfig, handleSort,
  selectedIds, toggleSelectAll, toggleSelect, handleBulkAction,
  isDeleteModalOpen, itemToDelete, confirmDelete, confirmBulkDelete, executeDelete
} = useEmployees();

// --- FORMATTERS ---

const formatImageUrl = (url) => {
  if (!url || url.includes('default-avatar.png')) { 
    return null; // This forces the initials to show instead of a broken image
  }
  
  if (url.startsWith('/media/')) {
    return `http://127.0.0.1:8002${url}`;
  }
  return url;
};

const props = defineProps({
  user: Object,
  dashboardData: Object
});

const emit = defineEmits(['refreshUser']);

// Add this to your script to handle images that exist but are broken links
const handleImageError = (e) => {
  e.target.style.display = 'none'; // Hide the broken img element
  e.target.nextSibling.style.display = 'block'; // Show the initials span
};

const formatDate = (date) => date ? new Date(date).toLocaleDateString() : '---';

const getInitials = (emp) => {
  if (!emp) return "??"; // Placeholder if the employee data hasn't loaded yet
  
  const first = (emp.first_name || "").trim().charAt(0);
  const last = (emp.last_name || "").trim().charAt(0);
  
  const initials = (first + last).toUpperCase();
  return initials || "Unknown"; // Default to 'U' for Unknown
};

const getCompanyColor = (companyId) => {
  // DEBUG: Check what is being passed in
  console.log(`[Color Debug] Received ID: ${companyId}, Type: ${typeof companyId}`);

  if (!companies.value || companies.value.length === 0) {
    console.warn("[Color Debug] Companies list is empty or not loaded yet.");
    return '#444444'; 
  }

  const companyObj = companies.value.find(c => Number(c.id) === Number(companyId));
  
  // If we can't find the company, we hash the ID itself so it's still dynamic
  const stringToHash = companyObj ? companyObj.name : `Company-${companyId}`;
  
  console.log(`[Color Debug] Hashing string: "${stringToHash}"`);

  let hash = 0;
  for (let i = 0; i < stringToHash.length; i++) {
    hash = stringToHash.charCodeAt(i) + ((hash << 5) - hash);
  }

  const hue = Math.abs(hash) % 360;
  const finalColor = `hsl(${hue}, 75%, 60%)`;
  
  console.log(`[Color Debug] Final Output: ${finalColor}`);
  return finalColor;
};

</script>