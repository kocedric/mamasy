import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from store.forms import RegisterForm, RegisterFormUpdate, ClientForm
from store.models import *


# app_name = 'store'
def showProduit(request):
    produits = Product.objects.filter(available=True)
    paginator = Paginator(produits, 9)  # Show 9 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    page_name = 'home'
    dernier_produits = Product.objects.filter(available=True).order_by('-created_at')[:4]
    categories = Category.objects.all()[:6]
    # categories = Category.objects.filter(parent_category_id=None)[:6]
    list1 = categories[:3]
    list2 = categories[3:]
    mylist = zip(list1, list2)
    # posts = PostSocial.objects.order_by('-ajouter_le')[:3]
    contexts = {
        'dernier_produits': dernier_produits,
        'page_name': page_name,
        # 'categories': categories,
        'mylist': mylist
    }
    return render(request, template_name="store/index.html", context=contexts)


def inscription(request):
    page_name = 'inscription'

    form = RegisterForm()
    client_form = ClientForm()
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        client_form = ClientForm(request.POST, request.FILES)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            # Permet d'ajouter manuellement des infomations non contenu dans le formulaire
            client = client_form.save(commit=False)
            client.user = user
            client.save()
            # my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            # my_customer_group[0].user_set.add(user)

            # On connecte le client

            messages.success(request, f'Compte Créé avec Succès pour {user}')
            return redirect('store:sign_in')
    # form = RegisterForm()
    # client_form = ClientForm()
    # if request.method == 'POST':
    #     # if 'register' in request.POST:
    #     form = RegisterForm(request.POST)
    #     if form.is_valid():
    #         # On crée l'utilisateur et le client
    #         user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
    #                     first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
    #         user.set_password(form.cleaned_data['password'])
    #         user.save()
    #         client = Client(user_id=user.id)
    #         client.save()
    #
    #         messages.success(request, f'Compte Créé avec Succès pour {user}')
    #         return redirect('index')
    contexts = {'form': form, 'client_form': client_form, 'page_name': page_name}
    return render(request, 'store/sign_up.html', context=contexts)


def sign_in(request):
    page_name = 'connexion'
    form = RegisterForm()

    if request.method == 'POST':
        # if 'register' in request.POST:
        #     form = RegisterForm(request.POST)
        #     if form.is_valid():
        #         # On crée l'utilisateur et le client
        #         user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
        #                     first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
        #         user.set_password(form.cleaned_data['password'])
        #         user.save()
        #         client = Client(user_id=user.id)
        #         client.save()
        #
        #         # On connecte le client
        #         user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        #         __move_session_cart_to_database_cart(request, client.id)
        #         login(request, user)
        #
        #         if request.GET.get('next', False):
        #             return redirect(request.GET['next'])
        #         else:
        #             return redirect(reverse('store:index'))
        # else:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            # Verifie que l'utilisateur existe et qu'il n'est pas désactivé
            if user.is_active:
                client = Client.objects.filter(user_id=user.id).first()
                __move_session_cart_to_database_cart(request, client.id)
                login(request, user)
                if request.GET.get('next', False):
                    return redirect(request.GET['next'])
                else:
                    # return redirect(reverse('index'))
                    return redirect('index')
            else:
                messages.add_message(request, messages.ERROR,
                                     'Votre compte a été désactivé, veuillez-contacter le service client.')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Les identifiants que vous avez saisis sont incorrects !')

    contexts = {
        'get': request.GET,
        'form': form,
        'page_name': page_name
    }

    return render(request, 'store/login.html', context=contexts)


def sign_out(request):
    logout(request)
    # return redirect(reverse('index'))
    return redirect('index')


