<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
  // Retrieve form data
  $category = $_POST["category"];
  $years = $_POST["years"];

  // Process the form data and send an email
  // Replace this code with your actual email sending logic
  $to = "info.sankofainnovationsfund@gmail.com";
  $subject = "Funding Application Submission";
  $message = "Category: " . $category . "\n";
  $message .= "Years in Business: " . $years . "\n";
  // Include other form data in the email message as needed

  $mailSent = mail($to, $subject, $message);

  // Return a response to the JavaScript code
  if ($mailSent) {
    http_response_code(200);
    echo "success";
  } else {
    http_response_code(500);
    echo "error";
  }
}
?>

