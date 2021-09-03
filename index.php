composer require vlucas/phpdotenv //https://github.com/vlucas/phpdotenv
composer require eleirbag89/telegrambotphp //https://github.com/Eleirbag89/TelegramBotPHP

include (__DIR__ . '/vendor/autoload.php');

$telegram = new Telegram('TELEGRAM_TOKEN');
$dbhost = 'DB_HOST'
$dbname = 'DB_NAME'
$dbuser = 'DB_USER'
$dbpassword = 'DB_PASSWORD'

$dbh = new PDO('mysql:host=$dbhost;dbname=test', $user, $pass);