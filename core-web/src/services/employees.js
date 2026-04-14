import api from "./api";

/**
 * Fetch the list of all employees
 */
export const getEmployees = (params) => {
    return api.get('/employees/', { params }); 
};

/**
 * Create a new employee record
 */
export const createEmployee = async (employeeData) => {
  const response = await api.post("/employees/", employeeData);
  return response.data;
};

/**
 * Update an existing employee record
 */
export const updateEmployee = async (id, employeeData) => {
  const response = await api.put(`/employees/${id}/`, employeeData);
  return response.data;
};

/**
 * Delete a single employee record
 */
export const deleteEmployee = async (id) => {
  const response = await api.delete(`/employees/${id}/`);
  return response.data;
};

/**
 * Bulk delete multiple employee records
 * This matches the import in your useEmployees.js
 */
export const deleteEmployees = async (ids) => {
  // Ensure your backend endpoint can handle a list of IDs via POST or DELETE
  const response = await api.post('/employees/bulk-delete/', { ids });
  return response.data;
};

export const getOrgMetadata = (params = {}) => {
  return api.get('/employees/metadata/', { params });
};