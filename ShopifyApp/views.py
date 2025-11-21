from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.views import View
from ShopifyApp.models import Category, Product, Cart, CartItem ,Order, OrderItem, Address
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddProductForm
from django.http import HttpResponse
from .models import Wishlist
from django.contrib import messages
from decimal import Decimal
from django.views.generic import ListView, DetailView






# -------------------------- HOME PAGE VIEW --------------------------
class HomePageView(View):

    def get(self, request):
        # Fetch all products
        products = Product.objects.all()
        return render(request, 'ShopifyApp/index.html', context={'products': products})


# -------------------------- CREATE PRODUCT VIEW --------------------------
class CreateProductView(LoginRequiredMixin, View):

    def get(self, request):
        # Render empty form for adding product
        context = {
            'form': AddProductForm()
        }
        return render(request, 'ShopifyApp/add-product.html', context)

    def post(self, request):
        try:
            form = AddProductForm(request.POST, request.FILES)

            if form.is_valid():
                # Save product object without committing immediately
                instance = form.save(commit=False)
                instance.user = request.user  # assign current logged in user

                # Calculate selling price
                selling_price = instance.original_price - (
                    instance.original_price * instance.discount_percentage / 100
                )
                instance.selling_price = selling_price

                # Save product in DB
                instance.save()

        except Exception as e:
            print(f'{type(e).__name__}: {e}')

        return redirect("app:home")


# -------------------------- CREATE CATEGORY VIEW --------------------------
class CreateCategoryView(LoginRequiredMixin, View):
    flag = False

    def get(self, request):
        # Show category form page
        return render(request, 'ShopifyApp/add-category.html')

    def post(self, request):
        flag = False
        try:
            # Get category name from form
            category_name = request.POST.get('cname')
            category = Category(name=category_name)

            # Save category
            category.save()
            print("product added successfully")
            flag = True

            return redirect('app:home')

        except Exception as e:
            flag = False
            print(f'{type(e).__name__}: {e}')

        return render(request, 'ShopifyApp/add-category.html', {'flag': flag})


# -------------------------- VIEW SINGLE PRODUCT --------------------------
class ViewProduct(View):

    def get(self, request, id):
        print(id)
        product = Product.objects.get(pk=id)

        return render(request, 'ShopifyApp/view-product.html', {"product": product})


# -------------------------- EDIT PRODUCT VIEW --------------------------
class EditProduct(LoginRequiredMixin, View):

    def get(self, request, id):
        # Fetch product to edit
        product = Product.objects.get(pk=id)
        return render(request, 'ShopifyApp/edit-product.html', {"product": product})

    def post(self, request, id):

        try:
            db_product = Product.objects.get(pk=id)

            # Clean numbers and calculate selling price
            original_price_user = eval(request.POST.get('oprice').replace(',', ''))
            discount_percentage_user = eval(request.POST.get('dprice').replace(',', ''))

            discount_price = original_price_user * discount_percentage_user / 100
            selling_price = original_price_user - discount_price

            # Update fields
            db_product.name = request.POST.get('pname')
            db_product.discription = request.POST.get('discription')
            db_product.original_price = original_price_user
            db_product.discount_percentage = discount_percentage_user
            db_product.selling_price = selling_price
            db_product.image = request.FILES.get('image')

            db_product.save()

            print("product updated successfully")
            return redirect('app:home')

        except Exception as e:
            print(f'{type(e).__name__}: {e}')

        return render(request, 'ShopifyApp/add-product.html')


# -------------------------- DELETE PRODUCT VIEW --------------------------
class DeleteProduct(LoginRequiredMixin, View):

    def get(self, request, id):
        print(id)
        product = Product.objects.get(pk=id)
        return render(request, 'ShopifyApp/delete-product.html', context={"product": product})

    def post(self, request, id):
        product = Product.objects.get(pk=id)
        product.delete()
        return redirect('app:home')


