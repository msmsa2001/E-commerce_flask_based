from flask import redirect,render_template,request,session,url_for,flash,current_app
from shop import db,app,photos
from .models import Brand,Category, Addproduct
from .forms import Addproducts
import secrets,os


@app.route('/')
def home():
    products=Addproduct.query.filter(Addproduct.stock > 0)
    # brands=Brand.query.all()
    brands=Brand.query.join(Addproduct,(Brand.id==Addproduct.id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    return render_template('products/index.html', title="Home",products=products,brands=brands,categories=categories)

@app.route('/brand/<int:id>')
def get_brand(id):
    brand=Addproduct.query.filter_by(brand_id=id)
    brands=Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    return render_template('products/index.html', title="search",brand=brand,brands=brands,categories=categories)

@app.route('/categories/<int:id>')
def get_category(id):
    get_cat_prod=Addproduct.query.filter_by(category_id=id)
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    brands=Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    return render_template('products/index.html', title="search",get_cat_prod=get_cat_prod,categories=categories,brands=brands)

@app.route('/brands') 
def brands():
    if 'email' not in session:
        flash('Please first login', 'danger')
        return redirect(url_for('login'))
    brands=Brand.query.order_by(Brand.id.desc()).all()
    return render_template('products/brands.html', title='Alll Brands Page' ,brands=brands)

@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if request.method=="POST":
        getbrand=request.form.get('brand')
        brand=Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html',brands='brands')

@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    updatebrand=Brand.query.get_or_404(id)
    if request.method=='POST':
        getbrand=request.form.get('brand')
        updatebrand.name=getbrand
        # brand=Brand(name=getbrand)
        # db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your  database','success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html',updatebrand=updatebrand,title='Update Brand page')

@app.route('/deletebrand/<int:id>',methods=['GET','POST'])
def deletebrand(id):
    brand=Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        db.session.commit()
        flash(f'The {brand.name} was deleted from your database','success')
    return redirect(url_for('admin'))


@app.route('/category') 
def category():
    if 'email' not in session:
        flash('Please first login', 'danger')
        return redirect(url_for('login'))
    category=Category.query.order_by(Category.id.desc()).all()
    return render_template('products/brands.html', title='Category Page' ,categorys=category)

@app.route('/updatecategory/<int:id>',methods=['GET','POST'])
def updatecategory(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    updatecategory=Category.query.get_or_404(id)
    if request.method=='POST':
        getcategory=request.form.get('category')
        updatecategory.name=getcategory

        # brand=Brand(name=getbrand)
        # db.session.add(brand)
        flash(f'The Category {getcategory} was added to your  database','success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html',updatecategory=updatecategory,title='Update Brand page')

@app.route('/addcategory', methods=['GET', 'POST'])
def addcat():
    if request.method=="POST":
        getcat=request.form.get('category')
        cat=Category(name=getcat)
        db.session.add(cat)
        flash(f'The Brand {getcat} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')

@app.route('/deletecategory/<int:id>',methods=['GET','POST'])
def deletecategory(id):
    category=Category.query.get_or_404(id)
    if request.method=="POST":    
        db.session.delete(category)
        db.session.commit()
        flash(f'The {category.name} was deleted from your database','success')
    return redirect(url_for('admin'))



@app.route('/addproduct',methods=['GET','POST'])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    brands=Brand.query.all()
    categories=Category.query.all()
    form=Addproducts(request.form)
    if request.method=='POST':
        name=form.name.data
        price=form.price.data
        discount=form.discount.data
        stock=form.stoke.data
        colors=form.colors.data
        desc=form.discription.data
        brand=request.form.get('brand')
        category=request.form.get('category')
        image_1=photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
        image_2=photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
        image_3=photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")
        addpro=Addproduct(name=name,price=price,discount=discount,stock=stock,colors=colors,desc=desc,brand_id=brand,category_id=category,image_1=image_1,image_2=image_2,image_3=image_3)
        db.session.add(addpro)
        flash(f'the product {name} has been added to your database','success')
        db.session.commit()
    #     return redirect(url_for('admin'))

    return render_template('products/addproducts.html',title='Add products page',form=form,brands=brands,categories=categories)
    # return "Hello"


@app.route('/updateproduct/<int:id>',methods=['GET','POST'])
def updateproduct(id):
    brands=Brand.query.all()
    categories=Category.query.all()
    product=Addproduct.query.get_or_404(id)
    brand=request.form.get('brand')
    category=request.form.get('category')
    form=Addproducts(request.form)
    if request.method=="POST":
        product.name=form.name.data
        product.price=form.price.data
        product.discount=form.discount.data
        product.brand_id=brand
        product.category_id=category
        product.stock=form.stoke.data
        product.colors=form.colors.data
        product.desc=form.discription.data

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_1))
                product.image_1=photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
            except:
                product.image_1=photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")

        if request.files.get('image_2'):
            print("****************************")
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_2))
                product.image_2=photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
            except:
                product.image_1=photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_3))
                product.image_1=photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")
            except:
                product.image_1=photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")
        flash('your product have been updated','success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.name.data=product.name
    form.price.data=product.price
    form.discount.data=product.discount
    form.stoke.data=product.stock
    form.colors.data=product.colors
    form.discription.data=product.desc
    return render_template('products/updateproduct.html',form=form,brands=brands,categories=categories,product=product)

@app.route('/deleteproduct/<int:id>',methods=['GET','POST'])
def deleteproduct(id):
    product=Addproduct.query.get_or_404(id)
    if request.method=="POST": 
        try:   
            os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_1))
            os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_2))
            os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_3))
        except Exception as e:
            print(e)

        db.session.delete(product)
        db.session.commit()
        flash(f'The {product.name} was deleted from your database','success')
    return redirect(url_for('admin'))

@app.route('/createdb')
def createdb():
    db.create_all()
    return "data base created"
