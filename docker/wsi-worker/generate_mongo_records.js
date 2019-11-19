const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');

const url = 'mongodb://delphinus-mongodb:27017';
const dbName = 'knowledgeEnvironment';

const kpmpId = process.argv[2];
const slideName = process.argv[3];
const fileUUID = process.argv[4];
const stainType = process.argv[5];

const addAndUpdateParticipants = function(db, callback) {

	let stainCollection = db.collection("stains");

	stainCollection.find().toArray(function(err, stainDocuments) {
		assert.equal(null, err);

		let stainsByType = {};
		stainDocuments.forEach(stain => {
			stainsByType[stain.type] = stain;
		});

		let participantCollection = db.collection("patients");

		participantCollection.find({ kpmp_id: kpmpId }).toArray(function(err, docs) {
			assert.equal(null, err);

			docs.forEach(function(doc) {
				console.log("--- found existing participant, KPMP_ID: " + kpmpId);
				let slides = doc.slides;
				let exists = false;
				let added = false;

				slides.forEach(slide => {
					if(slide.slideName === slideName) {
						exists = true;
					}
				});

				if (!exists) {
					slides.push({
						_id: fileUUID,
						slideName: slideName,
						stain: stainsByType[stainType]
					});

					console.log("--- adding new slide, fileUUID: " + fileUUID);
					participantCollection.update({ _id: doc._id }, { $set: { slides: slides }});
					added = true;
				}

				if(!added) {
					console.log('... no slides added');
				}
			});

			if (docs.length === 0) {
				let participantRecord = {
					kpmp_id: kpmpId,
					label: kpmpId,
					slides: [ {
						_id: fileUUID,
						slideName: slideName,
						stain: stainsByType[stainType]
					}]
				};

				console.log("--- adding new participant and slides, KPMP_ID: " + kpmpId);
				participantCollection.insertOne(participantRecord);
			}
			callback();
		});
	});
};

MongoClient.connect(url, { useUnifiedTopology: true }, function(err, client) {
	assert.equal(null, err);

	const db = client.db(dbName);

	addAndUpdateParticipants(db, function() {
		client.close();
	});
});
