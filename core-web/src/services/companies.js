import api from "./api";

/**
 * Fetch the list of all companies
 */
export const getCompanies = async (params) => {
  const response = await api.get('/companies/', { params });
  return response.data;
};

/**
 * Create a new company record
 * Handles FormData (Logos) automatically
 */
export const createCompany = async (companyData) => {
  const response = await api.post("/companies/", companyData);
  return response.data;
};

/**
 * Update an existing company record
 * NOTE: We use PATCH instead of PUT/POST to support FormData 
 * and avoid "Method Not Allowed" errors.
 */
export const updateCompany = async (id, formData) => {
  const response = await api.put(`/companies/${id}/?logo`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }); 
  return response.data;
};

/**
 * Delete a single company record
 */
export const deleteCompany = async (id) => {
  const response = await api.delete(`/companies/${id}/`);
  return response.data;
};

/**
 * Bulk delete multiple company records
 */
export const deleteCompanies = async (ids) => {
  const response = await api.post('/companies/bulk-delete/', { ids });
  return response.data;
};

/**
 * Metadata for dropdowns
 */
export const getCompanyMetadata = async () => {
  const response = await api.get('/companies/metadata/');
  return response.data;
};