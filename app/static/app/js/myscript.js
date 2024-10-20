$(document).ready(function(){
    $('.plus-cart').click(function(){
        var id = $(this).data("pid");

        $.ajax({
            url: "/pluscart/",
            data: {
                prod_id: id
            },
            success: function(data){
                $('span.cart-quantity[data-product-id="' + id + '"]').text(data.quantity);
                $('#amount').text('Rs.' + data.amount);
                $('#totalamount').text('Rs.' + data.totalamount);
            },
            error: function(xhr, status, error) {
                console.error("An error occurred:", error);
            }
        });
    });

    $('.minus-cart').click(function(){
        var id = $(this).data("pid");

        $.ajax({
            url: "/minuscart/",
            data: {
                prod_id: id
            },
            success: function(data){
                if (data.quantity === 0) {
                    // If quantity is zero, remove the item row from the DOM
                    $('span.cart-quantity[data-product-id="' + id + '"]').closest('.row').remove();
                } else {
                    $('span.cart-quantity[data-product-id="' + id + '"]').text(data.quantity);
                }
                $('#amount').text('Rs.' + data.amount);
                $('#totalamount').text('Rs.' + data.totalamount);
            },
            error: function(xhr, status, error) {
                console.error("An error occurred:", error);
            }
        });
    });

    $('.remove-cart').click(function(){
        var id = $(this).data("pid");

        $.ajax({
            url: "/removecart/",
            data: {
                prod_id: id
            },
            success: function(data){
                $('span.cart-quantity[data-product-id="' + id + '"]').closest('.row').remove();
                $('#amount').text('Rs.' + data.amount);
                $('#totalamount').text('Rs.' + data.totalamount);
            },
            error: function(xhr, status, error) {
                console.error("An error occurred:", error);
            }
        });
    });
});




document.querySelectorAll('.remove-button').forEach(button => {
    button.addEventListener('click', function() {
        const productId = this.dataset.productId;
        fetch(`/remove-from-cart/${productId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ 'product_id': productId })
        })
        .then(response => response.json())
        .then(data => {
            // Update UI based on response
        });
    });
});
