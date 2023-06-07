new Vue({
  delimiters: ['[[', ']]'],
  el: '#app',
  data: {
    inputData: '',
    jsonData: null,
    files: '',
  },
  mounted() {
    this.getFiles();
  },
  methods: {
    getFiles() {
      fetch('/api/files', {
        method: 'GET',
      })
        .then((response) => response.json())
        .then((data) => {
          // Handle the response data
          this.files = data['files'];
        })
        .catch((error) => {
          // Handle any errors
          console.error(error);
        });
    },

    submitForm() {
      // Make the API request
      const formData = new FormData();
      formData.append('search', this.inputData);
      fetch('/api/search', {
        method: 'POST',
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          // Handle the response data
          this.jsonData = data;
        })
        .catch((error) => {
          // Handle any errors
          console.error(error);
        })
        .finally(() => this.getFiles());
    },
  },
});
