def get_cart(session):
    return session.get('cart', {})


def add_to_cart(session, product_id):
    cart = session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    session['cart'] = cart
    session.modified = True