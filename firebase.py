import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import uuid

cred = credentials.Certificate("./accountkey.json")
# firebase_admin.initialize_app(cred)


# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://statementreader-5f13a-default-rtdb.firebaseio.com/',
    'databaseAuthVariableOverride': {
        'uid': 'client-app'
    }
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('/statements')
print(ref.get())


def saveUserdata(username, data):
    ref = db.reference("/statements/" + username)
    ref.push().set(data)

def fetchAllUserStatements(username):
    ref = db.reference("/statements/" + username)
    return ref.get()

def genId():
    return uuid.uuid4()
