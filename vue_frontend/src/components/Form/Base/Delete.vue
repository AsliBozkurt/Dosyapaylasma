<template>
  <div class="mt-3">
    <input
      class="form-control form-control-sm"
      type="text"
      @input="inputHandler"
      v-bind="$attrs"
      :value="$attrs.modelValue"
    />
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
  },
  methods: {
    inputHandler(e) {
      const target = e.target; //e.target as HTMLInputElement;
      this.$emit("update:modelValue", target.value);
      //   console.log(Event, HTMLInputElement)
    },
  },
  data() {
    return {};
  },
});
</script>

<style>
</style>
