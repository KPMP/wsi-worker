const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
const fs = require('fs');

const url = 'mongodb://delphinus-mongodb:27017';
const dbName = 'knowledgeEnvironment';

const kpmpId = process.argv[2];
const slideName = process.argv[3];
const fileUUID = process.argv[4];
const stainType = process.argv[5];
const metadataFile = process.argv[6];
let rawdata = fs.readFileSync(metadataFile);
let metadata = JSON.parse(rawdata);

const addAndUpdateParticipants = function (db, callback) {

	let stainCollection = db.collection("stains");

	stainCollection.find().toArray(function (err, stainDocuments) {
		assert.equal(null, err);

		let stainsByType = {};
		stainDocuments.forEach(stain => {
			stainsByType[stain.type] = stain;
		});

		let participantCollection = db.collection("patients");

		participantCollection.find({ kpmp_id: kpmpId }).toArray(function (err, docs) {
			assert.equal(null, err);

			let asyncWrapper = new Promise((resolve, reject) => {
				docs.forEach(function (doc, index, array) {
					let slides = doc.slides;
					let exists = false;
					let added = false;

					slides.forEach(slide => {
						if (slide.slideName === slideName) {
							exists = true;
						}
					});

					if (!exists) {
						if (stainsByType[stainType] !== null && stainsByType[stainType] !== undefined) {

							slides.push({
								_id: fileUUID,
								slideName: slideName,
								metadata: metadata,
								stain: stainsByType[stainType]
							});

							console.log("--- adding new slide, fileUUID: " + fileUUID);
							participantCollection.update({ _id: doc._id }, { $set: { slides: slides } });
							added = true;
						} else {
							console.log("***** ERROR: Unable to find stain type *****");
						}
					}

					if (!added) {
						console.log('... no slides added');
					}
					if (index === array.length - 1) resolve();
				});
			});
			asyncWrapper.then(() => {
				callback()
			});
			if (docs.length === 0) {
				if (stainsByType[stainType] !== null && stainsByType[stainType] !== undefined) {

					let participantRecord = {
						kpmp_id: kpmpId,
						label: kpmpId,
						slides: [{
							_id: fileUUID,
							slideName: slideName,
							metadata: metadata,
							stain: stainsByType[stainType]
						}]
					};

					console.log("--- adding new participant and slides, KPMP_ID: " + kpmpId);
					participantCollection.insertOne(participantRecord, function () {
						callback();
					});
				} else {
					console.log("***** ERROR: Unable to find stain type *****");
					callback();
				}
			}
		});
	});
};

MongoClient.connect(url, { useUnifiedTopology: true }, function (err, client) {
	assert.equal(null, err);

	const db = client.db(dbName);

	addAndUpdateParticipants(db, function () {
		client.close();
	});
});