def __move_session_cart_to_database_cart(request, client_id):
    """
    Cette fonction permet de copier le panier stocké en session d'un utilisateur non identifé vers la base de données
    juste avant son identification et supprime ensuite le panier stocké en session.
    :param request: l'objet request transmis depuis la fonction parent pour accéder à la session courante
    :param client_id: l'id du client
    :return:
    """
    if 'cart' in request.session:
        for product_id, qty in request.session['cart'].items():
            if CartLine.objects.filter(product_id=product_id, client_id=client_id).exists():
                cart_line = CartLine.objects.get(product_id=product_id, client_id=client_id)
                cart_line.quantity += int(qty)
            else:
                cart_line = CartLine(product_id=product_id, client_id=client_id, quantity=qty)
            cart_line.save()
        del request.session['cart']
    return


def about(request):
    page_name = 'A propos'
    contexts = {'page_name': page_name}
    return render(request, 'store/about.html', context=contexts)


def boutique(request, category_id):
    """
        Cette fonction permet de visualiser les produits contenus dans une catégorie.
        :type request:
        :param request:
        :param category_id: Id de la catégorie à visualiser
        :return:
    """
    page_name = 'Boutique'  # Affiche ce nom comme titre

    try:
        categorie = Category.objects.get(pk=category_id)
        produit_all_categorie = categorie.products.filter(available=True)
        if produit_all_categorie.count() > 0:
            paginator = Paginator(produit_all_categorie, 9)  # Show 9 contacts per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
            page_obj = showProduit(request)
    except Category.DoesNotExist:
        page_obj = showProduit(request)

    categories = Category.objects.all()[:5]

    contexts = {'page_name': page_name, 'page_obj': page_obj, 'categories': categories}
    return render(request, 'store/shop.html', context=contexts)


def detail(request, product_id):
    page_name = 'Détail'  # Affiche ce nom comme titre
    product = get_object_or_404(Product, pk=product_id)
    # pictures = Photo.objects.filter(product__pk=product.id)

    dernier_produits = Product.objects.filter(available=True).order_by('-created_at')[:3]
    contexts = {
        'page_name': page_name,
        'produit_choisi': product,
        'dernier_produits': dernier_produits
    }
    return render(request, 'store/shop-detail.html', context=contexts)


def contact(request):
    page_name = 'Contact'  # Affiche ce nom comme titre
    contexts = {'page_name': page_name}
    return render(request, 'store/contact.html', context=contexts)


def __create_order_from_database_cart(request):
    """
    Cette fonction permet créer un objet Order et les objets OrderDetail associés à partir
    :param request:
    :return:
    """

    client = Client.objects.get(user_id=request.user.id)
    order = Order(status=Order.WAITING,
                  client_id=client.id,
                  shipping_address=request.session['shipping_address'].title(),
                  phone=request.session['phone'],
                  order_date=datetime.datetime.now()
                  )
    order.save()

    cart = CartLine.objects.filter(client_id=client.id)
    for cart_line in cart:
        order_detail = OrderDetail(order_id=order.id,
                                   product_id=cart_line.product_id,
                                   qty=cart_line.quantity,
                                   product_unit_price=cart_line.product.price,
                                   vat=cart_line.product.vat.percent
                                   )
        order_detail.save()

    cart.delete()

    return order


def add_to_cart(request, product_id, qty):
    """
    Cette fonction permet d'ajouter un produit au panier. Si l'utilisateur n'est pas connecté, le produit est ajouté
    dans un panier virtuel géré grâce au système de sessions ; sinon, il est persisté en BDD.
    :type request:
    :param request:
    :param product_id: Id du produit à ajouter au panier
    :param qty: Nombre d'exemplaire du produit à ajouter au panier
    :return:
    """
    if not request.user.is_authenticated:
        if 'cart' not in request.session:
            cart = dict()
        else:
            cart = request.session['cart']

        if product_id in cart:
            cart[product_id] = int(cart[product_id]) + int(qty)
        else:
            cart[product_id] = qty

        request.session['cart'] = cart
    else:
        client = Client.objects.get(user_id=request.user.id)
        if CartLine.objects.filter(product_id=product_id, client_id=client.id).exists():
            cart_line = CartLine.objects.get(product_id=product_id, client_id=client.id)
            cart_line.quantity += int(qty)
        else:
            cart_line = CartLine(product_id=product_id, client_id=client.id, quantity=qty)
        cart_line.save()

    if request.META.get('HTTP_REFERER'):
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(reverse('store:index'))


