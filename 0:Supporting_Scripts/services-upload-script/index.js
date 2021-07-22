const TSV_FILE = "Service A-Z - Services to include  (4).tsv";
const DYNAMO_TABLE = "cypmh-staging-service";

const EXPECTED_HEADERS = [
  "Title for website and text service",
  "Onward link (non-referral)",
  "Description for website and text service",
  "Support type",
  "Min age",
  "Max age",
  "National?",
  "Free?",
  "Service type",
  "Risk type",
  "Support Finder & Text Bot Rank", //10 Number
  "List of Services Rank", //11 Number
  "Tent Service?", //12 Boolean (TRUE OR FALSE)
  "Tent Service Redirect", //13 string
  "Text Bot Referral Description", // String
  "Text Bot Referral Start word", // String
  "Text Referral Available?", // String
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
    console.log(`Provided : ${headers.splice(0, EXPECTED_HEADERS.length)}`);
    console.log(`Expected : ${EXPECTED_HEADERS}`);
    return;
  }

  tsvRows.forEach((entry, index) => {
    putRequests.push({ PutRequest: tsvRowToDynamoItem(entry,index) });
  });
  const chunkedRequests = chunkRequests(tableName, putRequests);
  chunkedRequests.forEach(async (request) => await pushToDynamo(request));
}

function tsvRowToDynamoItem(tsvRow,index) {
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
  const serviceId = `${name.replace(/ /g, "-")}-${index}`;
  const url = splitData[1];
  const description = splitData[2].trim();
  minAge = parseInt(splitData[4]);
  maxAge = parseInt(splitData[5]);

  const dynamoItem = {
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

  const supportFinderAndTextBotRank = splitData[10].trim();
  const listOfServiceRanks = splitData[11].trim();
  const tentService = splitData[12].trim();
  const tentServiceRedirect = splitData[13].trim();
  const textBotReferralDescription = splitData[14].trim();
  const textBotReferralStartWord = splitData[15].trim();
  const textReferralAvailable = splitData[16].trim();

  if (supportFinderAndTextBotRank !== "") {
    dynamoItem.Item.SupportFinderAndTextBotRank = makeDynamoNumberType(
      parseInt(supportFinderAndTextBotRank).toString()
    );
  }

  if (listOfServiceRanks !== "") {
    dynamoItem.Item.ListOfServicesRank = makeDynamoNumberType(
      parseInt(listOfServiceRanks).toString()
    );
  }

  if (tentService === "TRUE") {
    dynamoItem.Item.IsTentService = makeDynamoStringType(tentService);
  }

  if (tentServiceRedirect !== "") {
    dynamoItem.Item.TentRedirectUrl = makeDynamoStringType(tentServiceRedirect);
  }
  if (textBotReferralDescription !== "") {
    dynamoItem.Item.TextBotReferralDescription = makeDynamoStringType(
      textBotReferralDescription
    );
  }
  if (textBotReferralStartWord !== "") {
    dynamoItem.Item.TextBotReferralStartWord = makeDynamoStringType(
      textBotReferralStartWord
    );
  }
  if (textReferralAvailable === "TRUE") {
    dynamoItem.Item.TextReferralAvailable = makeDynamoStringType(
      textReferralAvailable
    );
  }

  return dynamoItem;
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

async function pushToDynamo(dynamoData) {
  const AWS = require("aws-sdk");
  AWS.config.update({ region: "eu-west-2" });

  const dynamo = new AWS.DynamoDB({ apiVersion: "2012-08-10" });

  const params = {
    RequestItems: dynamoData,
  };

  await dynamo.batchWriteItem(params, (err, data) => {
    if (err) {
      console.log(params);
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
    .filter((tag) => tag.trim() !== "")
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
