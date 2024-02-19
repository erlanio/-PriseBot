
from typing import Any, Text, Dict, List ## Datatypes

from rasa_sdk import Action, Tracker  ##
from rasa_sdk.executor import CollectingDispatcher
import pymysql.cursors
from contextlib import contextmanager
import openai

#DETECTAÇÃO DE IDIOMAS
import spacy
from spacy.language import Language
from spacy_language_detection import LanguageDetector

from bardapi import Bard
import os

openai.api_key = "API-KEY"
host = "localhost"
user = "root"
password = ""
database = "mrrt"
charset = "utf8mb4"

botoes = []
idioma = ""
class ActionSearch(Action):

    def name(self) -> Text:
        return "action_search"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Calling the DB
        #calling an API
        # do anything
        #all caluculations are done
        idioma = ""
        ent = tracker.latest_message['entities'][0]['value']
        botoes.clear()
        print(f"Entidade: {ent}")

        def get_lang_detectorr(nlp, name):
            return LanguageDetector(seed=42)  # We use the seed 42


        nlp_model = spacy.load("en_core_web_sm")
        Language.factory("language_detectorr", func=get_lang_detectorr)
        nlp_model.add_pipe('language_detectorr', last=True)
       
        txt_completo = tracker.latest_message['text']
        job_title = txt_completo
        doc = nlp_model(job_title)
        idioma = doc._.language['language']
    
        conexao = pymysql.connect(
            host = host,
            user = user,
            password = password,
            db=database,
            charset = charset,
            cursorclass = pymysql.cursors.DictCursor
        )
        print(idioma)
        if idioma != 'en':
            with conexao.cursor() as cursor:
                total =  (f"SELECT count(*) as total from constructs as c JOIN publications as p on p.id = c.publications_id WHERE concept_pt LIKE  '%{ent}%' OR sinonimos LIKE '{ent} %' or sinonimos LIKE '%{ent}' OR  sinonimos LIKE '% {ent} %'")
                cursor.execute(total)
                resultado = cursor.fetchall()
                for item in resultado: 
                    numTotal = item['total']
                    if numTotal >= 1:
                        if numTotal == 1:
                            msgConst = "construtor relacionado"
                        elif numTotal > 1:
                            msgConst = 'construtores relacionados'
                        msgTotal = (f"Identifiquei {numTotal} {msgConst} a {ent}.")
                        dispatcher.utter_message(msgTotal)
                    else:                    
                        msgNaoTem = (f"Desculpe, mas não pude identificar nenhum construtor relacionado a {ent}")
                        dispatcher.utter_message(msgNaoTem)
                    
        else:
            with conexao.cursor() as cursor:
                total = (f"SELECT count(*) as total from constructs as c JOIN publications as p on p.id = c.publications_id WHERE concept LIKE '{ent}%' OR concept LIKE '{ent} %' OR concept LIKE '% {ent}' OR concept LIKE '% {ent} %'")
                cursor.execute(total)
                resultado = cursor.fetchall()
                for item in resultado: 
                    numTotal = item['total']
                    if numTotal >= 1:
                        if numTotal == 1:
                            msgConst = "related constructor"
                        elif numTotal > 1:
                            msgConst = 'related constructors'
                            msgTotal = (f"I identified {numTotal} {msgConst} a {ent}.")
                            dispatcher.utter_message(msgTotal)
                    else:
                        msgNaoTem = (f"Sorry, but I couldn't identify any constructors related to {ent}")
                        dispatcher.utter_message(msgNaoTem)

        with conexao.cursor() as cursor:
            if idioma != 'en':        
                sql = (f"SELECT c.id as id, c.path_svg as path_svg, p.title as title, p.title_pt as title_pt, c.image as image, c.description_pt as description, c.form_pt as form, c.concept_pt as concept, c.type_pt as type, c.example_image as example from constructs as c JOIN publications as p on p.id = c.publications_id WHERE concept_pt LIKE '%{ent}%' OR sinonimos LIKE '{ent} %' or sinonimos LIKE '%{ent}' OR  sinonimos LIKE '% {ent} %'")
            elif idioma == 'en':             
                sql = (f"SELECT  c.id as id, c.path_svg as path_svg, p.title as title, c.image as image, c.description as description, c.form as form, c.concept as concept, c.type as type, c.example_image as example from constructs as c JOIN publications as p on p.id = c.publications_id WHERE concept LIKE '{ent}%' OR concept LIKE '{ent} %' OR concept LIKE '% {ent}' OR concept LIKE '% {ent} %'")
            print(sql)
            cursor.execute(sql)
            resultado = cursor.fetchall()
            for item in resultado:
                image = 'https://istarextensions.cin.ufpe.br/catalogue/images/'+item['image']
                
                if item['example']:
                    example = 'https://istarextensions.cin.ufpe.br/catalogue/images/'+item['example']
                
                description = item['description']
                extension = item['title']
                title = item['concept']
                type_construct = item['type']
                form = item['form']
                path_svg = item['path_svg']
                id = item['id']
                if idioma != 'en':
                    msg = (f"Título: {title} \n \nDescrição: {description} \n \nExtensão: {extension} \n \nTipo: {type_construct} \n \nForma: {form}")
                    msgExample = "Estou lhe enviando um exemplo de uso: "
                else:
                    msg = (f"Title: {title} \n \nDescription: {description} \n \nExtension: {extension} \n \nType: {type_construct} \n \nForm: {form}")
                    msgExample = "I'm sending you an example of use:"
                dispatcher.utter_message(msg, image)
               
                if item['example']:
                    dispatcher.utter_message(msgExample, example)
                
                if idioma != 'en':
                    if numTotal > 0:
                        if item['path_svg']:
                            shape = f"SHAPE-{id}"
                            title = f"VER SHAPE - {item['title_pt']}"
                            botoes.append({"title": title ,"payload": shape})

                if idioma == 'en':
                    if numTotal > 0:
                        if item['path_svg']:
                            shape = f"SHAPE-{id}"
                            title = f"VIEW SHAPE - {item['title']}"
                            botoes.append({"title": title ,"payload": shape})
                                 
            dispatcher.utter_message("Ver o shape do construtor", buttons=botoes)
                               
                #dispatcher.utter_message(item)
                    #    dispatcher.utter_message(item)
        
        
        return []

