from asyncio import gather
import json
import requests
from ariadne import ObjectType, QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL
import httpx 
from httpx import AsyncClient

type_defs = gql("""
    type Query {
            person(id: Int): Person
            filme : Film        
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
async def resolve_person(self, info, id):
    async with httpx.AsyncClient() as client:
        r = await client.get(f'https://swapi.dev/api/people/{id}')
        #r.json()  
    return r.json()

@person.field("films")

async def resolve_films(person, _):
    films = []
    async with httpx.AsyncClient() as client:
        for i in person['films']:
            r = await client.get(i) 
            films.append(r.json())
        return films    
        
     
film = ObjectType("Film")

schema = make_executable_schema(type_defs, query, person)

app = GraphQL(schema, debug=True)
