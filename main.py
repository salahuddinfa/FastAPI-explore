from fastapi import FastAPI,Query
from enum import Enum
from typing import Union,Annotated
from pydantic import BaseModel


class Product(BaseModel):
    name:str
    description: Union[str,None] = None
    price : float
    tax: Union[float,None] = None


class ModelName(str,Enum):
    xnet = 'xnet'
    ynet = 'ynet'
    znet = 'znet'

app = FastAPI()

@app.get('/items/{item_id}')
async def test(item_id : int):
    return {'message':item_id}


@app.get('/models/{model_name}')
def get_model(model_name:ModelName): 
    if model_name is ModelName.xnet:
        return {'model':model_name}
    if model_name.value == 'ynet':
        return {'model':model_name}
    return {'model': model_name}

@app.get('/params/{param_id}')
def path_query_parameters(param_id: int ,skip: int = 0,limit: Union[int,None]=None,short:bool = False):
    data={}
    if param_id:
        data['param_id'] = param_id
    data["skip"] = skip
    
    data['short'] = short
    if limit:
        data['limit'] = limit
    return data


# you will get type hints and completion everywhere
#  (this wouldn't happen if you received a dict instead of a Pydantic model):
@app.put('/products/{product_id}')
def create_product(product_id: int,product:Product,skip:int,limit:Union[int,None]=None):
    
    product.name = product.name.capitalize()
    product_dict = product.model_dump()
    result = {"product_id":product_id}
  
    if product.tax:
        total_amount = product.price + product.tax
        product_dict['total_amount'] = total_amount
    
    result['skip'] = skip
    if limit:
        result['limit'] = limit
    result.update(**product_dict)
    print(result)
    # result.update(**product_dict)
    # print(result)
    return result 

@app.get("/elements/{element_id}/")
def get_elements(element_id : int,q: Annotated[Union[list,None],Query()]=...):
    result = {'elements':[{'id':1},{'id':2}]}
    result['element_id'] = element_id
    if q :
        result.update({'q':q})
    return result