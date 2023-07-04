document.getElementById("applicationForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent the form from submitting normally

  var formData = new FormData(this);

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "php/form.php"); // Specify the server-side script URL
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        showThankYouMessage();
      } else {
        showErrorMessage();
      }
    }
  };
  xhr.send(formData);
});

function showThankYouMessage() {
  document.getElementById("applicationForm").style.display = "none";
  document.getElementById("thankYouMessage").style.display = "block";
}

function showErrorMessage() {
  document.getElementById("applicationForm").style.display = "none";
  document.getElementById("errorMessage").style.display = "block";
}

