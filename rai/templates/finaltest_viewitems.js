function viewInvoice() {
  const totalPrice = document.getElementById('total-price').innerText;
  localStorage.setItem('totalPrice', totalPrice);
  
  // Collect all selected items with their quantities
  const selectedItems = [];
  const addButtons = document.querySelectorAll('.add-to-cart');
  
  addButtons.forEach(button => {
    const foodItem = button.closest('.food-item');
    const itemName = foodItem.querySelector('h3').innerText;
    const itemPriceText = foodItem.querySelector('p').innerText;
    const itemPrice = itemPriceText.replace('₹', '').trim();
    const quantityInput = foodItem.querySelector('input[type="number"]');
    
    if (quantityInput && parseInt(quantityInput.value) > 0) {
      selectedItems.push({
        name: itemName,
        price: itemPrice,
        quantity: parseInt(quantityInput.value)
      });
    }
  });
  
  // Store the selected items in localStorage
  localStorage.setItem('selectedItems', JSON.stringify(selectedItems));
  
  // Redirect to the invoice page
  window.location.href = "{% url 'invoice' %}";
}
