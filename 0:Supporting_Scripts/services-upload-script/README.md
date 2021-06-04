# CYPMH Services Uploader

This is a simple Node.js script that will allow you to upload services from a tsv file into our DynamoDB tables.

## Installation

We assume that both NodeJs and Yarn are installed on the machine.

Pull down the script, and run `yarn` to install dependencies.

## Upload services

1. Remove current services from DynamoDB Table.
2. Move your .tsv file into the root level of the project.
3. Update the `TSV_FILE` and `DYNAMO_TABLE` constant values inside of `index.js`. e.g. `TSV_FILE="services.tsv` and `DYNAMO_TABLE="services_table"`.
4. Execute the script using `node index.js` (using aws-vault this would be `aws-vault exec <profile> -- node index.js`).

_Please note, this script assumes the headings of the tsv file match those defined in `EXPECTED_HEADERS` inside of `index.js`, the ordering is also assumed._
