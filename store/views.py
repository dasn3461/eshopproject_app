from django.shortcuts import render,redirect
from django.views.generic import  TemplateView,View,CreateView,FormView,DetailView,ListView
from .models import *
from .forms import CheckOutForm,CustomerRegistrationForm,CustomerLoginForm ,ProductForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
class EShopMix(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id=request.session.get('cart_id')
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer=request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)
    
    

class HomeView(EShopMix,TemplateView):
    template_name='home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Product.objects.all().order_by('-id')
        paginator=Paginator(all_products, 6)
        page_number=self.request.GET.get('page')
        products=paginator.get_page(page_number)
        context["products"] = products
        return context
    
    
class AllProductsView(EShopMix,TemplateView):
    template_name='allProducts.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context    
    
    
class ProductDetailsView(EShopMix,TemplateView):
    template_name='productdetails.html'  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug=self.kwargs['slug']
        product=Product.objects.get(slug=url_slug)
        product.view_count+=1
        product.save()
        context["product"] = product 
        return context
    
    
class AddToCartView(EShopMix,TemplateView):
    template_name='addtocart.html'  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Product Item
        product_id=self.kwargs['pro_id']
        product_obj=Product.objects.get(id=product_id)
        # Cart Item
        cart_id=self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            this_product_in_cart=cart_obj.cartproduct_set.filter(product=product_obj)
            if this_product_in_cart.exists():
                cartproduct=this_product_in_cart.last()
                cartproduct.quantity+=1
                cartproduct.subtotal+=product_obj.selling_price
                cartproduct.save()
                cart_obj.total+=product_obj.selling_price
                cart_obj.save()
            else:
                cartproduct=CartProduct.objects.create(cart=cart_obj, product=product_obj,rate=product_obj.selling_price,quantity=1,subtotal=product_obj.selling_price)   
                cart_obj.total+=product_obj.selling_price
                cart_obj.save() 
        else:    
            cart_obj=Cart.objects.create(total=0)
            self.request.session['cart_id']=cart_obj.id
            cartproduct=CartProduct.objects.create(cart=cart_obj, product=product_obj,rate=product_obj.selling_price,quantity=1,subtotal=product_obj.selling_price)   
            cart_obj.total+=product_obj.selling_price
            cart_obj.save()
        return context
    
    
    
class MyCartView(EShopMix,TemplateView):
    template_name='viewcart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id=self.request.session.get('cart_id', None)
        if cart_id:
            cart=Cart.objects.get(id=cart_id)
        else:
            cart=None    
        context["cart"] = cart 
        return context


class ManageCartView(EShopMix,View):
    def get(self, request, *args, **Kwargs):
        cp_id=self.kwargs['cp_id']
        action=request.GET.get('action')
        cp_obj=CartProduct.objects.get(id=cp_id)
        cart_obj=cp_obj.cart
        if action=='inc':
            cp_obj.quantity+=1
            cp_obj.subtotal+=cp_obj.rate
            cp_obj.save()
            cart_obj.total+=cp_obj.rate
            cart_obj.save()
            
        elif action =='dcr':
            cp_obj.quantity-=1
            cp_obj.subtotal-=cp_obj.rate
            cp_obj.save()
            cart_obj.total-=cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity==0:
                cp_obj.delete()
        
        elif action=='rmv':
            cart_obj.total-=cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass           
        return redirect('viewcart')
    
    
    
class EmptyCartView(EShopMix,View):
    def get(self, request, *args, **Kwargs):
        cart_id=self.request.session.get('cart_id', None)
        if cart_id:
            cart=Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()         
            cart.total=0         
            cart.save()         
        return redirect('viewcart')  
        
        
class CheckOutView(EShopMix,CreateView):
    template_name='checkout.html'
    form_class=CheckOutForm    
    success_url=reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass 
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id=self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
        else:
            cart_obj=None    
        context["cart"] = cart_obj
        return context
    
    
    def form_valid(self, form):
        cart_id=self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            form.instance.cart=cart_obj
            form.instance.subtotal=cart_obj.total
            form.instance.discount=0
            form.instance.total=cart_obj.total
            form.instance.order_status='Order Received'
            del self.request.session['cart_id']
        else:
            return redirect('home')    
        return super().form_valid(form)
      

