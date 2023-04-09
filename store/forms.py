from django import forms
from .models import Order,Customer,Product
from django.contrib.auth.models import User

class CheckOutForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['ordered_by','shipping_address','email','mobile']
        labels={ 
              'ordered_by':'Order By',  
              'shipping_address':'Shipping Address',  
              'email':'Email',  
              'mobile':'Mobile',  
        }
        
        widgets={ 
                 'ordered_by':forms.TextInput(attrs={'class':'form-control'}),
                 'shipping_address':forms.TextInput(attrs={'class':'form-control'}),
                 'email':forms.TextInput(attrs={'class':'form-control'}),
                 'mobile':forms.TextInput(attrs={'class':'form-control'})
        }
        
        
class CustomerRegistrationForm(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model=Customer
        fields=['username','password', 'email','full_name','address']
        labels={ 
              'username':'Username',  
              'password':'Password',  
              'email':'Email',  
              'full_name':'Full Name',  
              'address':'Address',  
        }
        
        widgets={ 
                 'full_name':forms.TextInput(attrs={'class':'form-control'}),
                 'address':forms.TextInput(attrs={'class':'form-control'}),
        }     
        
    
    def clean_username(self):
        unam=self.cleaned_data['username']
        if User.objects.filter(username=unam).exists():
            raise forms.ValidationError("Customer or Username Alreday Exists!!")
        return unam
               

class CustomerLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    
    
class ProductForm(forms.ModelForm):   
    more_images=forms.FileField(required=False, widget=forms.FileInput(attrs={'class':'form-control','multiple':True}))
   
    class Meta:
        model=Product
        fields=['title', 'slug','category','image','marked_price','selling_price','description','warranty','return_policy']
        labels={ 
              'title':'Title',  
              'slug':'Slug',  
              'category':'Category',  
              'image':'Image',  
              'marked_price':'Marked Price',  
              'selling_price':'Selling Price',  
              'description':'Description',  
              'warranty':'Warranty',  
              'return_policy':'Return Policy',  
        }
        
        widgets={ 
                 'title':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Product Title Here....'}),
                 'slug':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Product Slug Here....'}),
                 'category':forms.Select(attrs={'class':'form-control'}),
                 'image':forms.ClearableFileInput(attrs={'class':'form-control'}),
                 'marked_price':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Marked Price Product....'}),
                 'selling_price':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Selling Price Product....'}),
                 'description':forms.Textarea(attrs={'class':'form-control', 'rows':5,'placeholder':'Product Description Here....'}),
                 'warranty':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Product Warranty Here....'}),
                 'return_policy':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Product Return Policy Here....'}),      
        }    
                  
               
             