class BuscarExtensao(Action):
    def name(self) -> Text:
        return "action_buscar_extensao"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Calling the DB
        #calling an API
        # do anything
        #all caluculations are done
        try:
            ent = tracker.latest_message['entities'][0]['value']
        except:
            dispatcher.utter_message("Ops! Não consegui identificar nenhuma extensão relacioanda a sua busca")
            return[]
       
        print(ent)
        #salvar pergunta e resposta no bd
        conexao = pymysql.connect(
            host = host,
            user = user,
            password = password,
            db=database,
            charset = charset,
            cursorclass = pymysql.cursors.DictCursor
        )

        def get_lang_detector(nlp, name):
            return LanguageDetector(seed=42)  # We use the seed 42


        nlp_model = spacy.load("en_core_web_sm")
        Language.factory("language_detector", func=get_lang_detector)
        nlp_model.add_pipe('language_detector', last=True)
       
        txt_completo = tracker.latest_message['text']
        job_title = txt_completo
        doc = nlp_model(job_title)
        idioma = doc._.language['language']
        if idioma == 'pt':
            sql = f"SELECT * FROM publications where title_pt LIKE '%{ent}%' "
            sqlCount = f"SELECT count(*) as total FROM publications where title_pt LIKE '%{ent}%'"
        else:
            sql = f"SELECT * FROM publications where title LIKE '%{ent}%'"
            sqlCount = f"SELECT count(*) as total FROM publications where title LIKE '%{ent}%'"
        
        #retorna total
        with conexao.cursor() as cursor:                
                cursor.execute(sqlCount)
                resultado = cursor.fetchall()
                for i in resultado:
                    total = i['total']

       

        if idioma != 'en':
            msgFinal = "Posso ajudar em mais alguma coisa?"
            if total == 1:
                msgTotal = f"Identifiquei uma extensão relacionadas a sua busca"
            elif total >= 1:
                msgTotal = f"Identifiquei {total} extensões relacionadas a sua busca"
            else:
                msgTotal = f"Desculpe, não consegui identificar nenhuma extensão relacionada a sua busca"
        else:
            msgFinal = "Can I help you with anything else?"
            if total == 1:
                msgTotal = f"I've identified an extension related to your search"
            elif total >= 1:
                msgTotal = f"I identified {total} extensions related to your search"
            else:
                msgTotal = f"Sorry, I couldn't identify any extensions related to your search"

        dispatcher.utter_message(msgTotal) 

    
        with conexao.cursor() as cursor:                
            cursor.execute(sql)
            resultado = cursor.fetchall()
            for item in resultado:
                title_pt = item['title_pt']
                title = item['title']
                link = item['url']
                ano = item['year']
                journal = item['journal']
                authors = item['authors']
                if idioma != 'en':
                    msg = (f"Título: {title} \n \nLink: {link} \n \nAno: {ano} \n \nJournal: {journal} \n \nAutores: {authors}")                        
                else:                    
                    msg = (f"Title: {title} \n \nURL: {link} \n \nYear: {ano} \n \nJournal: {journal} \n \nAuthors: {authors}")
                        
                dispatcher.utter_message(msg)

            dispatcher.utter_message(msgFinal)  
        return []







