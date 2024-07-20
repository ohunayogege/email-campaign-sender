
$(document).ready(function () {
  $("#toggle-password").on("click", function () {
    let passwordField = $("#password");
    let passwordFieldType = passwordField.attr("type");
    if (passwordFieldType === "password") {
      passwordField.attr("type", "text");
      $(this).find("i").removeClass("fa-eye").addClass("fa-eye-slash");
    } else {
      passwordField.attr("type", "password");
      $(this).find("i").removeClass("fa-eye-slash").addClass("fa-eye");
    }
  });
});