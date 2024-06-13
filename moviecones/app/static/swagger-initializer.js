window.onload = function() {
  const ui = SwaggerUIBundle({
    url: "/static/swagger.yaml",
    dom_id: '#swagger-ui',
    deepLinking: true,
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ],
    plugins: [
      SwaggerUIBundle.plugins.DownloadUrl
    ],
    layout: "StandaloneLayout",
    requestInterceptor: (request) => {
      const token = localStorage.getItem('jwt_token');
      if (token) {
        request.headers['Authorization'] = 'Bearer ' + token;
      }
      return request;
    },
    responseInterceptor: (response) => {
      if (response.status === 200 && response.body.access_token) {
        localStorage.setItem('jwt_token', response.body.access_token);
      }
      return response;
    }
  });

  window.ui = ui;
}
