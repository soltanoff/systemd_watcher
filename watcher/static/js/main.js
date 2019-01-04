new Vue({
  el: '#app',
  delimiters: ['${','}'],
  data: {
    loading: false,
    preview: false,
    message: null,
    failedServicesData: '',
    services: [],
  },
  mounted: function() {
    this.getServices();
  },
  methods: {
    getServices: function() {
      this.$http.get(`/api/v1/services/`)
          .then((response) => {
            this.services = response.data;
          })
          .catch((err) => {
            console.log(err);
          })
    },
    showFailedServices: function() {
      this.$http.get(`/api/v1/services/failed/`)
          .then((response) => {
            this.failedServicesData = response.data;
            $("#showFailedServices").modal('show');
          })
          .catch((err) => {
            console.log(err);
          })
    }
  }
});
