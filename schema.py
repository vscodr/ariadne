from ariadne import QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL
import json
import requests

from ariadne import ObjectType, make_executable_schema

from ariadne import ObjectType, make_executable_schema

type_defs = gql("""
    type Query {
        hello: String!
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
    }
""")

query = ObjectType("Query")

@query.field("hello")
def resolve_hello(*_):
    return "Hello!"

@query.field("person")
def resolve_person(self, info, id):
    response = requests.get(f'https://swapi.dev/api/people/{id}')
    res = json.loads(response.text)
    dict_items = dict(res.items())
    return dict_items


schema = make_executable_schema(type_defs, query)


schema = make_executable_schema(type_defs, query)
app = GraphQL(schema, debug=True)