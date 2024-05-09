let cartItems = [];

function addToCart(id, name, price, img) {
  const existingItem = cartItems.find(item => item.id === id);

  if (existingItem) {
    existingItem.quantity++;
  } else {
    cartItems.push({ id, name, price, quantity: 1, img });
  }

  updateCart();
}

function updateCart() {
    const cartCountElement = document.getElementById('cart-count');
  const cartElement = document.getElementById('cart-items');
  const totalElement = document.getElementById('cart-total');

  cartElement.innerHTML = '';

  let total = 0;
  let totalQuantity = 0;

  cartItems.forEach(item => {
    const itemElement = document.createElement('div');
    itemElement.innerHTML = `
      <div class="cart-item">
        <img src="${item.img}" alt="${item.name}">
        <p> ${item.name}</p>
        <p> $${item.price.toFixed(2)}</p>
        <p>x${item.quantity}</p>
        <div class="btn-remove">
            <button onclick="removeFromCart('${item.id}')"><i class="fa-solid fa-xmark"></i></button>
        </div>
      </div>
    `;
    cartElement.appendChild(itemElement);

    total += item.price * item.quantity;
    totalQuantity += item.quantity;
  });

  totalElement.textContent = total.toFixed(2);
  cartCountElement.textContent = totalQuantity;
}

function removeFromCart(id) {
  const index = cartItems.findIndex(item => item.id === id);

  if (index !== -1) {
    if (cartItems[index].quantity > 1) {
      cartItems[index].quantity--;
    } else {
      cartItems.splice(index, 1);
    }

    updateCart();
  }
}

function toggleCart() {
  const cartElement = document.getElementById('cart');
  cartElement.style.display = (cartElement.style.display === 'none' || cartElement.style.display === '') ? 'block' : 'none';
}
