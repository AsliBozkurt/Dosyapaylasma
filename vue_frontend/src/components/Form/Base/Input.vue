<template>
  <div>
    <label class="form-label"
      >{{ label }}<span class="ms-1 text-danger" v-if="required">*</span></label
    >
    <input
      type="text"
      class="form-control form-control-sm"
      :placeholder="label"
      @input="inputHandler"
      v-bind="$attrs"
      :value="$attrs.modelValue"
    />
    {{ error }}
    <div class="invalid-feedback2">
      <span v-for="(error, index) in errors" :key="`error-${label}-${index}`">
        {{ error.$message }}
      </span>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";
export default defineComponent({
  name: "TitleInput",
  props: {
    label: {
      type: String,
      default: null,
    },
    errors: {
      type: Array,
      default: () => [],
    },
    isValidData: {
      type: Boolean,
      default: false,
    },
    required: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    inputHandler(e) {
      const target = e.target; //e.target as HTMLInputElement;
      this.$emit("update:modelValue", target.value);
    },
  },
});
</script>

<style></style>
