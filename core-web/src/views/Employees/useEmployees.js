import { ref, computed, onMounted, watch } from 'vue';
import { getEmployees, createEmployee, updateEmployee, deleteEmployees } from "../../services/employees";
import api from "../../services/api";
import { useToast } from "vue-toastification";

export function useEmployees() {
  const toast = useToast();
  
  // State
  const employees = ref([]);
  const searchQuery = ref("");
  const currentTab = ref("All");
  const isLoading = ref(false);
  const pagination = ref({ current: 1, totalPages: 1 });
  const tabs = ['All', 'Active', 'Probationary', 'On Leave', 'Offboarded'];
  
  const isModalOpen = ref(false);
  const isBulkOpen = ref(false);
  const isEditing = ref(false);
  const editingId = ref(null);
  const selectedIds = ref([]);

  // Metadata
  const companies = ref([]);
  const allBranches = ref([]);
  const allDepartments = ref([]);
  const designations = ref([]);

  const sortConfig = ref({ key: 'first_name', direction: 'asc' });

  const fetchAllMetadata = async () => {
    try {
      const res = await api.get('/employees/metadata/');
      const d = res.data.data;
      companies.value = d.companies || [];
      allBranches.value = d.branches || [];
      allDepartments.value = d.departments || [];
      designations.value = d.designations || [];
    } catch (err) {
      console.error("Error loading metadata:", err);
    }
  };

  const generateId = () => `EMP-${Math.random().toString(36).substr(2, 9).toUpperCase()}`;

  const newEmp = ref({
    employee_id: generateId(),
    first_name: '',
    last_name: '',
    hired_at: new Date().toISOString().substr(0, 10),
    company: '', branch: '', department: '', designation: '',
    tax_id: '', sss_no: '', is_active: true
  });

  const resetForm = () => {
    newEmp.value = {
      employee_id: generateId(), // Your helper function
      first_name: '',
      last_name: '',
      hired_at: new Date().toISOString().substr(0, 10),
      company: '', 
      branch: '', 
      department: '', 
      designation: '',
      tax_id: '', 
      sss_no: '', 
      is_active: true
    };
    isEditing.value = false;
    editingId.value = null;
  };

  // Logic Functions
  const fetchEmployees = async (page = 1) => {
    isLoading.value = true;
    try {
      const params = {
        page,
        search: searchQuery.value,
        order_by: sortConfig.value.key,
        order_dir: sortConfig.value.direction,
        status: currentTab.value !== 'All' ? currentTab.value : null
      };
      const response = await getEmployees(params);
      const d = response.data.data;
      employees.value = d.records || [];
      pagination.value = { current: d.current_page, totalPages: d.last_page };
      selectedIds.value = []; // Clear selection on page change
    } catch (err) {
      console.error("Fetch error:", err);
    } finally {
      isLoading.value = false;
    }
  };

  const submitEmployee = async () => {
    try {
      isLoading.value = true;
      if (isEditing.value) {
        await updateEmployee(editingId.value, newEmp.value);
        toast.success("Employee updated!");
      } else {
        await createEmployee(newEmp.value);
        toast.success("Employee created!");
      }
      isModalOpen.value = false;
      resetForm();
      fetchEmployees(pagination.value.current);
    } catch (err) {
      toast.error(err.response?.data?.message || "Error saving employee");
    } finally {
      isLoading.value = false;
    }
  };

  const handleEditEmployee = (emp) => {
    isEditing.value = true;
    editingId.value = emp.id;
    newEmp.value = { ...emp };
    isModalOpen.value = true;
  };

  const toggleSelectAll = (event) => {
    selectedIds.value = event.target.checked ? employees.value.map(e => e.id) : [];
  };

  const toggleSelect = (id) => {
    const idx = selectedIds.value.indexOf(id);
    idx > -1 ? selectedIds.value.splice(idx, 1) : selectedIds.value.push(id);
  };

 const handleBulkAction = async (action) => {
  if (selectedIds.value.length === 0) return toast.info("No employees selected");
  
  if (action === 'delete') {
    // We now use confirmBulkDelete() for this, but if called, redirect:
    confirmBulkDelete();
  } else if (action === 'status') {
    // Keep your status change logic here
    toast.info("Status change logic goes here");
  }
  isBulkOpen.value = false;
};

  const handleSort = (key) => {
    sortConfig.value.direction = (sortConfig.value.key === key && sortConfig.value.direction === 'asc') ? 'desc' : 'asc';
    sortConfig.value.key = key;
    fetchEmployees(1);
  };

  // Computed
  const availableBranches = computed(() => allBranches.value.filter(b => b.company_id === newEmp.value.company));
  const availableDepartments = computed(() => allDepartments.value.filter(d => d.branch_id === newEmp.value.branch));
  const filteredEmployees = computed(() => employees.value);

  const isDeleteModalOpen = ref(false);
const itemToDelete = ref(null);

// Open the modal for a single employee
const confirmDelete = (emp) => {
  itemToDelete.value = emp;
  isDeleteModalOpen.value = true;
};

// Open the modal for bulk selection
// 1. Update confirmBulkDelete to close the dropdown automatically
const confirmBulkDelete = () => {
  if (selectedIds.value.length === 0) return toast.info("No employees selected");
  itemToDelete.value = null; // Ensure we aren't targeting a single person
  isDeleteModalOpen.value = true;
  isBulkOpen.value = false; // Close the dropdown menu
};

const executeDelete = async () => {
  try {
    isLoading.value = true;
    if (itemToDelete.value) {
      // Single Delete
      await api.delete(`/employees/${itemToDelete.value.id}/`);
    } else {
      // Bulk Delete
      await deleteEmployees(selectedIds.value);
    }
    toast.success("Successfully removed.");
    fetchEmployees(pagination.value.current);
    selectedIds.value = [];
  } catch (err) {
    toast.error("Deletion failed.");
  } finally {
    isDeleteModalOpen.value = false;
    itemToDelete.value = null;
    isLoading.value = false;
  }
};

  watch(currentTab, () => fetchEmployees(1));
  onMounted(() => { fetchEmployees(); fetchAllMetadata(); });

  return {
    employees, 
    searchQuery, 
    currentTab, 
    isLoading, 
    tabs, 
    pagination, 
    filteredEmployees,
    companies, 
    branches: availableBranches, 
    departments: availableDepartments, 
    designations,
    isModalOpen, 
    isBulkOpen, 
    isEditing, 
    selectedIds, 
    newEmp, 
    sortConfig,
    fetchEmployees, 
    submitEmployee, 
    handleEditEmployee, 
    handleSort, 
    handleBulkAction,
    toggleSelectAll, 
    toggleSelect, 
    toggleBulk: () => isBulkOpen.value = !isBulkOpen.value,
    handleSearch: () => fetchEmployees(1),
    handleAddEmployee: () => { resetForm(); isModalOpen.value = true; },
    isDeleteModalOpen,
    itemToDelete, 
    confirmDelete, 
    confirmBulkDelete, 
    executeDelete
  };
}