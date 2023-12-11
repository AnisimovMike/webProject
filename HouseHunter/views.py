from django.shortcuts import render, redirect
from .models import Graphic, Object
from .forms import UserForm, LoadObject, AuthorizationForm
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


header = """
 <nav id="nav" role="navigation">
    <a href="#nav" title="Show navigation">Show navigation</a>
    <a href="#" title="Hide navigation">Hide navigation</a>
    <ul class="clearfix">
    <li class="active"><a href="/" title="">Home</a></li>
    <li><a href="/about-us" title="">About Us</a></li>                
    <li><a href="/catalog/all" title="">Catalog</a></li>
    <li><a href="/services" title="">Services</a></li>
    <li><a href="#" title=""><span>Features</span></a>
      <ul> <!-- Submenu -->
          <li><a href="/charts" title="">Charts</a></li>
          <li><a href="/authorization" title="">Authorization</a></li>
     </ul> <!-- End Submenu -->      
   </li>
   </ul>
</nav>
"""


def index(request):
    data = {"header": header}
    return render(request, "index.htm", context=data)


def send_mes(request):
    cur_name = request.POST.get("name")
    cur_email = request.POST.get("email")
    cur_mes = request.POST.get("message")
    print(cur_name, cur_email, cur_mes)
    data = {"header": header}
    return render(request, "index.htm", context=data)


def about_us(request):
    data = {"header": header}
    return render(request, "about-us.htm", context=data)


def catalog(request, object_filter):
    if object_filter == "all":
        object_list = Object.objects.filter()
    elif object_filter == "commercial":
        object_list = Object.objects.filter(object_type='commercial')
    elif object_filter == "country":
        object_list = Object.objects.filter(object_type='country')
    elif object_filter == "residential":
        object_list = Object.objects.filter(object_type='residential')
    else:
        object_list = None

    obj_dict = []
    for cur_object in object_list:
        foto_link = cur_object.foto_link
        address = cur_object.address
        object_type = cur_object.object_type

        img_link = f"img/catalog/{foto_link}"
        cur_obj = {'address': address, 'img_link': img_link, 'object_type': object_type}
        obj_dict.append(cur_obj)

    data = {"header": header, "obj_dict": obj_dict}
    return render(request, "gallery.htm", context=data)


def services(request):
    data = {"header": header}
    return render(request, "services.htm", context=data)


def charts(request):
    get_graphic = ""
    for i in range(1, 6):
        cur_graphic = Graphic.objects.get(id=i)
        cur_chartType = cur_graphic.cur_chartType
        cur_dataTable = cur_graphic.cur_dataTable
        more = cur_graphic.more
        cur_title = cur_graphic.cur_title
        js_script = f"""
            <script type='text/javascript'>
              function drawVisualization{i}() {{
                var wrapper = new google.visualization.ChartWrapper({{
                  chartType: '{cur_chartType}',
                  dataTable: {cur_dataTable},
                  options: {{
                    {more}
                    'title': '{cur_title}'
                  }},
                  containerId: 'vis_div{i}'
                }});
                wrapper.draw();
              }}
            </script>
        """
        get_graphic += js_script

    data = {"header": header, "get_graphic": get_graphic}
    return render(request, "charts.htm", context=data)


def authorization(request):
    form1 = AuthorizationForm()
    form2 = UserForm()
    form3 = LoadObject()
    cur_login = ''
    cur_password = ''
    cur_action = ''
    if request.method == "POST":
        cur_login = request.POST.get("login")
        cur_password = request.POST.get("password")
        cur_action = request.POST.get("new_action")
        print(cur_login)
        print(cur_password)
    if cur_login == 'superuser' and cur_password == '12345':
        if cur_action == 'add':
            response = redirect('/bd/1')
            # data = {"header": header, "bd_form": form2}
        else:
            response = redirect('/bd/2')
            # data = {"header": header, "bd_form": form3}
        return response
        # return render(request, "bd.htm", context=data)
    else:
        data = {"header": header, "authprization_form": form1}
        return render(request, "authorization.htm", context=data)


def bd(request, f):
    form1 = UserForm()
    form2 = LoadObject()
    mes = ''
    if request.method == "POST":
        if f == 1:
            mes = 'Данные отправлены на сервер и добавлены в БД'
            cur_square = request.POST.get("square")
            cur_address = request.POST.get("address")
            cur_email_address = request.POST.get("email_address")
            object_type = request.POST.get("type")
            price = request.POST.get("price")
            foto_link = request.POST.get("foto_link")
            new_object = Object.objects.create(square=cur_square, address=cur_address,
                                               email_address=cur_email_address, object_type=object_type,
                                               price=price, foto_link=foto_link)
            gr = Graphic.objects.get(id=2)
            cur_data = gr.cur_dataTable
            cur_data = cur_data[1:-1]
            cur_data = cur_data.split('[')
            c1 = int(cur_data[2][13:-2])
            c2 = int(cur_data[3][10:-2])
            c3 = int(cur_data[4][14:-1])
            if object_type == 'commercial':
                c1 += 1
            elif object_type == 'country':
                c2 += 1
            elif object_type == 'residential':
                c3 += 1
            gr.cur_dataTable = f"[['Property types','Quantity'],['Commercial',{c1}],['Country',{c2}],['Residential',{c3}]]"
            gr.save(update_fields=["cur_dataTable"])
        else:
            obj_id = request.POST.get("obj_id")
            method_type = request.POST.get("method_type")
            print(method_type)
            if method_type == '1':
                try:
                    cur_obj = Object.objects.get(id=obj_id)
                    mes = f"""
                    square: {cur_obj.square}
                    address: {cur_obj.address}
                    email_address: {cur_obj.email_address}
                    object_type: {cur_obj.object_type}
                    price: {cur_obj.price}
                    """
                except ObjectDoesNotExist:
                    mes = "ObjectDoesNotExist"
                except MultipleObjectsReturned:
                    mes = "MultipleObjectsReturned"
            elif method_type == '2':
                cur_obj = Object.objects.get(id=obj_id)
                cur_object_type = cur_obj.object_type
                Object.objects.filter(id=obj_id).delete()
                gr = Graphic.objects.get(id=2)
                cur_data = gr.cur_dataTable
                cur_data = cur_data[1:-1]
                cur_data = cur_data.split('[')
                c1 = int(cur_data[2][13:-2])
                c2 = int(cur_data[3][10:-2])
                c3 = int(cur_data[4][14:-1])
                if cur_object_type == 'commercial':
                    c1 -= 1
                elif cur_object_type == 'country':
                    c2 -= 1
                elif cur_object_type == 'residential':
                    c3 -= 1
                gr.cur_dataTable = f"[['Property types','Quantity'],['Commercial',{c1}],['Country',{c2}],['Residential',{c3}]]"
                gr.save(update_fields=["cur_dataTable"])
                mes = f"Объект {obj_id} удалён"
                pass
    if f == 1:
        data = {"header": header, "bd_form": form1, "mes": mes}
    else:
        data = {"header": header, "bd_form": form2, "mes": mes}
    return render(request, "bd.htm", context=data)
