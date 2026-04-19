<template>
    <div class="view-container">
        <div class="employees-container">
            <div class="workforce-card">
                <div class="card-header">
                    <div class="title-group">
                        <h1 class="main-title">Companies</h1>
                        <p class="sub-title">Core Hub Entities</p>
                    </div>
                    <div class="header-actions">
                        <button class="btn btn-primary" @click="handleAddCompany">+ Add Company</button>
                        <div class="dropdown-wrapper" style="position: relative;">
                            <button class="btn btn-secondary" @click="toggleBulk">Bulk Actions ⌄</button>
                            <div v-if="isBulkOpen" class="custom-dropdown-menu">
                                <button @click="confirmBulkDelete">Delete Selected</button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="table-controls">
                    <div class="search-wrapper">
                        <span class="search-icon">🔍</span>
                        <input type="text" v-model="searchQuery" placeholder="Search companies..." @keyup.enter="handleSearch" />
                        <button class="btn btn-primary search-btn" @click="handleSearch">Search</button>
                    </div>

                    <div class="filter-tabs">
                        <button v-for="tab in tabs" :key="tab" :class="['tab-btn', { active: currentTab === tab }]" @click="currentTab = tab">
                            {{ tab }}
                        </button>
                    </div>
                    <button class="btn btn-secondary">Export ⌄</button>
                </div>

                <table class="employee-table">
                    <thead>
                        <tr>
                            <th><input type="checkbox" @change="toggleSelectAll" :checked="selectedIds.length === filteredCompanies.length && filteredCompanies.length > 0" /></th>
                            <th>Logo</th>
                            <th @click="handleSort('name')" class="sortable-header">Company Name <span>{{ sortConfig.key === 'name' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : '' }}</span></th>
                            <th>Registration No.</th>
                            <th>Industry</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="isLoading && !companies.length">
                            <td colspan="7" style="text-align:center;padding:60px;">Loading...</td>
                        </tr>
                        <tr v-else v-for="comp in filteredCompanies" :key="comp.id">
                            <td><input type="checkbox" :checked="selectedIds.includes(comp.id)" @change="toggleSelect(comp.id)" /></td>
                            <td>
                                <div class="emp-avatar-container" style="width: 42px; height: 42px;">
                                    <div class="user-avatar" :style="{ backgroundColor: getCompanyColor(comp) }">
                                        <img v-if="comp.logo" :src="formatLogoUrl(comp.logo)" class="logo-img" alt="logo" @error="e => e.target.style.display = 'none'" />
                                        <span v-else class="initials-text">{{ getInitials(comp.name) }}</span>
                                    </div>
                                </div>
                            </td>
                            <td class="bold-text">{{ comp.name }}</td>
                            <td>{{ comp.registration_number || '—' }}</td>
                            <td>—</td>
                            <td><span :class="['status-badge', comp.is_active ? 'active' : '']">{{ comp.is_active ? 'Active' : 'Inactive' }}</span></td>
                            <td>
                                <div class="action-buttons">
                                    <button class="action-btn edit" @click="handleEditCompany(comp)">✏️</button>
                                    <button class="action-btn delete" @click="confirmDelete(comp)">🗑️</button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>

                <div class="pagination-footer" v-if="pagination.totalPages > 1">
                    <button class="page-btn" :disabled="pagination.current === 1" @click="fetchCompanies(pagination.current - 1)">Prev</button>
                    <span class="page-info">Page {{ pagination.current }} of {{ pagination.totalPages }}</span>
                    <button class="page-btn" :disabled="pagination.current === pagination.totalPages" @click="fetchCompanies(pagination.current + 1)">Next</button>
                </div>
            </div>
        </div>

        <Teleport to="body">
            <div v-if="isModalOpen || isDeleteModalOpen" class="modal-overlay" @click.self="isModalOpen = isDeleteModalOpen = false">
                <div v-if="isModalOpen" class="modal-content large-modal">
                    <div class="modal-header">
                        <h2>{{ isEditing ? 'Edit Company' : 'Add New Company' }}</h2>
                        <button class="close-x" @click="isModalOpen = false">&times;</button>
                    </div>

                    <form @submit.prevent="submitCompany">
                        <div class="form-grid">
                            <div class="form-group" style="grid-column: span 2; margin-bottom: 20px;">
                                <label>Company Logo</label>
                                <div class="file-upload-area">
                                    <input type="file" accept="image/*" @change="handleLogoUpload" id="logo-upload" class="file-input" />
                                    <label for="logo-upload" class="upload-label">📸 Click to upload company logo</label>
                                </div>
                                <div v-if="logoPreview" class="logo-preview">
                                    <img :src="logoPreview" alt="Preview" />
                                    <button type="button" @click="clearLogoPreview" class="remove-preview">×</button>
                                </div>
                            </div>

                            <div class="form-group">
                                <label>Company Name *</label>
                                <input type="text" v-model="newCompany.name" required />
                            </div>
                            <div class="form-group">
                                <label>Registration Number</label>
                                <input type="text" v-model="newCompany.registration_number" />
                            </div>
                            <div class="form-group">
                                <label>Code</label>
                                <input type="text" v-model="newCompany.code" />
                            </div>
                            <div class="form-group">
                                <label>Website</label>
                                <input type="url" v-model="newCompany.website" placeholder="https://..." />
                            </div>
                            <div class="form-group" style="grid-column: span 2;">
                                <label>Address</label>
                                <textarea v-model="newCompany.address" rows="3"></textarea>
                            </div>
                        </div>

                        <div class="modal-actions">
                            <button type="button" class="btn btn-secondary" @click="isModalOpen = false">Cancel</button>
                            <button type="submit" class="btn btn-primary" :disabled="isLoading">
                                {{ isLoading ? 'Saving...' : (isEditing ? 'Update Company' : 'Create Company') }}
                            </button>
                        </div>
                    </form>
                </div>

                <div v-if="isDeleteModalOpen" class="modal-content confirm-modal">
                    <div class="confirm-icon-wrapper">⚠️</div>
                    <h2 class="confirm-title">Confirm Deletion</h2>
                    <p v-if="itemToDelete">Delete <strong>{{ itemToDelete.name }}</strong>?</p>
                    <p v-else>Delete <strong>{{ selectedIds.length }}</strong> selected companies?</p>
                    <p class="warning-subtext">This action cannot be undone.</p>
                    <div class="modal-actions">
                        <button class="btn btn-secondary" @click="isDeleteModalOpen = false">Cancel</button>
                        <button class="btn btn-danger" @click="executeDelete" :disabled="isLoading">Delete Permanently</button>
                    </div>
                </div>
            </div>
        </Teleport>
    </div>
