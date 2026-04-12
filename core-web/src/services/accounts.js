import api from "./api"; // Ensure this matches your api configuration file

export const updateProfile = async (profileData, imageFile) => {
  const formData = new FormData();

// ONLY append to formData if the value actually has content
  if (profileData.first_name) formData.append("first_name", profileData.first_name);
  if (profileData.middle_name) formData.append("middle_name", profileData.middle_name);
  if (profileData.last_name) formData.append("last_name", profileData.last_name);
  if (profileData.phone_number) formData.append("phone_number", profileData.phone_number);

  if (imageFile) {
    formData.append("profile_photo", imageFile); // 'avatar' matches your Django model field
  }

  // This override is correct!
  const response = await api.patch("/accounts/profile/update/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data;
};