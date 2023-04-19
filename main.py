from fastapi import FastAPI,Form,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sys
sys.path.append('./class_object/')
from system import System
from category import TypeOfTool, SubtypeOfTool
from tool import Tool
from customerinfo import CustomerInfo
from app_database import add_database_users, add_database_system, add_database_userdata


templates = Jinja2Templates(directory="templates")
app = FastAPI()
system = System()
app.mount("/static", StaticFiles(directory="static"), name="static")
add_database_users(system)
add_database_system(system)
add_database_userdata(system)

# CATEGORY
@app.post("/system/category/typeoftools/")
async def add_typeoftool(type_data:dict):
    new_typeoftool = TypeOfTool(type_data['name'])
    system.category.add_type(new_typeoftool)
    return {"ADD TypeOfTool": new_typeoftool}

@app.post("/system/category/subtypeoftools/")
async def add_subtypeoftool(subtype_data:dict):
    new_subtypeoftool = SubtypeOfTool(subtype_data['name'])
    system.category.type_name_add_subtype(subtype_data['type'], new_subtypeoftool)
    return {'ADD SubtypeOfTool':new_subtypeoftool}

# SEARCH
@app.get("/system/category/")
async def search_category(search:str=''):
    return system.category.search_by_category(search)

@app.get("/system/category/tools/")
async def search_category(search:str=''):
    return system.category.search_by_name(search)

#MANAGE TOOL
@app.post("/system/category/tools/")
async def add_tool(tool_data:dict):
    system.create_tool(tool_data["code"], tool_data["name"], tool_data["description"], tool_data["brand"],
                       tool_data["amount"], tool_data["image"], tool_data["price"], tool_data['type_of_tool'])
    return {'ADD Tool':tool_data["name"]}

# MANAGE COUPON
def make_coupon_dict(system : System): 
    dict = {}
    for item in system.server_coupons :
        dict[item.code] = {"name":item.name, "discount_value":item.discount_value}
    return dict

@app.get("/coupons/all/get",tags = ['coupon'])
async def get_coupons(request:Request) -> dict:   
# def  get_coupons() -> dict: 
    # return make_coupon_dict(system)
    data = make_coupon_dict(system)
    return templates.TemplateResponse("getcoupon.html", {"request": request, "data": data})

@app.get("/coupons/all/put",tags = ['coupon'])
async def put_coupons(request:Request): 
    return templates.TemplateResponse("putcoupon.html", {"request": request})

# @app.put("/coupons/all/put",tags=['coupon'])
@app.post("/coupons/all/put",tags=['coupon'])
# async def update_coupons(newcoupon : dict) -> dict: 
async def update_coupons(request: Request,code: str = Form(...), name: str = Form(...), discount_value: int = Form(...)) -> dict:
    newcoupon = {}
    newcoupon[code] = {"discount_value": discount_value,"name": name}
    for key_sys in make_coupon_dict(system).keys(): 
        for key_item in newcoupon.keys(): 
            if key_item == key_sys : 
                system.modify_coupon(key_item,newcoupon[key_item]["discount_value"],newcoupon[key_item]["name"]) 
                # return {"data":f"coupon at code {key_item} has been update"} 
                message = f"coupon at code {key_item} has been update"
                return templates.TemplateResponse("messageput.html", {"request": request,"message": message})
                
    for key in newcoupon.keys():
        # return {"data":f"coupon at code {key} is not found"}
        message = f"coupon at code {key} is not found"
        return templates.TemplateResponse("messageput.html", {"request": request,"message": message})

@app.get("/coupons/all/post",tags=['coupon'])  
async def index(request: Request):
    return templates.TemplateResponse("postcoupon.html", {"request": request})
@app.post("/coupons/all/post",tags=['coupon']) 
# async def add_coupons(newcoupon : dict) -> dict:
async def add_coupons(request: Request,code: str = Form(...), name: str = Form(...), discount_value: int = Form(...)) -> dict: 
    newcoupon = {}
    newcoupon[code] = {"discount_value": discount_value,"name": name}
    for key_item in newcoupon.keys(): 
        for key_sys in make_coupon_dict(system).keys(): 
            if key_item == key_sys :
                # return {"data":f"coupon have already been added"}  
                message = f"coupon have already been added"
                # return {"data" :message}
                return templates.TemplateResponse("messagepost.html", {"request": request,"message": message})
    for key_item in newcoupon.keys(): 
        system.add_coupon(key_item,newcoupon[key_item]["discount_value"],newcoupon[key_item]["name"])        
        # return {"data":f"add new coupon with code {key_item} successfully"}
        message = f"add new coupon with code {key_item} successfully"
        return templates.TemplateResponse("messagepost.html", {"request": request,"message": message})
        # return {"data" :message}

@app.get("/coupons/all/delete",tags=['coupon'])
async def del_coupon(request: Request):
    return templates.TemplateResponse("deletecoupon.html", {"request": request})
