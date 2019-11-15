const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');

const url = 'mongodb://delphinus-mongodb:27017';
const dbName = 'knowledgeEnvironment';

var kpmpId = process.argv[2];
var slideName = process.argv[3];
var fileUUID = process.argv[4];

const addAndUpdateParticipants = function(db, callback) {
	var participantCollection = db.collection("patients");
	var query = { kpmp_id: kpmpId };

	participantCollection.find(query).toArray(function(err, docs) {
		assert.equal(null, err);
		docs.forEach(function(doc) {
			var slides = doc.slides;
			var exists = false;
			slides.forEach(slide => {
				if(slide.slideName === slideName) {
					exists = true;
				}
			});
			if (!exists) {
				console.log("adding new slide")
				// Not adding the stain type because we aren't using in DPR
				slides.push({ _id: fileUUID, slideName: slideName });
				participantCollection.update({ _id: doc._id }, { $set: { slides: slides }});
			}
		});
		if (docs.length === 0) {
			var participantRecord = {
				kpmpId: kpmpId,
				label: kpmpId,
				slides: [ {
					_id: fileUUID,
					slideName: slideName
				}]
			};
			participantCollection.insertOne(participantRecord);
		}
		callback();
	});

}


MongoClient.connect(url, function(err, client) {
	assert.equal(null, err);
	
	const db = client.db(dbName);
	
	addAndUpdateParticipants(db, function() {
		client.close();
	});

});
