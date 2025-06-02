
$(document).ready(function () {
    const $messagesContainer = $('.messages-container');

    // Функция для показа сообщений (глобально доступная)
    window.showMessage = function (text, type = 'success') {
        const messageClass = `message message-${type}`;
        const messageEl = $(`
            <div class="${messageClass}">
                <span class="message-text">${text}</span>
                <button class="message-close">&times;</button>
            </div>
        `);

        $messagesContainer.append(messageEl);
        setTimeout(() => {
            messageEl.fadeOut(500, () => messageEl.remove());
        }, 3000);
    };

    // Обработка статических сообщений (из Django)
    $('.message').each(function () {
        const $msg = $(this);
        setTimeout(() => {
            $msg.fadeOut(500, () => $msg.remove());
        }, 3000);
    });

    // Обработчик закрытия сообщений (работает для всех типов)
    $(document).on('click', '.message-close', function () {
        $(this).closest('.message').fadeOut(300, function () {
            $(this).remove();
        });
    });
});
