<template>
  <div>
    <form class="vstack gap-5">
      <div>
        <div class="d-flex align-items-center">
          <div
            class="spinner-border text-primary"
            role="status"
            v-if="is_loading"
          >
            <span class="visually-hidden">Loading...</span>
          </div>
          <a
            href="#"
            class="avatar avatar-lg bg-warning rounded-circle text-white"
            v-if="!is_loading"
          >
            <img :src="data.avatar" />
          </a>
          <div class="ms-5">
            <label for="file-upload" class="btn btn-sm btn-neutral">
              <span
                >Upload
                <span
                  class="spinner-border text-primary spinner-border-sm ms-1"
                  role="status"
                  aria-hidden="true"
                  v-if="is_submit_loading"
                ></span
              ></span>
              <input
                type="file"
                @change="onFileSelected"
                name="file-upload"
                id="file-upload"
                class="visually-hidden"
              />
            </label>
            <a
              href="#"
              class="btn d-inline-flex btn-sm btn-neutral ms-2 text-danger"
              @click="setDelete()"
            >
              <span class="pe-2">
                <i class="bi bi-trash"></i>
              </span>
              <span>{{ $t("Delete") }}</span>
            </a>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { useToast } from "vue-toastification";

export default {
  setup() {
    const toast = useToast();
    return {
      toast,
    };
  },
  name: "app",
  data() {
    return {
      locale: null,
      data: [],
      is_loading: false,
      is_submit_loading: false,
      avatar: "",
    };
  },

  components: {},
  watch: {},
  created() {
    // this.$watch(
    //   () => this.$route.params,
    //   (toParams) => {
    //     this.$i18n.locale = toParams.lang;
    //     this.locale = toParams.lang;
    //   }
    // );
    this.getData();
  },
  methods: {
    onFileSelected(event) {
      this.avatar = event.target.files[0];
      this.submit();
      console.log(this.avatar);
    },
    getData() {
      this.is_loading = true;

      this.axios
        .get(`/v1/users/users-profile-avatar`)
        .then((response) => {
          this.data = response.data;
        })
        .catch(() => {})
        .finally(() => {
          this.is_loading = false;
        });
    },
    submit() {

      console.log("selam burdayım")

      this.is_submit_loading = true;
      let avatar = new FormData();
      avatar.append("avatar", this.avatar);

      this.axios
        .patch(`/v1/users/users-profile-avatar`, avatar, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then(() => {
          this.getData();
          this.toast.success(this.$t("Successfully Saved"));
        })
        .catch((error) => {
          console.log(error.response.data);
        })
        .finally(() => {
          this.is_submit_loading = false;
        });
    },
    setDelete() {
      this.axios
        .delete(`/v1/users/users-profile-avatar`)
        .then(() => {
          this.getData();
          this.toast.success(this.$t("Successfully Saved"));
        })
        .catch((error) => {
          console.log(error.response.data);
        })
        .finally(() => {});
    },
  },
};
</script>

<style>
</style>
