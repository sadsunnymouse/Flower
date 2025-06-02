$(document).ready(function() {
    const csrfToken = $('meta[name="csrf-token"]').attr('content');
    const productsUrl = $('meta[name="products-url"]').attr('content');
    
    // Очередь операций
    let operationQueue = Promise.resolve();
    const operationLocks = new Set();
    
    // Общая функция AJAX-запросов
    function ajaxRequest(url, data) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: url,
                type: 'POST',
                headers: {'X-CSRFToken': csrfToken},
                data: data,
                success: resolve,
                error: xhr => {
                    const error = new Error(xhr.responseJSON?.error || 'Server error');
                    error.status = xhr.status;
                    reject(error);
                }
            });
        });
    }
    
    function enqueueOperation(itemId, operation) {
        if (operationLocks.has(itemId)) return Promise.resolve();
        
        operationLocks.add(itemId);
        return new Promise((resolve, reject) => {
            operationQueue = operationQueue
                .then(() => operation())
                .then(resolve)
                .catch(reject)
                .finally(() => operationLocks.delete(itemId));
        });
    }
    
    // Обработчик изменения количества
    $(document).on('change', '.quantity-input', function() {
        const $input = $(this);
        const itemId = $input.closest('.cart-item').data('item-id');
        const newQuantity = parseInt($input.val());
        const oldValue = $input.data('old-value');
        
        if (isNaN(newQuantity) || newQuantity < 1) {
            showMessage('Invalid quantity value', 'error');
            $input.val(oldValue);
            return;
        }
        
        enqueueOperation(itemId, async () => {
            $input.prop('disabled', true);
            
            try {
                const response = await ajaxRequest(`/cart/update/${itemId}/`, {
                    quantity: newQuantity
                });
                
                if (response.success) {
                    const $row = $(`.cart-item[data-item-id="${itemId}"]`);
                    $row.find('.product-total').text('$' + response.item_total);
                    $('.cart-summary .value').text('$' + response.cart_total);
                    $('#cart-total-items').text(response.total_items);
                    showMessage('Quantity updated successfully');
                } else {
                    throw new Error(response.error || 'Update failed');
                }
            } catch (error) {
                showMessage(`Error: ${error.message}`, 'error');
                $input.val(oldValue);
            } finally {
                $input.prop('disabled', false);
            }
        });
    }).on('focus', '.quantity-input', function() {
        $(this).data('old-value', $(this).val());
    });
    
    // Обработчик удаления товара
    $(document).on('click', '.remove-btn', function() {
        const $btn = $(this);
        const itemId = $btn.data('item-id');
        const $row = $btn.closest('.cart-item');
        
        enqueueOperation(itemId, async () => {
            $btn.prop('disabled', true);
            $btn.html('<i class="fas fa-spinner fa-spin"></i>');
            
            try {
                const response = await ajaxRequest(`/cart/remove/${itemId}/`, {});
                
                if (response.success) {
                    await new Promise(resolve => {
                        $row.fadeOut(300, () => {
                            $row.remove();
                            resolve();
                        });
                    });
                    
                    updateCartState(response);
                    showMessage('Product removed from cart');
                } else {
                    throw new Error(response.error || 'Remove failed');
                }
            } catch (error) {
                showMessage(`Error: ${error.message}`, 'error');
                $btn.prop('disabled', false);
                $btn.html('<i class="fas fa-trash"></i>');
            }
        });
    });
    
    // Обновление состояния корзины
    function updateCartState(response) {
        $('.cart-summary .value').text('$' + response.cart_total);
        $('#cart-total-items').text(response.total_items || 0);
        
        if ($('.cart-item').length === 0) {
            $('.cart-items').html(`
                <div class="empty-cart">
                    <p>Your cart is empty</p>
                    <a href="${productsUrl}" class="continue-shopping">Continue shopping</a>
                </div>
            `);
        }
    }
});