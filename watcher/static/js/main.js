new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data: {
        loading: false,
        preview: false,

        pickedServices: 'active',

        message: null,
        serviceStatus: '',

        failedServices: [],
        favoriteServices: [],
        services: [],

        currentServiceLogs: '',
        search: '',
    },
    mounted: function() {
        this.pickedServices = 'active'
        this.getActiveServices();
    },
    watch: {
        pickedServices: function(value) {
            this.getServicesByPickedRadioButton(value);
        },
    },
    computed: {
        filteredServices: function() {
            search = this.search.trim().toUpperCase();
            if (this.search.length > 0)
                return this.services.filter(service => { return service.name.toUpperCase().includes(search) })
            else
                return this.services
        },
    },
    methods: {
        getServices: function() {
            this.loading = true;
            this.$http
                .get(`/api/v1/services/`)
                .then((response) => {
                    this.loading = false;
                    this.services = response.data.services;
                    this.favoriteServices = response.data.favorite_services;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        getActiveServices: function() {
            this.loading = true;
            this.$http
                .get(`/api/v1/services/active/`)
                .then((response) => {
                    this.loading = false;
                    this.services = response.data.services;
                    this.favoriteServices = response.data.favorite_services;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        getInactiveServices: function() {
            this.loading = true;
            this.$http
                .get(`/api/v1/services/inactive/`)
                .then((response) => {
                    this.loading = false;
                    this.services = response.data.services;
                    this.favoriteServices = response.data.favorite_services;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        getFavoriteServices: function() {
            this.loading = true;
            this.$http
                .get(`/api/v1/services/favorite/`)
                .then((response) => {
                    this.loading = false;
                    this.services = response.data;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        manageFavoriteServices: function(service) {
            this.$http
                .post(`/api/v1/service/manage_favorite/${service}/`)
                .then((response) => {
                    this.favoriteServices = response.data;
                })
                .catch((err) => {
                    console.log(err);
                })
        },
        getServicesByPickedRadioButton: function(value) {
            switch(value) {
                case 'active':
                    this.getActiveServices();
                    break;
                case 'inactive':
                    this.getInactiveServices();
                    break;
                case 'favorite':
                    this.getFavoriteServices();
                    break;
                default:
                    this.getServices();
                    break;
            }
        },
        showFailedServices: function() {
            this.$http
                .get(`/api/v1/services/failed/`)
                .then((response) => {
                    this.failedServices = response.data;
                    $("#showFailedServices").modal('show');
                })
                .catch((err) => {
                    console.log(err);
                })
        },
        showServiceLogs: function(service) {
            this.$http
                .get(`/api/v1/service/logs/${service}/`)
                .then((response) => {
                    this.currentServiceLogs = response.data;
                    $("#showServiceLogs").modal('show');
                })
                .catch((err) => {
                    console.log(err);
                    this.currentServiceLogs = '';
                })
        },
        startService: function(service) {
            this.loading = true;
            this.$http
                .post(`/api/v1/service/start/${service}/`)
                .then((response) => {
                    this.serviceStatus = "Service \"<b>" + service + "</b>\" started successful!";
                    this.getServicesByPickedRadioButton(this.pickedServices);
                    $("#showServiceStatus").modal('show');
                })
                .catch((err) => {
                    console.log(err);
                    this.serviceStatus = "Service \"<b>" + service + "</b>\" not started!<br>Error: " + err;
                    this.getServicesByPickedRadioButton(this.pickedServices);
                    $("#showServiceStatus").modal('show');
                })
        },
        restartService: function(service) {
            this.loading = true;
            this.$http
                .post(`/api/v1/service/restart/${service}/`)
                .then((response) => {
                    this.serviceStatus = "Service \"<b>" + service + "</b>\" restarted successful!";
                    this.getServicesByPickedRadioButton(this.pickedServices);
                    $("#showServiceStatus").modal('show');
                })
                .catch((err) => {
                    console.log(err);
                    this.serviceStatus = "Service \"<b>" + service + "</b>\" not restarted!<br>Error: " + err;
                    this.getServicesByPickedRadioButton(this.pickedServices);
                    $("#showServiceStatus").modal('show');
                })
        },
        stopService: function(service) {
            this.loading = true;
            this.$http
                .post(`/api/v1/service/stop/${service}/`)
                .then((response) => {
                    this.serviceStatus = "Service \"<b>" + service + "</b>\" stopped!";
                    this.getServicesByPickedRadioButton(this.pickedServices);
                    $("#showServiceStatus").modal('show');
                })
                .catch((err) => {
                    console.log(err);
                    this.serviceStatus = "Service \"<b>" + service + "</b>\" not stopped!<br>Error: " + err;
                    this.getServicesByPickedRadioButton(this.pickedServices);
                    $("#showServiceStatus").modal('show');
                })
        },
    }
});