def clear_item_cart(request, product_id):
    """
    Cette fonction permet de supprimer un produit du panier. Si l'utilisateur n'est pas connecté, la fonction le fait dans le panier virtuel
    stocké en session ; sinon, les objets précédemment persistés en BDD sont supprimés.
    :param product_id: identifient du produit à supprimer
    :param request:
    :return:
    """
    if not request.user.is_authenticated and 'cart' in request.session:
        # del request.session['cart']
        carts = request.session['cart']
        if product_id in carts:
            del carts[product_id]
    else:
        client = Client.objects.get(user_id=request.user.id)
        CartLine.objects.filter(client_id=client.id, product_id=product_id).delete()

    return redirect(request.META.get('HTTP_REFERER'))


def clear_cart(request):
    """
    Cette fonction permet de vider le panier. Si l'utilisateur n'est pas connecté, la fonction vide le panier virtuel
    stocké en session ; sinon, les objets précédemment persistés en BDD sont supprimés.
    :param request:
    :return:
    """
    if not request.user.is_authenticated and 'cart' in request.session:
        del request.session['cart']
    else:
        client = Client.objects.get(user_id=request.user.id)
        CartLine.objects.filter(client_id=client.id).delete()

    return redirect(request.META.get('HTTP_REFERER'))


def display_cart(request):
    page_name = 'Panier'
    total = 0
    if not request.user.is_authenticated:
        if 'cart' in request.session:
            cart = list()
            for product_id, quantity in request.session.get('cart').items():
                cart_line = CartLine(product_id=product_id, quantity=quantity)
                total += cart_line.total()
                list.append(cart, cart_line)
        else:
            cart = None
    else:
        try:
            client = Client.objects.get(user_id=request.user.id)
            cart = CartLine.objects.filter(client_id=client.id)
            for cart_line in cart:
                total += cart_line.total()
        except:
            cart = None

    contexts = {'cart': cart, 'grand_total': int(total), 'page_name': page_name}
    return render(request, 'store/cart.html', context=contexts)


@login_required(login_url='store:connexion')
def shipping(request):
    # client = Client.objects.get(user_id=request.user.id)
    # addresses_list = Address.objects.filter(client_id=client.id)

    if request.method == 'POST':
        request.session['shipping_address'] = request.POST['shipping_address']
        request.session['phone'] = request.POST['phone']
        return redirect('store:checkout')

    # if 'shipping_address' in request.session and 'phone' in request.session:
    #     shipping_address = request.session['shipping_address']
    #     phone = request.session['phone']
    #

    return render(request, 'store/shipping.html')


@login_required(login_url='store:connexion')
def checkout(request):
    page_name = 'checkout'
    # if 'shipping_address' not in request.session or 'invoicing_address' not in request.session:
    #     return redirect(reverse('store:shipping'))

    total = 0
    try:
        client = Client.objects.get(user_id=request.user.id)
        cart = CartLine.objects.filter(client_id=client.id)
        for cart_line in cart:
            total += cart_line.total()
        total_cents = int(round(total * 100))

    except:
        cart = None
        total_cents = None

    # if request.method == 'POST':
    #     # Set your secret key: remember to change this to your live secret key in production
    #     # See your keys here https://dashboard.stripe.com/account
    #     # stripe.api_key = "sk_test_1g1mSv8k1NZxmsfDKvIckMZL"
    #
    #     # Get the credit card details submitted by the form
    #     token = request.POST.get('stripeToken', None)
    #
    #     order = __create_order_from_database_cart(request)
    #
    #     # Create the charge on Stripe's servers - this will charge the user's card
    #     if token:
    #         try:
    #             charge = stripe.Charge.create(
    #                 amount=total_cents,  # amount in cents, again
    #                 currency="eur",
    #                 card=token,
    #                 description='Charge for order ' + str(order.id)
    #             )
    #             order.status = Order.PAID
    #             order.stripe_charge_id = charge.id
    #             order.save()
    #             return redirect(reverse('commerce:confirmation'))
    # except stripe.CardError, e:
    #     # The card has been declined
    #     pass

    contexts = {
        'cart': cart,
        'grand_total': int(total),
        'grand_total_cents': total_cents,
        'user_email': request.user.email,
        'page_name': page_name
    }
    return render(request, 'store/checkout.html', context=contexts)


