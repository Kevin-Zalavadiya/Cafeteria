function viewInvoice() {
    const totalPrice = document.getElementById('total-price').innerText;
    // Store the total price in localStorage so we can access it on the invoice page
    localStorage.setItem('invoiceTotal', totalPrice);
    // Redirect to the invoice page
    window.location.href = invoiceUrl;
}
