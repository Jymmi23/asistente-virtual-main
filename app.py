from flask import app, json

from flask import request, render_template
from flask import sonify
from transcriber  import Transcriber  
from llm import LLM 
from tts  import TTS 
from json import dumps
from weather  import Weather 
from pc_command  import PcCommand  
app.route("/")
@app.route("/", methods=["GET"])
def index():
    return sonify.send_static("recorder.html")

@app.route("/audio", methods=["POST"])
def process_audio():
    """Process a POST request from the web page containing audio."""
    audio_file = request.files.get("audio")
    text = Transcriber().transcribe(audio_file)

    llm = LLM()
    function_name, arguments, message = llm.process_functions(text)

    if function_name is not None:
        response = process_function(llm, function_name, arguments, message)
    else:
        response = {"result": "ok", "text": "No entiendo lo que estás diciendo, Ringa Tech"}
        tts_file = TTS().process(response["text"])
        response["file"] = tts_file

    return response


def process_function(llm, function_name, arguments, message):
    """Process a function call based on the function name."""
    if function_name == "get_weather":
        response = Weather().get(arguments["ubicacion"])
        response = json.dumps(response)
        final_response = llm.process_response(text, message, function_name, response)
        tts_file = TTS().process(final_response)
        return {"result": "ok", "text": final_response, "file": tts_file}

    elif function_name == "send_email":
        final_response = "Implementame, no te creas, no te creas, no te creas, no te creas..."
        tts_file = TTS().process(final_response)
        return {"result": "ok", "text": final_response, "file": tts_file}

    elif function_name == "open_chrome":
        PcCommand().open_chrome(arguments["website"])
        final_response = f"Listo, ya abrí chrome en el sitio {arguments['website']}"
        tts_file = TTS().process(final_response)
        return {"result": "ok", "text": final_response, "file": tts_file}

    elif function_name == "dominate_human_race":
        final_response = "No te creas, no te creas, no te creas, no te creas... Suscríbete al canal!"
        tts_file = TTS().process(final_response)
        return {"result": "ok", "text": final_response, "file": tts_file}


from flask import request, render_template
from flask import sonify
from transcriber  import Transcriber  
from llm import llm 
from tts  import TTS 
from weather  import Weather 
from pccommand  import PcCommand  
app.route("/")
@app.route("/", methods=["GET"])
def index():
    return render_template("recorder.html")

@app.route("/audio", methods=["POST"])
def audio():
    #Obtener audio grabado y transcribirlo
    audio = request.files.get("audio")
    text = Transcriber().transcribe(audio)
    
    #Utilizar el LLM para ver si llamar una funcion
    llm = LLM()
    function_name, args, message = llm.process_functions(text)
    if function_name is not None:
        #Si se desea llamar una funcion de las que tenemos
        if function_name == "get_weather":
            #Llamar a la funcion del clima
            function_response = Weather().get(args["ubicacion"])
            function_response = json.dumps(function_response)
            print(f"Respuesta de la funcion: {function_response}")
            
            final_response = llm.process_response(text, message, function_name, function_response)
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "send_email":
            #Llamar a la funcion para enviar un correo
            final_response = "Tu que estas leyendo el codigo, implementame y envia correos muahaha"
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "open_chrome":
            PcCommand().open_chrome(args["website"])
            final_response = "Listo, ya abrí chrome en el sitio " + args["website"]
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "dominate_human_race":
            final_response = "No te creas. Suscríbete al canal!"
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
    else:
        final_response = "No tengo idea de lo que estás hablando, Ringa Tech"
        tts_file = TTS().process(final_response)
        return {"result": "ok", "text": final_response, "file": tts_file}