@login_required(login_url='store:connexion')
def confirmation(request):
    page_name = 'confirmation'
    order = __create_order_from_database_cart(request)
    order.status = Order.PAID

    contexts = {
        'page_name': page_name
    }
    # return redirect('index')
    return render(request, 'store/confirmation.html', context=contexts)


@login_required(login_url='store:connexion')
# @user_passes_test(is_customer)
def my_order_view(request):
    page_name = "mes commandes"
    client = Client.objects.get(user_id=request.user.id)
    orders = Order.objects.all().filter(client_id=client.id).order_by('-order_date')
    # ordered_products = []
    # for order in orders:
    #     ordered_product = Product.objects.all().filter(id=order.product.id)
    #     ordered_products.append(ordered_product)

    return render(request, 'store/my_order.html', {'orders': orders, 'page_name': page_name})


@login_required(login_url='store:connexion')
# @user_passes_test(is_customer)
def my_order_view_detail(request, commande_id):
    page_name = "detail commandes"
    order = Order.objects.get(pk=commande_id)
    commande_items = order.commande.all()

    return render(request, 'store/order_detail.html', {'commande_items': commande_items, 'order': order, 'page_name': page_name})


@login_required(login_url='store:connexion')
# @user_passes_test(is_customer)
def my_profile_view(request):
    page_name = 'mon compte'
    customer = Client.objects.get(user_id=request.user.id)
    try:
        image = customer.profile_pic.url
    except:
        image = None
    return render(request, 'store/my_profile.html', {'customer': customer, 'page_name': page_name, 'image': image})


@login_required(login_url='store:connexion')
# @user_passes_test(is_customer)
def edit_profile_view(request):
    page_name = 'mis à jour'
    client = Client.objects.get(user_id=request.user.id)
    user = User.objects.get(id=client.user_id)
    user_form = RegisterForm(instance=user)
    client_form = ClientForm(request.FILES, instance=client)
    mydict = {'user_form': user_form, 'client_form': client_form, 'page_name': page_name}
    if request.method == 'POST':
        user_form = RegisterForm(request.POST, instance=user)
        client_form = ClientForm(request.POST, instance=client)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            client_form.save()
            messages.add_message(request, messages.SUCCESS, "Vos informations ont été correctement mises à jour.")
            return redirect('store:my-profile')
    return render(request, 'store/edit_profile.html', context=mydict)


# @login_required(login_url='/sign-in')
# def account(request):
#     form = RegisterFormUpdate(instance=request.user)
#     if request.method == 'POST':
#         form = RegisterFormUpdate(request.POST)
#         if form.is_valid():
#             user = request.user
#             user.first_name = form.cleaned_data['first_name']
#             user.last_name = form.cleaned_data['last_name']
#             user.email = form.cleaned_data['email']
#             user.save()
#             messages.add_message(request, messages.SUCCESS, "Vos informations ont été correctement mises à jour.")
#             return redirect('commerce:account')
#     return render(request, 'account.html', {'form': form})


@login_required(login_url='/sign-in')
def orders(request):
    client = Client.objects.get(user_id=request.user.id)
    return render(request, 'orders.html', {'orders': client.orders()})


@login_required(login_url='/sign-in')
def addresses(request):
    client = Client.objects.get(user_id=request.user.id)
    return render(request, 'addresses.html', {'addresses': client.addresses()})

# try:
#     p = Produit.objects.get(pk=produit_id)
# except Produit.DoesNotExist:
#     raise Http404("Désolé, nous n'avons pas trouver ce produit")
