import hug;
import base64;
import main
import uuid


@hug.get()
def getMethod(name: hug.types.text, hug_timer=3):
    return {
        'message': 'Happy birthay {0}'.format(name),
        'took': float(hug_timer)
    }

@hug.post()
def postData(fileData: hug.types.text, hug_timer=3):

    decoded_data = base64.b64decode(fileData)
    output_file = open('file-{0}.pdf'.format(genId()), 'w', encoding="utf-8")
    output_file.write(decoded_data.decode("utf-8"))
    output_file.close()

    jsonData = main.extractData(output_file)

    return {
        'data': jsonData,
        'time': float(hug_timer)
    }


def genId():
    return uuid.uuid4()




