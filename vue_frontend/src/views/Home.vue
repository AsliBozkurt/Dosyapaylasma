<template>
  <header>
    <div class="container-fluid">
      <div class="border-bottom pt-6">
        <div class="row align-items-center">
          <div class="col-sm col-12"><h1 class="h2 ls-tight">Dosya Paylaş</h1></div>
          <div class="col-sm-auto col-12 mt-4 mt-sm-0">
            <div class="hstack gap-2 justify-content-sm-end">
              <a
                href="javascript:void('0')"
                class="btn btn-sm btn-primary"
                @click="openuploadModal()"
                ><span class="pe-2"><i class="bi bi-plus-square-dotted"></i> </span
                ><span>Dosya Ekle</span></a
              >
            </div>
          </div>
        </div>
        &nbsp;
      </div>
    </div>
  </header>

  <div class="container-fluid mt-3">
    <div class="vstack gap-4">
      <div class="row mb-3 mt-3">
        <div class="col-sm-4">
          <span v-if="is_size_loading">
            <Skeletor height="25px" width="160px" />
          </span>
          <span v-else>
            Boyut : {{ formatBytes(user_size) }} / {{ formatBytes(storage_size) }}</span
          >
        </div>
        <div class="col-sm-8">
          <div class="progress" style="height: 20px" v-if="is_size_loading">
            <div
              class="progress-bar bg-primary"
              role="progressbar"
              style="0"
              aria-valuenow="0"
              aria-valuemin="0"
              aria-valuemax="100"
            ></div>
          </div>
          <div class="progress" style="height: 20px" v-else>
            <div
              class="progress-bar bg-primary"
              role="progressbar"
              :style="'width:' + use_size(storage_size, user_size) + '%'"
              :aria-valuenow="use_size(storage_size, user_size)"
              aria-valuemin="0"
              aria-valuemax="100"
            >
              {{ use_size(storage_size, user_size) }} %
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header border-bottom d-flex align-items-center">
          <h5 class="me-auto">Dosyalarım</h5>
        </div>
        <div class="table-responsive">
          <table class="table table-hover table-nowrap">
            <thead class="table-light">
              <tr>
                <th scope="col">İsim</th>
                <th scope="col">Depolama Türü</th>
                <th scope="col"></th>
                <th scope="col">Dosya Soyadı</th>
                <th scope="col">Boyut</th>
              </tr>
            </thead>
            <tbody v-if="is_page_loading">
              <tr>
                <td><Skeletor width="100" pill /></td>
                <td><Skeletor width="100" pill /></td>
                <td><Skeletor width="100" pill /></td>
                <td><Skeletor width="100" pill /></td>
                <td><Skeletor width="100" pill /></td>
              </tr>
            </tbody>
            <tbody v-if="!is_loading">
              <tr v-if="data.count == 0">
                <td colspan="5" class="text-center">
                  <h6 class="h4 font-semibold mt-5 mb-2">Paylaştığınız bir dosya yok</h6>

                  <p class="mt-3">Bir dosya yüklediğinizde burada göreceksiniz</p>
                  <a
                    href="javascript:void('0')"
                    class="btn btn-sm btn-primary mt-3"
                    @click="openuploadModal()"
                    ><span class="pe-2"><i class="bi bi-plus-square-dotted"></i> </span
                    ><span>Dosya Ekle</span></a
                  >
                </td>
              </tr>

              <tr v-for="(item, index) in data.results" v-bind:key="index">
                <td>
                  {{ item.name }}
                </td>
                <td>
                  <span class="badge bg-success" v-if="item.storage_type === 'public'"
                    >Herkese Açık</span
                  >
                  <span class="badge bg-danger" v-else>Özel</span>
                </td>
                <td>
                  <!-- download -->
                  <span v-if="item.storage_type === 'public'">
                    <a
                      :href="item.file_public"
                      class="btn btn-sm btn-secondary d-block d-md-inline-block ms-auto ms-md-0 me-2"
                      target="_blank"
                      ><i class="bi bi-cloud-arrow-down-fill me-1"></i>Download</a
                    >
                  </span>

                  <span v-else>
                    <a
                      :href="item.file_private"
                      class="btn btn-sm btn-secondary d-block d-md-inline-block ms-auto ms-md-0 me-2"
                      target="_blank"
                      ><i class="bi bi-cloud-arrow-down-fill me-1"></i>Download</a
                    >
                  </span>
                  <!-- Copy -->
                  <span v-if="item.storage_type === 'public'">
                    <a
                      href="javascript:void('0')"
                      @click="urlGoster(item.file_public)"
                      class="btn btn-sm btn-warning d-block d-md-inline-block ms-auto ms-md-0"
                    >
                      <i class="bi bi-clipboard-check me-1"></i>Url Göster</a
                    >
                  </span>
                  <span v-else>
                    <a
                      href="javascript:void('0')"
                      @click="urlGoster(item.file_private)"
                      class="btn btn-sm btn-warning d-block d-md-inline-block ms-auto ms-md-0"
                    >
                      <i class="bi bi-clipboard-check me-1"></i>Url Göster</a
                    >
                  </span>
                  <button
                    href="javascript:void('0')"
                    class="btn btn-sm btn-danger ms-2"
                    @click="deleteData(item.id)"
                    v-if="!is_delete_loading"
                  >
                    <i class="bi bi-trash-fill"></i>
                  </button>
                  <button
                    class="btn btn-danger btn-sm"
                    type="button"
                    disabled
                    v-if="is_delete_loading"
                  >
                    <span
                      class="spinner-border spinner-border-sm"
                      role="status"
                      aria-hidden="true"
                    ></span>
                    <span class="visually-hidden">Loading...</span>
                  </button>
                </td>
                <td>{{ item.file_type }}</td>
                <td>{{ formatBytes(item.size) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="card-footer border-0 py-5"></div>
      </div>
    </div>
  </div>

  <!-- modalCreate  -->
  <div
    class="modal fade"
    id="uploadModal"
    tabindex="-1"
    aria-labelledby="uploadModal"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered modal-md">
      <div class="modal-content shadow-3">
        <div class="modal-header justify-content-start">
          <div>
            <h5 class="mb-1">Dosya Ekle</h5>
          </div>
        </div>
        <div class="modal-body py-0">
          <div class="form-group mt-3">
            <input
              type="email"
              class="form-control form-control-sm"
              v-model="name"
              placeholder="Başlık"
            />
            <small class="form-text text-primary text-sm">
              Daha sonra hatırlamak için bir kaç kelime birşey yazın.
            </small>
          </div>
          <div class="form-group mt-3">
            <div class="input-group file-browser form-control-sm">
              <input
                type="text"
                class="form-control browse-file form-control-sm"
                :placeholder="file_name"
                readonly=""
              />
              <label class="input-group-btn">
                <span class="btn btn-default">
                  Dosya
                  <input
                    type="file"
                    style="display: none"
                    multiple=""
                    v-on:change="handleFileUpload()"
                    id="file"
                    ref="file"
                  />
                </span>
              </label>
            </div>
            <small class="form-text text-primary text-sm">
              Maksimum 1 mb e kadar dosya kabul edilir.
            </small>
          </div>

          <div class="form-group mt-3">
            <div class="form-check">
              <input
                class="form-check-input"
                name="radio"
                type="radio"
                id="public"
                value="public"
                v-model="storage_type"
              />
              <label class="form-check-label" for="public"> Herkese Açık </label>
            </div>
            <div class="form-check">
              <input
                class="form-check-input"
                type="radio"
                id="private"
                value="private"
                v-model="storage_type"
              />
              <label class="form-check-label" for="private"> Özel </label>
            </div>

            <small class="form-text text-primary text-sm mb-3">
              Herkese Açık erişim izni verdiğinizde, dünyadaki herkes bu nesneye
              erişebilir. Özel erişim izni verdiğinizde, süresi dolana kadar herkes
              önceden belirlenmiş URL ile nesneye erişebilir.
            </small>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-sm btn-neutral" data-bs-dismiss="modal">
            Kapat
          </button>

          <button
            type="submit"
            class="btn btn-sm btn-primary"
            :disabled="v$.$invalid"
            @click="submitForm()"
            v-if="!is_modal_loading"
          >
            Yükle
          </button>
          <button
            class="btn btn-sm btn-primary"
            type="button"
            v-if="is_modal_loading"
            disabled
          >
            <span
              class="spinner-border spinner-border-sm"
              role="status"
              aria-hidden="true"
            ></span>
            Lütfen bekleyin
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- modalUrlGöster  -->
  <div
    class="modal fade"
    id="urlGoster"
    tabindex="-1"
    aria-labelledby="urlGoster"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered modal-md">
      <div class="modal-content shadow-3">
        <div class="modal-header justify-content-start">
          <div>
            <h5 class="mb-1">Url Göster</h5>
          </div>
        </div>
        <div class="modal-body py-0 text-sm">
          <p class="text-sm lh-relaxed mb-4">
            <code>{{ url }}</code>
          </p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-sm btn-neutral" data-bs-dismiss="modal">
            Kapat
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from "vue-toastification";
import useVuelidate from "@vuelidate/core";
import { required, maxLength } from "@vuelidate/validators";

export default {
  setup() {
    const toast = useToast();
    return { v$: useVuelidate(), toast };
  },
  name: "app",
  data() {
    return {
      is_data_loading: false,
      is_size_loading: false,
      storage_size: "",
      user_size: "",
      file: "",
      file_name: "Choose",
      name: "",
      search_name: "",
      storage_type: "public",
      is_modal_loading: false,
      is_page_loading: false,
      is_delete_loading: false,
      url: "",
      form: {
        name: "",
      },
      send_date_date: "",
      data: {
        count: 1,
      },
      refresh_data: 1,
    };
  },
  validations: {
    name: { required, maxLength: maxLength(100) },
    file: { required },
    storage_type: { required },
  },
  components: {},
  created() {
    this.$watch(
      () => this.$route.params,
      (toParams) => {
        this.locale = toParams.lang;
        this.getData();
        this.getSize();
      }
    );
  },
  watch: {
    refresh_data: function () {
      this.getData();
      this.getSize();
    },
  },
  methods: {
    getData() {
      this.is_page_loading = true;

      this.axios
        .get(`v1/file-manager-filter/?ordering=-1`)
        .then((response) => {
          this.data = response.data;
        })
        .catch(() => {
          this.toast.error("Hata");
        })
        .finally(() => {
          this.is_page_loading = false;
        });
    },
    getSize() {
      this.is_size_loading = true;
      this.axios
        .get(`v1/file-manager-size/`)
        .then((response) => {
          this.storage_size = response.data.storage_size;
          this.user_size = response.data.user_size;
        })
        .catch(() => {})
        .finally(() => {
          this.is_size_loading = false;
        });
    },
    submitForm() {
      this.is_modal_loading = true;

      let formData = new FormData();
      if (this.storage_type == "public") {
        formData.append("file_public", this.file);
      } else {
        formData.append("file_private", this.file);
      }
      formData.append("storage_type", this.storage_type);
      formData.append("name", this.name);

      this.axios
        .post("v1/file-manager", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then(() => {
          $("#uploadModal").modal("hide");
          this.toast.success("Dosya eklendi");
          this.getData();
          this.getSize();
        })
        .catch((error) => {
          console.log(error);
          this.toast.error("Hata. Dosya boyutu fazla");
        })
        .finally(() => {
          this.is_modal_loading = false;
        });
    },

    formatBytes(bytes, decimals = 2) {
      if (!+bytes) return "0 Bytes";

      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];

      const i = Math.floor(Math.log(bytes) / Math.log(k));

      return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
    },
    use_size(storage_size, user_size) {
      var percent = (user_size / storage_size) * 100;

      var decimals = 2;
      const dm = decimals < 0 ? 0 : decimals;

      return percent.toFixed(dm);
    },
    openuploadModal() {
      $("#uploadModal").modal("show");
      this.file_name = "Choose";
      this.file = "";
      this.name = "";
    },
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
      this.file_name = this.file["name"];
      this.storage_type = "public";
    },
    deleteData(id) {
      this.is_delete_loading = true;
      this.axios
        .delete(`v1/file-manager/${id}`)
        .then(() => {
          this.toast.success("Silindi");
          this.getData();
          this.getSize();
        })
        .catch(() => {
          this.toast.error("Hata");
        })
        .finally(() => {
          this.is_delete_loading = false;
        });
    },
    urlGoster(url) {
      $("#urlGoster").modal("show");
      this.url = url;
    },
  },
};
</script>
