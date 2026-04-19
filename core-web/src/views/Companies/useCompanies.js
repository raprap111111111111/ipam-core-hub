import { ref, computed, onMounted, watch } from 'vue';
import { useToast } from "vue-toastification";
import { 
  getCompanies, 
  createCompany, 
  updateCompany, 
  deleteCompany, 
  deleteCompanies 
} from "../../services/companies";

export function useCompanies() {
  const toast = useToast();

  // State
  const companies = ref([]);
  const searchQuery = ref("");
  const currentTab = ref("All");
  const isLoading = ref(false);
  const pagination = ref({ current: 1, totalPages: 1 });
  const tabs = ['All', 'Active', 'Inactive'];
  
  const isModalOpen = ref(false);
  const isBulkOpen = ref(false);
  const isEditing = ref(false);
  const editingId = ref(null);
  const selectedIds = ref([]);
  const isDeleteModalOpen = ref(false);
  const itemToDelete = ref(null);
  const sortConfig = ref({ key: 'name', direction: 'asc' });

  // Logo Upload State
  const logoPreview = ref(null);
  const selectedFile = ref(null);

  const newCompany = ref({
    name: '',
    registration_number: '',
    address: '',
    website: '',
    code: '',
    is_active: true,
  });

  // Methods
  const handleLogoUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      selectedFile.value = file;
      logoPreview.value = URL.createObjectURL(file);
    }
  };

  const clearLogoPreview = () => {
    logoPreview.value = null;
    selectedFile.value = null;
    const input = document.getElementById('logo-upload');
    if (input) input.value = '';
  };

  const resetForm = () => {
    newCompany.value = {
      name: '',
      registration_number: '',
      address: '',
      website: '',
      code: '',
      is_active: true,
    };
    isEditing.value = false;
    editingId.value = null;
    clearLogoPreview();
  };

  const fetchCompanies = async (page = 1) => {
    isLoading.value = true;
    try {
      const params = {
        page,
        search: searchQuery.value?.trim() || undefined,
        order_by: sortConfig.value.key,
        order_dir: sortConfig.value.direction,
        status: currentTab.value !== 'All' ? currentTab.value.toLowerCase() : undefined,
      };

      Object.keys(params).forEach(key => {
        if (params[key] === undefined) delete params[key];
      });

      const response = await getCompanies(params);
      const data = response.data.data || response.data;

      companies.value = data.records || data.results || [];
      pagination.value = {
        current: data.current_page || 1,
        totalPages: data.last_page || data.total_pages || 1
      };
    } catch (err) {
      console.error("Fetch error:", err);
      toast.error("Failed to load companies");
    } finally {
      isLoading.value = false;
    }
  };

 const submitCompany = async () => {
  try {
    isLoading.value = true;
    const formData = new FormData();
    
    // 1. Text Fields
    formData.append('name', newCompany.value.name);
    formData.append('registration_number', newCompany.value.registration_number || '');
    formData.append('address', newCompany.value.address || '');
    formData.append('website', newCompany.value.website || '');
    formData.append('code', newCompany.value.code || '');
    formData.append('is_active', newCompany.value.is_active ? 'true' : 'false');

    // 2. The File Logic (CRITICAL)
    if (selectedFile.value instanceof File) {
      // ONLY append if it is a new file picked from the computer
      formData.append('logo', selectedFile.value);
    } 
    // If it's not a file (meaning it's just the old URL), 
    // we DON'T append 'logo' at all. Django partial update will keep the old one.

    if (isEditing.value) {
      const res = await updateCompany(editingId.value, formData);
      
      // Handle your specific backend response structure
      if (res.success === false) {
        throw new Error(res.errors || res.message);
      }
      
      toast.success("Company updated successfully!");
    } else {
      await createCompany(formData);
      toast.success("Company created!");
    }

    isModalOpen.value = false;
    resetForm();
    fetchCompanies(pagination.value.current);
  } catch (err) {
    console.error("Save error:", err);
    // Drill down to the specific error detail
    const errorMsg = err.response?.data?.errors || err.message || "Save failed";
    toast.error(errorMsg);
  } finally {
    isLoading.value = false;
  }
};

  const handleEditCompany = (company) => {
    resetForm(); 
    isEditing.value = true;
    editingId.value = company.id;
    newCompany.value = { ...company };
    
    if (company.logo) {
      // Use dynamic base URL for the preview as well
      const baseURL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8002";
      
      logoPreview.value = company.logo.startsWith('http') 
        ? company.logo 
        : `${baseURL}${company.logo.startsWith('/') ? '' : '/'}${company.logo}`;
    }

    selectedFile.value = null;
    isModalOpen.value = true;
  };

  const handleAddCompany = () => {
    resetForm();
    isModalOpen.value = true;
  };

  const toggleSelectAll = (e) => {
    selectedIds.value = e.target.checked ? companies.value.map(c => c.id) : [];
  };

  const toggleSelect = (id) => {
    const idx = selectedIds.value.indexOf(id);
    idx > -1 ? selectedIds.value.splice(idx, 1) : selectedIds.value.push(id);
  };

  const executeDelete = async () => {
    try {
      isLoading.value = true;
      if (itemToDelete.value) {
        await deleteCompany(itemToDelete.value.id);
      } else {
        await deleteCompanies(selectedIds.value);
      }
      toast.success("Deleted successfully");
      fetchCompanies(pagination.value.current);
      selectedIds.value = [];
      isDeleteModalOpen.value = false;
    } catch (err) {
      toast.error("Delete failed");
    } finally {
      isLoading.value = false;
    }
  };

  const handleSort = (key) => {
    if (sortConfig.value.key === key) {
      sortConfig.value.direction = sortConfig.value.direction === 'asc' ? 'desc' : 'asc';
    } else {
      sortConfig.value.key = key;
      sortConfig.value.direction = 'asc';
    }
    fetchCompanies(1);
  };

  watch(currentTab, () => fetchCompanies(1));
  onMounted(() => fetchCompanies());

  return {
    companies, searchQuery, currentTab, tabs, isLoading, pagination,
    filteredCompanies: computed(() => companies.value),
    isModalOpen, isBulkOpen, isEditing, newCompany,
    sortConfig, selectedIds, isDeleteModalOpen, itemToDelete,
    logoPreview, handleLogoUpload, clearLogoPreview,
    fetchCompanies, submitCompany, handleAddCompany, handleEditCompany,
    handleSort, toggleSelectAll, toggleSelect,
    toggleBulk: () => isBulkOpen.value = !isBulkOpen.value,
    handleSearch: () => fetchCompanies(1),
    confirmDelete: (company) => { itemToDelete.value = company; isDeleteModalOpen.value = true; },
    confirmBulkDelete: () => { if (selectedIds.value.length > 0) isDeleteModalOpen.value = true; },
    executeDelete
  };
}