</template>

<script setup>
import { useCompanies } from './useCompanies';
import './Companies.css';

// Props/Emits to clear Vue warnings
const props = defineProps({
  user: Object,
  dashboardData: Object
});
defineEmits(['refreshUser']);

const {
    companies, searchQuery, currentTab, tabs, isLoading, pagination,
    filteredCompanies, isModalOpen, isBulkOpen, isEditing, newCompany,
    sortConfig, selectedIds, isDeleteModalOpen, itemToDelete,
    logoPreview, handleLogoUpload, clearLogoPreview,
    fetchCompanies, submitCompany, handleAddCompany, handleEditCompany,
    handleSort, toggleSelectAll, toggleSelect, toggleBulk, handleSearch,
    confirmDelete, confirmBulkDelete, executeDelete
} = useCompanies();

// Helper Functions
const getInitials = (name) => {
    if (!name) return '??';
    const words = name.trim().split(/\s+/);
    return words.length >= 2 ? (words[0][0] + words[1][0]).toUpperCase() : name.substring(0, 2).toUpperCase();
};

const getCompanyColor = (comp) => {
    if (!comp || !comp.name) return '#666666';
    const str = comp.name + (comp.id || '');
    let hash = 0;
    for (let i = 0; i < str.length; i++) hash = str.charCodeAt(i) + ((hash << 5) - hash);
    return `hsl(${Math.abs(hash) % 360}, 85%, 55%)`;
};

const formatLogoUrl = (logoPath) => {
    if (!logoPath) return null;
    
    // If it's already a full URL (common in production/S3), return as is
    if (logoPath.startsWith('http')) {
        return logoPath;
    }
    
    // Use the Env variable for the base URL
    const baseURL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8002";
    
    // Ensure there is a single slash between base and path
    const cleanPath = logoPath.startsWith('/') ? logoPath : `/${logoPath}`;
    return `${baseURL}${cleanPath}`;
};
</script>