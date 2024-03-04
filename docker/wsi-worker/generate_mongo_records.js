const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
const fs = require('fs');

const url = 'mongodb://delphinus-mongodb:27017';
const dbName = 'knowledgeEnvironment';

const kpmpId = process.argv[2];
const slideName = process.argv[3];
const fileUUID = process.argv[4];
const slideType = process.argv[5];
const stainType = process.argv[6];
const metadataFile = process.argv[7];

const addAndUpdateParticipants = function (db, callback) {
	let metadata = null;
	if (slideType === "LM" && fs.existsSync(metadataFile)) {
		let rawdata = fs.readFileSync(metadataFile);
		metadata = JSON.parse(rawdata);
	}

	let stainCollection = db.collection("stains");

	stainCollection.find().toArray(function (err, stainDocuments) {
		assert.equal(null, err);

		let stainsByType = {};
		stainDocuments.forEach(stain => {
			stainsByType[stain.type] = stain;
		});

		let slideTypeFull = "";
		switch (slideType.toUpperCase()) {
			case "LM":
				slideTypeFull = "(LM) Light Microscopy";
				break;
			case "EM":
				slideTypeFull = "(EM) Electron Microscopy";
				break;
			case "IF":
				slideTypeFull = "(IF) Immunofluorescence";
				break;
			default:
				break;
		}

		let participantCollection = db.collection("patients");

		participantCollection.find({ kpmp_id: kpmpId }).toArray(function (err, docs) {
			assert.equal(null, err);

			let asyncWrapper = new Promise((resolve, reject) => {
				docs.forEach(function (doc, index, array) {
					let slides = doc.slides;
					let exists = false;
					let added = false;

					slides.forEach(slide => {
						if (slideType === "LM" && slide.slideName === slideName) {
							slide = slide['metadata'] = metadata;
							participantCollection.update({_id: doc._id }, { $set: { slides: slides }});
							console.log("updated slide with metadata");
							exists = true;
						}
					});

					if (!exists) {
						if (stainsByType[stainType] !== null && stainsByType[stainType] !== undefined) {
							if (slideType === "LM") {
								slides.push({
									_id: fileUUID,
									slideName: slideName,
									metadata: metadata,
									stain: stainsByType[stainType],
									slideType: slideTypeFull
								});
							}
							else {
								slides.push({
									_id: fileUUID,
									slideName: slideName,
									stain: stainsByType[stainType],
									slideType: slideTypeFull
								});
							}

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
							stain: stainsByType[stainType],
							slideType: slideTypeFull
						}]
					};
					if (slideType === "LM") {
						participantRecord.slides[0].metadata = metadata;
					}

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