class ActionDefaultFallback(Action):

   

    def name(self) -> Text:
        return "action_default_fallback"
    

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Calling the DB
        #calling an API
        # do anything
        #all caluculations are done
        conexao = pymysql.connect(
        host = host,
        user = user,
        password = password,
        db=database,
        charset = charset,
        cursorclass = pymysql.cursors.DictCursor
        )
        texto = tracker.latest_message['text']
        print(texto)
        try:
            tipoBusca = texto.split('-')[0]
            id = texto.split('-')[1]
            print(tipoBusca)
            print(id)
        except:
            print("erro")
        if tipoBusca == "SHAPE":
            sql = f"SELECT path_svg, concept, image, concept_pt FROM constructs where id = {id}"
            with conexao.cursor() as cursor:                
                cursor.execute(sql)
                resultado = cursor.fetchall()
                for item in resultado:
                    path_svg = item['path_svg']

                    if idioma != 'en':
                        dispatcher.utter_message(f"Claro, estou te enviando o SVG do construtor {item['concept_pt']}: ")
                        image = 'http://istarextensions.cin.ufpe.br/catalogue/images/'+item['image']
                        dispatcher.utter_message('', image)
                        dispatcher.utter_message(path_svg)
                        dispatcher.utter_message("Deseja visualizar o shape de outro construtor?", buttons=botoes)  
                    else: 
                        dispatcher.utter_message(f"Sure, I'm sending you the SVG of construct {item['concept_pt']}: ")
                        image = 'http://istarextensions.cin.ufpe.br/catalogue/images/'+item['image']
                        dispatcher.utter_message('', image)
                        dispatcher.utter_message(path_svg)
                        dispatcher.utter_message("Do you want to view the shape of another construct?", buttons=botoes)           
        else:

            
            resposta = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Suponha que você é um engenheiro de software"},
                    {"role": "user", "content": texto},
                ],
                temperature=0.7,
            )

            textoRecebido =  resposta['choices'][0]['message']['content'] 
            dispatcher.utter_message(textoRecebido)

            with conexao.cursor() as cursor:
                sql =  (f"INSERT INTO perguntas_gpt (pergunta, resposta) VALUES ('{texto}', '{textoRecebido}')")
                cursor.execute(sql)
                conexao.commit()
        return []