# -------------------------- SEARCH PRODUCT --------------------------
class SearchProduct(View):

    def post(self, request):
        search = request.POST.get('search')

        # Search by product name or category name
        search_list = Product.objects.filter(
            Q(name__icontains=search) | Q(category__name__icontains=search)
        )

        return render(request, 'ShopifyApp/search-product.html', {'search_list': search_list})


# -------------------------- FILTER PRODUCTS BY CATEGORY --------------------------
class CategoryProductView(View):

    def get(self, request, id=None):
        categories = Category.objects.all()

        if id:
            products = Product.objects.filter(category_id=id)
        else:
            products = Product.objects.all()

        return render(request, 'Shopifyapp/index.html', context={'products': products, 'categories': categories})


# -------------------------- GET PRODUCTS CREATED BY A SPECIFIC USER --------------------------
class GetProductByCreatedUser(View):

    def get(self, request, id):
        product_list = Product.objects.filter(user_id=id)
        return render(request, 'ShopifyApp/profile.html', context={'products': product_list})


# -------------------------- ADD PRODUCT TO CART --------------------------
class AddProductToCart(LoginRequiredMixin, View):

    def get(self, request, id):
        product = get_object_or_404(Product, id=id)

        # Get user's cart or create one
        user_cart, created = Cart.objects.get_or_create(user=request.user)

        # Add product or increase quantity
        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect("app:view-product", product.id)


# -------------------------- VIEW CART --------------------------
# class ViewCart(View):

#     def get(self, request):
#         user_cart = get_object_or_404(Cart, user=request.user)
#         cart_items = CartItem.objects.filter(cart=user_cart)

#         context = {
#             'cart': user_cart,
#             'cart_items': cart_items
#         }

#         return render(request, 'ShopifyApp/view-cart.html', context)
    




class ViewCart(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name = None

    def get(self, request):
        # Always get or create a cart for the logged-in user
        user_cart, created = Cart.objects.get_or_create(user=request.user)

        cart_items = CartItem.objects.filter(cart=user_cart)

        context = {
            'cart': user_cart,
            'cart_items': cart_items
        }
        return render(request, 'ShopifyApp/view-cart.html', context)



    


# ------------------ CART ADD (+) ------------------
class UpdateCartAdd(View):
    def get(self, request, item_id):

        product = get_object_or_404(Product, id=item_id)

        # Get or create user cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Get or create item in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        # Increase quantity
        cart_item.quantity += 1
        cart_item.save()

        return redirect("ShopifyApp:view-cart")


# ------------------ CART SUB (-) ------------------
class UpdateCartSub(View):
    def get(self, request, item_id):

        cart_item = get_object_or_404(CartItem, id=item_id)

        # decrease qty OR delete
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        return redirect("ShopifyApp:view-cart")


# ------------------ REMOVE ITEM ------------------
class RemoveCartItem(View):
    def get(self, request, item_id):

        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()

        return redirect("ShopifyApp:view-cart")


class AddToWishlist(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect("userapp:login")

        product = Product.objects.get(id=id)

        exists = Wishlist.objects.filter(user=request.user, product=product).exists()
        if exists:
            messages.info(request, "Product already in wishlist.")
        else:
            Wishlist.objects.create(user=request.user, product=product)
            messages.success(request, "Added to wishlist!")

        return redirect("app:view-product", id=id)

    

class ViewWishlist(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("userapp:login")

        wishlist = Wishlist.objects.filter(user=request.user)

        return render(request, "ShopifyApp/wishlist.html", {
            "wishlist": wishlist
        })

    

class RemoveWishlist(View):
    def get(self, request, id):
        Wishlist.objects.filter(id=id, user=request.user).delete()
        return redirect("app:view-wishlist")
    



class CheckoutView(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name = None

    def get(self, request):
        # get user cart & items
        user_cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=user_cart)

        # total calculation
        total = sum((item.product.selling_price * item.quantity) for item in cart_items)

        addresses = Address.objects.filter(user=request.user)

        return render(request, 'ShopifyApp/checkout.html', {
            'cart': user_cart,
            'cart_items': cart_items,
            'total': total,
            'addresses': addresses,
        })

    def post(self, request):
        # Handle posting a new address or selecting existing address
        address_id = request.POST.get('address_id')
        if address_id:
            address = get_object_or_404(Address, id=address_id, user=request.user)
        else:
            # Create new address from form fields
            address = Address.objects.create(
                user=request.user,
                full_name=request.POST.get('full_name'),
                phone=request.POST.get('phone'),
                line1=request.POST.get('line1'),
                line2=request.POST.get('line2', ''),
                city=request.POST.get('city'),
                state=request.POST.get('state', ''),
                postal_code=request.POST.get('postal_code'),
                country=request.POST.get('country', 'India'),
            )

        payment_method = request.POST.get('payment_method', 'COD')  # 'COD' or 'RAZORPAY'

        # load cart items and compute total
        user_cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=user_cart)
        if not cart_items.exists():
            return redirect('app:view-cart')

        total = sum((item.product.selling_price * item.quantity) for item in cart_items)
        total = Decimal(total).quantize(Decimal('0.01'))

        # create order with status pending
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=total,
            payment_method=payment_method,
            status='pending'
        )

        # create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.selling_price
            )

        # if COD -> clear cart and redirect to success
        if payment_method == 'COD':
            cart_items.delete()
            return redirect('app:order-success', order_id=order.id)

        # if Razorpay -> prepare razorpay order (you'll implement in Step 4)
        # store order.id in session and redirect to payment view which will create razorpay order
        request.session['pending_order_id'] = order.id
        return redirect('app:razorpay-pay', order_id=order.id)
    




