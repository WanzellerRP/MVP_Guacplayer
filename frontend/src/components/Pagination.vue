<template>
  <div class="flex items-center justify-between gap-4 mt-6">
    <!-- Informações de Paginação -->
    <div class="text-sm text-gray-600">
      Mostrando
      <span class="font-semibold">{{ startItem }}</span>
      a
      <span class="font-semibold">{{ endItem }}</span>
      de
      <span class="font-semibold">{{ pagination.total }}</span>
      itens
    </div>

    <!-- Botões de Navegação -->
    <div class="flex items-center gap-2">
      <button
        @click="goToPrevious"
        :disabled="pagination.page === 1"
        class="px-3 py-2 border border-caixa-border rounded-lg hover:bg-caixa-light disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        ← Anterior
      </button>

      <!-- Números de Página -->
      <div class="flex gap-1">
        <button
          v-for="page in visiblePages"
          :key="page"
          @click="goToPage(page)"
          :class="{
            'bg-caixa-primary text-white': page === pagination.page,
            'border border-caixa-border hover:bg-caixa-light': page !== pagination.page
          }"
          class="px-3 py-2 rounded-lg transition-colors"
        >
          {{ page }}
        </button>
      </div>

      <button
        @click="goToNext"
        :disabled="pagination.page === pagination.total_pages"
        class="px-3 py-2 border border-caixa-border rounded-lg hover:bg-caixa-light disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        Próxima →
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  pagination: {
    type: Object,
    required: true,
    validator: (obj) => {
      return 'page' in obj && 'per_page' in obj && 'total' in obj && 'total_pages' in obj
    }
  }
})

const emit = defineEmits(['page-change'])

// Computed
const startItem = computed(() => {
  return (props.pagination.page - 1) * props.pagination.per_page + 1
})

const endItem = computed(() => {
  return Math.min(props.pagination.page * props.pagination.per_page, props.pagination.total)
})

const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 5
  const totalPages = props.pagination.total_pages
  const currentPage = props.pagination.page

  let startPage = Math.max(1, currentPage - Math.floor(maxVisible / 2))
  let endPage = Math.min(totalPages, startPage + maxVisible - 1)

  if (endPage - startPage < maxVisible - 1) {
    startPage = Math.max(1, endPage - maxVisible + 1)
  }

  for (let i = startPage; i <= endPage; i++) {
    pages.push(i)
  }

  return pages
})

// Métodos
function goToPage(page) {
  emit('page-change', page)
}

function goToPrevious() {
  if (props.pagination.page > 1) {
    emit('page-change', props.pagination.page - 1)
  }
}

function goToNext() {
  if (props.pagination.page < props.pagination.total_pages) {
    emit('page-change', props.pagination.page + 1)
  }
}
</script>