class CustomerRegistrationView(EShopMix,CreateView):
    template_name='customerregistration.html'
    form_class=CustomerRegistrationForm    
    success_url=reverse_lazy('customerlogin')
    
    
    def form_valid(self, form):
        username=form.cleaned_data['username']
        email=form.cleaned_data['email']
        password=form.cleaned_data['password']
        user=User.objects.create_user(username,email,password)
        form.instance.user=user
        login(self.request, user)
        return super().form_valid(form)
    
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url=self.request.GET.get("next")
            return next_url
        else:
            return self.success_url
    
        

class CustomerLogoutView(EShopMix,View):
    def get(self, request):
        logout(request)
        return redirect('home')    


class CustomerLoginView(EShopMix,FormView):
    template_name='customerlogin.html'
    form_class=CustomerLoginForm    
    success_url=reverse_lazy('home')
    
    def form_valid(self, form):
        unam=form.cleaned_data['username']
        pwd=form.cleaned_data['password']
        usr=authenticate(username=unam, password=pwd)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {'form':self.form_class, 'error':'invalid credentials'})    
        return super().form_valid(form)
    
    
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url=self.request.GET.get("next")
            return next_url
        else:
            return self.success_url
        
        
        
class CustomerProfileView(TemplateView):
    template_name='customerprofile.html'  
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass 
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)  
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer=self.request.user.customer
        context["customer"] = customer 
        orders=Order.objects.filter(cart__customer=customer).order_by("-id")
        context["orders"] = orders 
        return context
    
    
    
class CustomerOrderDetailsView(DetailView):
    template_name='customerorderdetails.html'    
    model=Order
    context_object_name='ord_obj'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id=self.kwargs['pk']
            order=Order.objects.get(id=order_id)
            if request.user.customer!=order.cart.customer:
                return redirect('customerprofile')
                
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)  
        
        
class Search(TemplateView):
    template_name='search.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw=self.request.GET['keyword']
        results=Product.objects.filter(
            Q(title__icontains=kw)|Q(description__icontains=kw)|Q(return_policy__icontains=kw))
        context["results"] = results
        return context
    

     
    
    
# Admin Page

class AdminLoginView(FormView):
    template_name='adminpages/adminlogin.html'
    form_class=CustomerLoginForm    
    success_url=reverse_lazy('adminhome')
    
    def form_valid(self, form):
        unam=form.cleaned_data['username']
        pwd=form.cleaned_data['password']
        usr=authenticate(username=unam, password=pwd)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {'form':self.form_class, 'error':'invalid credentials'})    
        return super().form_valid(form)
    
    
    
class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass   
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)  
    
    
class AdminHomeView(AdminRequiredMixin,TemplateView):
    template_name='adminpages/adminhome.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(order_status='Order Received').order_by('-id') 
        return context
    
    
class AdminOrderDetailsView(AdminRequiredMixin,DetailView):
    template_name='adminpages/adminorderdetails.html'    
    model=Order
    context_object_name='ord_obj'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context
    
    
    
    
    
    

class AdminOrderListView(AdminRequiredMixin,ListView):
    template_name='adminpages/adminorderlist.html'    
    queryset=Order.objects.all().order_by('id')
    context_object_name='allorderes'
    
    
class AdminOrderStatuschangeListView(AdminRequiredMixin,View):
    def post(self, request,*args, **kwargs):
        order_id=self.kwargs['pk']
        order_obj=Order.objects.get(id=order_id)
        new_status=request.POST.get('status')
        order_obj.order_status=new_status
        order_obj.save()
        return redirect(reverse_lazy('adminorderdetails',kwargs={"pk":self.kwargs['pk']}))    
    
    

class AdminProductListView(AdminRequiredMixin,ListView):
    template_name='adminpages/adminproductlist.html'    
    queryset=Product.objects.all().order_by('-id')
    context_object_name='allproducts'    
    
    
    
class AdminProductCreateView(AdminRequiredMixin,CreateView):
    template_name='adminpages/adminproductcreate.html'    
    form_class=ProductForm
    success_url=reverse_lazy('adminoproductlist') 
    
    
    def form_valid(self, form):
        p=form.save()
        images=self.request.FILES.get('more_images')
        for i in images:
            ProductImage.objects.create(product=p,image=i)
        return super().form_valid(form)
        
        
    
    

        
    
    
             
    
    
    
    
    