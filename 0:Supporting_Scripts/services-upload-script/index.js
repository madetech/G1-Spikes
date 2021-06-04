const TSV_FILE = "";
const DYNAMO_TABLE = "";

const EXPECTED_HEADERS = [
  "Title for website and text service",
  "Onward link",
  "Description for website and text service",
  "Support type",
  "Min age",
  "Max age",
  "National?",
  "Free?",
  "Service type",
  "Risk type",
];

function arraysEqual(a, b) {
  if (a === b) return true;
  if (a == null || b == null) return false;
  if (a.length !== b.length) return false;
  for (var i = 0; i < a.length; ++i) {
    if (a[i] !== b[i]) return false;
  }
  return true;
}

const handleError = (err) => {
  console.log(err);
  return err;
};

async function runScript(filename, tableName) {
  const tsvFile = require("fs").readFileSync(filename, "utf-8", (err, data) =>
    err ? handleError(err) : JSON.parse(data)
  );

  dynamoFormattedData = tsvToDynamo(tsvFile, tableName);
}

function tsvToDynamo(tsvData, tableName) {
  const putRequests = [];
  const tsvRows = tsvData.split("\r\n");
  const headers = tsvRows.shift().split("\t");

  if (
    !arraysEqual(headers.slice(0, EXPECTED_HEADERS.length), EXPECTED_HEADERS)
  ) {
    console.log("Headers did not match expected format");
    console.log(`Provided : ${headers.splice(0, 9)}`);
    console.log(`Expected : ${EXPECTED_HEADERS}`);
    return;
  }

  tsvRows.forEach((entry) => {
    putRequests.push({ PutRequest: tsvRowToDynamoItem(entry) });
  });

  const chunkedRequests = chunkRequests(tableName, putRequests);
  chunkedRequests.forEach((request) => pushToDynamo(request));
}

function tsvRowToDynamoItem(tsvRow) {
  const splitData = tsvRow.split("\t");
  const paidTags = splitData[7].split(",").map((tag) => {
    let cleanTag = tag.trim();
    switch (cleanTag) {
      case "yes":
      case "Yes":
        return "free";
      case "no":
      case "No":
      case "unsure":
        return "paid";
      default:
        return cleanTag;
    }
  });
  const tags = handleTags([
    splitData[3].split(","),
    splitData[6].split(","),
    paidTags,
    splitData[8].split(","),
    splitData[9].split(","),
  ]);
  const name = splitData[0].trim();
  const serviceId = name.replace(/ /g, "-");
  const url = splitData[1];
  const description = splitData[2].trim();
  minAge = parseInt(splitData[4]);
  maxAge = parseInt(splitData[5]);
  return {
    Item: {
      ServiceId: makeDynamoStringType(serviceId),
      Description: makeDynamoStringType(description),
      MaxAge: makeDynamoNumberType(
        (Number.isInteger(maxAge) ? maxAge : 100).toString()
      ),
      MinAge: makeDynamoNumberType(
        (Number.isInteger(minAge) ? minAge : 0).toString()
      ),
      Name: makeDynamoStringType(name),
      Tags: tags,
      URL: makeDynamoStringType(url),
    },
  };
}

function chunkRequests(tableName, allRequests) {
  const chunkedRequests = [];
  const numberOfRequests = Math.ceil(allRequests.length / 25);

  for (let i = 0; i < numberOfRequests; i++) {
    const current = i * 25;
    chunkedRequests.push({
      [tableName]: allRequests.slice(current, current + 25),
    });
  }

  return chunkedRequests;
}

function pushToDynamo(dynamoData) {
  const AWS = require("aws-sdk");
  AWS.config.update({ region: "eu-west-2" });

  const dynamo = new AWS.DynamoDB({ apiVersion: "2012-08-10" });

  const params = {
    RequestItems: dynamoData,
  };

  dynamo.batchWriteItem(params, (err, data) => {
    if (err) {
      handleError(err);
    } else {
      console.log("Success", data);
    }
  });
}

function makeDynamoStringType(string) {
  return { S: string ? string : "" };
}

function makeDynamoNumberType(number) {
  return { N: number };
}

function handleTags(tags) {
  const dynamoTags = tags
    .flat()
    .map((tag) =>
      makeDynamoStringType(
        `${tag[0].toLowerCase().trim()}${tag.substring(1).trim()}`
      )
    );

  return { L: dynamoTags };
}

if (TSV_FILE == "" || DYNAMO_TABLE == "") {
  console.log(
    "Either the filename or dynamo table has not been set. Please update these at the top of index.js"
  );
} else {
  runScript(TSV_FILE, DYNAMO_TABLE);
}
