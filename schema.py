
import json

import requests
from ariadne import ObjectType, QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL


def get_list_items(list):
   for i in list:
    [r] = requests.get(i)
    print(r)
    




type_defs = gql("""
    type Query {
            person(id: Int): Person
            
        
    },
        type Person{
            name: String
            height: String
            mass: String
            hair_color: String
            skin_color: String
            eye_color: String
            birth_year: String
            gender: String
            films: [Film]
        },

        type Film {
            title: String 
            episode_id: Int 
            opening_crawl: String
            director: String 
            producer: String 
            release_date: String    
            },

        """)







query = ObjectType("Query")


person = ObjectType("Person")
@query.field("person")
def resolve_person(self, info, id):
    response = requests.get(f'https://swapi.dev/api/people/{id}')
    res = json.loads(response.text)
    dict_items = dict(res.items()) 
    # print("this is Person", type(dict_items),  json.dumps(dict_items, indent = 4))   
    return dict_items

@person.field("films")
def resolve_films(Person, info):
    _f = Person['films']
    films = []
    for i in _f:
       r = requests.get(i)
       r_dict = r.json()
       films.append(r_dict)
    return films
    
 
   
    
  



schema = make_executable_schema(type_defs, query, person)

app = GraphQL(schema, debug=True)
