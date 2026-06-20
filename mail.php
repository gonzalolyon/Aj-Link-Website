<?php
/**
 * Contact form handler for Hostway (PHP mail).
 * On Netlify (*.netlify.app), forms use Netlify Forms via data-netlify instead.
 */

$to      = 'alejandro@ajlink.com';
$subject = 'Contact Form Message - AJ Link Website';

function get_return_page($return_to) {
    return ($return_to === 'contactos') ? 'contactos.html' : 'contact.html';
}

function redirect_form($return_to, $params) {
    $page = get_return_page($return_to);
    header('Location: ' . $page . '?' . http_build_query($params) . '#contactos');
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: contact.html');
    exit;
}

$return_to = isset($_POST['return_to']) ? $_POST['return_to'] : 'contact';
if (!in_array($return_to, array('contact', 'contactos'), true)) {
    $return_to = 'contact';
}

if (!empty($_POST['website'])) {
    redirect_form($return_to, array('enviado' => '1'));
}

function clean_header($value) {
    return trim(str_replace(array("\r", "\n", "%0a", "%0d", "%0A", "%0D"), '', $value));
}

$name    = isset($_POST['name'])    ? trim($_POST['name'])    : '';
$email   = isset($_POST['email'])   ? trim($_POST['email'])   : '';
$message = isset($_POST['message']) ? trim($_POST['message']) : '';

$error_code = '';

if ($name === '' || $email === '' || $message === '') {
    $error_code = 'campos';
} elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $error_code = 'email';
} elseif (strlen($message) > 5000) {
    $error_code = 'largo';
}

if ($error_code !== '') {
    redirect_form($return_to, array('error' => $error_code));
}

$safe_name  = clean_header($name);
$safe_email = clean_header($email);

$body  = "New message from ajlink.com contact form\n\n";
$body .= "Name: $name\n";
$body .= "E-mail: $safe_email\n\n";
$body .= "Message:\n$message\n";

$headers  = "From: AJ Link Web <alejandro@ajlink.com>\r\n";
$headers .= "Reply-To: $safe_name <$safe_email>\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "X-Mailer: PHP/" . phpversion() . "\r\n";

if (mail($to, $subject, $body, $headers)) {
    redirect_form($return_to, array('enviado' => '1'));
}

redirect_form($return_to, array('error' => 'envio'));
?>
