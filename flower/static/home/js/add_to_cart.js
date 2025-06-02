let addToCartQueue = Promise.resolve();
const cartOperationLocks = new Set();

$(document).on('click', '.add-to-cart-btn', function() {
    const $btn = $(this);
    const productId = $btn.data('product-id');
    const url = $btn.data('url');
    const csrfToken = $('meta[name="csrf-token"]').attr('content');
    

    if (cartOperationLocks.has(productId)) return;
    cartOperationLocks.add(productId);
    

    const originalHtml = $btn.html();
    $btn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i>');
    
    addToCartQueue = addToCartQueue.then(async () => {
        try {
            const response = await new Promise((resolve, reject) => {
                $.ajax({
                    url: url,
                    method: 'POST',
                    data: {
                        product_id: productId,
                        csrfmiddlewaretoken: csrfToken
                    },
                    success: resolve,
                    error: (xhr, status, error) => {
                        const err = new Error(error);
                        err.status = xhr.status;
                        reject(err);
                    }
                });
            });
            
            if (response.success) {
                updateCartData(response);
                showMessage('Product added to cart');
            } else {
                throw new Error(response.error || 'Error adding to cart');
            }
        } catch (error) {
            if (error.status === 403) {
                showMessage('Please login to add items to cart');
            } else {
                console.error('AJAX Error:', error);
                showMessage(error.message || 'An error occurred. Please try again.');
            }
        } finally {
            $btn.prop('disabled', false).html(originalHtml);
            cartOperationLocks.delete(productId);
        }
    });
});


function updateCartData(response) {
    $('#cart-total-items').text(response.total_items);
    $(`#cart-item-${response.product_id}`).text(response.quantity);
    
    for (const [productId, quantity] of Object.entries(response.cart_items)) {
        $(`#cart-item-${productId}`).text(quantity);
    }
}