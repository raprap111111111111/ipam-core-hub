<template>
  <div class="profile-page">
    <div class="page-header">
    </div>

    <div class="layout">
      <!-- Left sidebar -->
      <div class="sidebar">
        <!-- Avatar + identity card -->
        <div class="card avatar-card">
          <div class="avatar-section">
            <div class="avatar-ring" @click="triggerFileInput" title="Change photo">
              <img
                v-if="form.avatarPreview || user?.profile_photo"
                :src="form.avatarPreview || user?.profile_photo"
                alt="Avatar"
                class="avatar-img"
              />
              <div v-else class="avatar-initials">{{ userInitials }}</div>
              <div class="avatar-overlay"><span>Change</span></div>
            </div>
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              style="display: none"
              @change="handleImageUpload"
            />

            <div class="avatar-name">{{ fullName || 'Your Name' }}</div>
            <span class="role-badge">{{ user?.roles?.join(', ') || 'superadmin' }}</span>
          </div>

          <div v-if="form.avatarFile" class="save-photo-row">
            <button class="btn btn-ghost btn-sm" @click="cancelPhotoChange">Cancel</button>
            <button class="btn btn-primary btn-sm" :disabled="loading" @click="updateAvatarOnly">
              {{ loading ? 'Saving…' : 'Save photo' }}
            </button>
          </div>

          <hr class="divider" />

          <div class="meta-block">
            <div class="meta-label">Email</div>
            <div class="meta-value">{{ form.email || '—' }}</div>
          </div>
          <div class="meta-block">
            <div class="meta-label">Member since</div>
            <div class="meta-value">{{ memberSince }}</div>
          </div>
        </div>

        <!-- Password card -->
        <div class="card pw-card">
          <button class="pw-trigger" @click="showPasswordModal = true">
            <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" width="15" height="15">
              <rect x="4" y="9" width="12" height="9" rx="2" />
              <path d="M7 9V6a3 3 0 016 0v3" />
            </svg>
            Change password
          </button>
        </div>
      </div>

      <!-- Main form card -->
      <div class="card form-card">
        <h2 class="form-title">Personal information</h2>

        <div class="form-grid">
          <div class="form-group">
            <label for="fname">First name</label>
            <input id="fname" v-model="form.first_name" type="text" placeholder="First name" />
          </div>
          <div class="form-group">
            <label for="mname">Middle name</label>
            <input id="mname" v-model="form.middle_name" type="text" placeholder="Optional" />
          </div>
          <div class="form-group">
            <label for="lname">Last name</label>
            <input id="lname" v-model="form.last_name" type="text" placeholder="Last name" />
          </div>
          <div class="form-group">
            <label for="phone">Phone number</label>
            <input id="phone" v-model="form.phone_number" type="tel" placeholder="+1 (555) 000-0000" />
          </div>
          <div class="form-group full">
            <label for="email">Email address</label>
            <input id="email" v-model="form.email" type="email" readonly class="readonly" />
            <span class="field-hint">Email cannot be changed here.</span>
          </div>
        </div>

        <div class="form-actions">
          <button class="btn btn-ghost" @click="resetForm">Cancel</button>
          <button class="btn btn-primary" :disabled="loading" @click="updateProfile">
            {{ loading ? 'Saving…' : 'Save changes' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Password Modal -->
    <Transition name="fade">
      <div v-if="showPasswordModal" class="modal-bg" @click.self="showPasswordModal = false">
        <div class="modal">
          <div class="modal-header">
            <h2>Change password</h2>
            <button class="close-btn" @click="showPasswordModal = false">&times;</button>
          </div>

          <div class="form-group">
            <label for="oldPw">Current password</label>
            <input id="oldPw" v-model="passwordForm.old_password" type="password" placeholder="Enter current password" />
          </div>

          <hr class="divider" style="margin: 1rem 0 0.75rem" />

          <div class="form-group">
            <label for="newPw">New password</label>
            <input
              id="newPw"
              v-model="passwordForm.new_password"
              type="password"
              placeholder="Min. 8 characters"
            />
            <div class="pw-strength-track">
              <div
                class="pw-strength-bar"
                :style="{ width: passwordStrengthPercent + '%', background: passwordStrengthColor }"
              ></div>
            </div>
            <span class="field-hint">{{ passwordStrengthLabel }}</span>
          </div>

          <div class="form-group">
            <label for="confPw">Confirm new password</label>
            <input
              id="confPw"
              v-model="passwordForm.confirm_password"
              type="password"
              placeholder="Repeat new password"
            />
            <span
              v-if="passwordForm.confirm_password"
              class="field-hint"
              :class="passwordsMatch ? 'hint-ok' : 'hint-err'"
            >
              {{ passwordsMatch ? 'Passwords match' : 'Passwords do not match' }}
            </span>
          </div>

          <div class="form-actions" style="margin-top: 1rem">
            <button class="btn btn-ghost" @click="showPasswordModal = false">Cancel</button>
            <button class="btn btn-primary" :disabled="loading" @click="handlePasswordChange">
              {{ loading ? 'Updating…' : 'Update password' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Toast -->
    <Transition name="toast">
      <div v-if="toast.visible" class="toast" :class="'toast-' + toast.type">
        {{ toast.message }}
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { useProfile } from './useProfile.js';

const {
  user,
  form,
  passwordForm,
  loading,
  toast,
  userInitials,
  fullName,
  memberSince,
  passwordStrengthPercent,
  passwordStrengthColor,
  passwordStrengthLabel,
  passwordsMatch,
  fileInput,
  triggerFileInput,
  handleImageUpload,
  updateAvatarOnly,
  cancelPhotoChange,
  updateProfile,
  resetForm,
  showPasswordModal,
  handlePasswordChange,
} = useProfile();
</script>

<style scoped src="./Profile.css"></style>