class OrderListView(LoginRequiredMixin, ListView):
    login_url = '/user/login/'
    model = Order
    template_name = 'ShopifyApp/orders_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(LoginRequiredMixin, DetailView):
    login_url = '/user/login/'
    model = Order
    template_name = 'ShopifyApp/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    


class OrderSuccessView(LoginRequiredMixin, View):
    login_url = '/user/login/'
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        return render(request, 'ShopifyApp/order_success.html', {'order': order})




import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class RazorpayCreateOrderView(LoginRequiredMixin, View):
    login_url = '/user/login/'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        # create razorpay order only if not created before
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        amount_paise = int(order.total_price * 100)  # razorpay expects paise
        data = {
            "amount": amount_paise,
            "currency": "INR",
            "receipt": f"order_rcptid_{order.id}",
            "payment_capture": 1
        }
        razorpay_order = client.order.create(data=data)
        order.razorpay_order_id = razorpay_order.get('id')
        order.save()

        # send data to template to open Razorpay checkout
        context = {
            'order': order,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'razorpay_order_id': order.razorpay_order_id,
            'amount': amount_paise,
        }
        return render(request, 'ShopifyApp/razorpay_checkout.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class RazorpayVerifyView(View):
    # Razorpay will post payment success data to this view from client side.
    # Alternatively handle via server verification POST from client.
    def post(self, request):
        # expected keys in POST: razorpay_payment_id, razorpay_order_id, razorpay_signature, order_id (our order id)
        from django.http import JsonResponse
        payload = request.POST
        razorpay_payment_id = payload.get('razorpay_payment_id')
        razorpay_order_id = payload.get('razorpay_order_id')
        razorpay_signature = payload.get('razorpay_signature')
        our_order_id = payload.get('order_id')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            # verify signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
        except Exception as e:
            return JsonResponse({'status': 'fail', 'reason': str(e)}, status=400)

        # signature valid -> update order
        order = get_object_or_404(Order, id=our_order_id, razorpay_order_id=razorpay_order_id, user=request.user)
        order.status = 'paid'
        order.save()

        # clear cart
        cart = get_object_or_404(Cart, user=request.user)
        CartItem.objects.filter(cart=cart).delete()
        return JsonResponse({'status': 'ok'})




