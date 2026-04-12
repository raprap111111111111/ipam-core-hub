// src/views/Profile/useProfile.js
import { ref, computed, onMounted } from 'vue';
import { getMe, changeUserPassword } from '../../services/auth.js';
import { updateProfile as updateProfileService } from '../../services/accounts.js';

export function useProfile() {
  const user = ref(null);
  const loading = ref(false);
  const showPasswordModal = ref(false);
  const fileInput = ref(null);
  
  // Feature Modal State
  const editModal = ref({ visible: false, target: '' });

  const toast = ref({ visible: false, message: '', type: 'success' });
  let toastTimer = null;

  const form = ref({
    first_name: '',
    middle_name: '',
    last_name: '',
    phone_number: '',
    email: '',
    avatarPreview: null,
    avatarFile: null,
  });

  const passwordForm = ref({
    old_password: '',
    new_password: '',
    confirm_password: '',
  });

  // ─── Computed Values ──────────────────────────────────────────────────────

  const userInitials = computed(() => {
    const first = form.value.first_name?.[0] || '';
    const last = form.value.last_name?.[0] || '';
    return (first + last).toUpperCase() || 'RA';
  });

  const fullName = computed(() =>
    [form.value.first_name, form.value.last_name].filter(Boolean).join(' ')
  );

  const memberSince = computed(() => {
    if (!user.value?.created_at) return '—';
    return new Date(user.value.created_at).toLocaleDateString('en-US', {
      month: 'long',
      year: 'numeric',
    });
  });

  // ─── Password Logic ───────────────────────────────────────────────────────

  const passwordStrengthScore = computed(() => {
    const v = passwordForm.value.new_password;
    if (!v) return 0;
    let score = 0;
    if (v.length >= 8) score++;
    if (/[A-Z]/.test(v)) score++;
    if (/[0-9]/.test(v)) score++;
    if (/[^A-Za-z0-9]/.test(v)) score++;
    return score;
  });

  const passwordStrengthPercent = computed(() => [0, 25, 50, 75, 100][passwordStrengthScore.value]);
  const passwordStrengthColor = computed(() => ['#e0e0e0', '#e24b4a', '#ef9f27', '#639922', '#1d9e75'][passwordStrengthScore.value]);
  const passwordStrengthLabel = computed(() => ['', 'Weak', 'Fair', 'Good', 'Strong'][passwordStrengthScore.value]);
  const passwordsMatch = computed(() => passwordForm.value.new_password === passwordForm.value.confirm_password);

  // ─── Actions ──────────────────────────────────────────────────────────────

  const showToast = (message, type = 'success') => {
    clearTimeout(toastTimer);
    toast.value = { visible: true, message, type };
    toastTimer = setTimeout(() => { toast.value.visible = false; }, 2800);
  };

  const loadUserData = async () => {
    try {
      user.value = await getMe();
      form.value.first_name = user.value.first_name || '';
      form.value.middle_name = user.value.middle_name || '';
      form.value.last_name = user.value.last_name || '';
      form.value.phone_number = user.value.phone_number || '';
      form.value.email = user.value.email || '';
      form.value.avatarPreview = user.value.profile_photo || null;
    } catch (err) {
      showToast('Failed to load profile', 'error');
    }
  };

  const triggerFileInput = () => fileInput.value?.click();

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    form.value.avatarFile = file;
    form.value.avatarPreview = URL.createObjectURL(file);
  };

  const updateProfile = async () => {
    loading.value = true;
    try {
      await updateProfileService(form.value, form.value.avatarFile);
      await loadUserData();
      showToast('Profile updated!');
    } catch {
      showToast('Update failed', 'error');
    } finally {
      loading.value = false;
    }
  };

  const openEditModal = (target) => {
    editModal.value.target = target;
    editModal.value.visible = true;
  };

  const saveAndClose = async () => {
    await updateProfile();
    editModal.value.visible = false;
  };

  onMounted(loadUserData);

  return {
    user, form, passwordForm, loading, toast, userInitials, fullName, memberSince,
    passwordStrengthPercent, passwordStrengthColor, passwordStrengthLabel, passwordsMatch,
    fileInput, triggerFileInput, handleImageUpload, updateProfile, showPasswordModal,
    editModal, openEditModal, saveAndClose
  };
}