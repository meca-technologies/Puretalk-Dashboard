import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['jamesbon']
lead_col = db['leads']

search_query = {
    "_id":ObjectId("618c07c4a0037844d451a405")
}

update_query = {
    '$set':{
        'status':'completed',
        'time_taken':38
    }
}

lead = lead_col.find_one(search_query)
print(lead)