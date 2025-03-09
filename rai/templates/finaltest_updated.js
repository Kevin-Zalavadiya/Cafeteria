function viewInvoice() {
  const totalPrice = document.getElementById('total-price').innerText;
  localStorage.setItem('totalPrice', totalPrice);
  window.location.href = "{% url 'invoice' %}";
}