# @app.delete("/coupons/all",tags=['coupon'])
@app.post("/coupons/all/delete",tags=['coupon'])
async def delete_coupons(request:Request,input : str =Form(...)) ->dict :  
# async def delete_coupons(code : dict) ->dict : 
    code ={} 
    code["code"] = input
    for key in make_coupon_dict(system).keys(): 
        if key == code["code"] : 
            system.delete_coupon(key) 
            message = f"coupon with code {code} have been deleted"
            return templates.TemplateResponse("messagedelete.html", {"request": request,"message": message})
            # return {"data":f"coupon with code {code} have been deleted"}
    message = f"delete coupon with code {code} is not found"
    return templates.TemplateResponse("messagedelete.html", {"request": request,"message": message})
    # return {"data":f"delete coupon with code {code} is not found"}

# MANAGE WHOLESALE
def system_wholesale() -> dict :  
    dict = {}
    for ws in system.wholesales : 
        dict[ws.code]={"discount_value":ws.discount_value,"amount":ws.amount}
    return dict

def get_wholesale(tool : Tool) -> dict :  
    dict = {} 
    for ws in tool.wholesales : 
        dict[ws.code]={"discount_value":ws.discount_value,"amount":ws.amount}
    return dict

@app.get("/wholesale/all/get",tags = ['wholesale']) 
async def show_wholesale()->dict : 
    return system_wholesale()

@app.put("/wholesale/all",tags = ['wholesale']) 
async def update_wholesale(data : dict) ->dict :
    code = data["wholesale_modify"]["code"]
    for key_sys in system_wholesale().keys(): 
        if key_sys == data["wholesale_modify"]["code"] : 
                system.modify_wholesale(data["wholesale_modify"]["code"],data["wholesale_modify"]["amount"],data["wholesale_modify"]["discount_value"])
                return {"data":f"wholesale at code {code} has been update"} 
                   
    return {"data":f"wholesale at code {code} is not found"} 

@app.post("/wholesale/all/post",tags = ['wholesale'])  
async def add_wholesale(data: dict) -> dict:   
    code = data["wholesale_add"]["code"] 
    for key_sys in system_wholesale().keys(): 
        if key_sys == code: 
            return {"data":f"wholesale at code {code} has been update"}
    system.add_wholesale(data["wholesale_add"]["code"],data["wholesale_add"]["amount"],data["wholesale_add"]["discount_value"])
    return {"data":f"wholesale at code {code} has been update"}

@app.delete("/wholesale/all",tags = ['wholesale']) 
async def delete_wholesale(data : dict) ->dict: 
    code = data["code"]
    for code in system_wholesale() : 
        if code == data["code"]: 
            system.delete_wholesale(data["code"])
            return {"data":f"wholesale with code {code} have been deleted"} 
    return {"data":f"wholesale with code {code} is not found"}

# MANAGE CUSTOMER
#create a new customer
@app.post('/customer/{first_name}/')
async def create_customer(customer:dict)->dict:
    new_customer = CustomerInfo(customer["first_name"], customer["last_name"], customer["email"],customer["company_name"])
    system.add_customerinfo(new_customer)
    return {'data':new_customer}

#create a new address
@app.post('/customer/address/{name}/')
async def create_address(newaddress:dict)->dict:
    for customer in system.customerinfos:
        if customer.first_name == newaddress["name"]:
            customer.create_address(newaddress["name"],newaddress["company"],newaddress["country"],newaddress[ "state"], newaddress["city"], newaddress["address"], newaddress["phone_number"],newaddress["postal_code"])
            return {"data":"You have create the address successfully."}
            
    return{"data":"Unable to create the address."}

# #delete the address     
@app.delete('/cusrtomer/address/{name}',tags=['address'])     
async def delete_address(data:dict) ->dict:
    for customer in system.customerinfos:
        if customer.first_name == data["name"]:
            customer.delete_address(data["name"])
            return {"data":"You have delete the address successfully"}
    return {"data":"Unable to delete the address"}    

#get the address              
@app.get('/customer/address/{address}',tags=['address'])   
async def get_address(name:str)->dict:
  for customer in system.customerinfos:
      if customer.first_name == name:
          address = customer.get_address(name)
          return {"data":f'Your address  {address}'}
  return {"data":"Sorry cannot found your address in system. Please try again!"}    
      
# edit the address       
@app.put('/customer/address/')
async def edit_address(address:dict) ->dict:
    for customer in system.customerinfos:
        if customer.first_name == address["name"]:
            customer.get_address(address["name"]).edit_address(company=address["company"],country=address["country"],state=address[ "state"], city=address["city"], address=address["address"], phone_number=address["phone_number"],postal_code=address["postal_code"])
            return {"data":f"Your edit address is successfully {customer.address}"}
    return {"data":"Unable to edit address. Please try again"}

@app.get('/customer/order{name}')
async def check_order(name:str)->dict:
    for customer in system.customerinfos:
        if customer.first_name == name:
            order = customer.my_order
            return {"data":f"Your order is {order}"}
    return {"data":"Not found this order. Please try again"}    

@app.get('/customer/review{name}')
async def check_review(name:str)->dict:
    for customer in system.customerinfos:
        if customer.first_name == name:
            return {"data":f"Your review is {customer.my_reviewed}"}
    return {"data":"Not found this review. Please try again"}