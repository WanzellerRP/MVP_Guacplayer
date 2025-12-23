<template>
  <div class="min-h-screen gradient-caixa flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Card de Login -->
      <div class="bg-white rounded-lg shadow-2xl p-8">
        <!-- Logo -->
        <div class="text-center mb-8">
          <div class="w-16 h-16 bg-caixa-primary rounded-lg flex items-center justify-center mx-auto mb-4">
            <span class="text-white text-3xl font-bold">G</span>
          </div>
          <h1 class="text-3xl font-bold text-caixa-primary mb-2">GuacPlayer</h1>
          <p class="text-gray-600">CAIXA Econômica Federal</p>
        </div>

        <!-- Formulário -->
        <form @submit.prevent="handleLogin" class="space-y-4">
          <!-- Username -->
          <div>
            <label for="username" class="block text-sm font-semibold text-gray-700 mb-2">
              Usuário
            </label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              class="input-field"
              placeholder="Digite seu usuário"
              required
            />
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-semibold text-gray-700 mb-2">
              Senha
            </label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              class="input-field"
              placeholder="Digite sua senha"
              required
            />
          </div>

          <!-- Error Message -->
          <div v-if="authStore.error" class="alert alert-error">
            {{ authStore.error }}
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="authStore.isLoading"
            class="w-full btn-primary py-3 font-semibold"
          >
            <span v-if="authStore.isLoading" class="spinner mr-2"></span>
            {{ authStore.isLoading ? 'Autenticando...' : 'Entrar' }}
          </button>
        </form>

        <!-- Footer -->
        <div class="mt-6 text-center text-sm text-gray-600">
          <p>Versão 1.0.0</p>
          <p class="mt-2">© 2025 CAIXA Econômica Federal</p>
        </div>
      </div>

      <!-- Informações -->
      <div class="mt-8 text-center text-white">
        <p class="text-sm">Use suas credenciais do Guacamole para acessar</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  password: ''
})

async function handleLogin() {
  try {
    await authStore.login(form.username, form.password)
    router.push('/dashboard')
  } catch (error) {
    // Erro já é tratado pelo store
    console.error('Erro ao fazer login:', error)
  }
}
</script>

<style scoped>
.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
