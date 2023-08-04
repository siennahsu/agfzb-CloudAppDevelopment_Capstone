/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
var params = {
    "COUCH_URL": "https://1f70d18e-2c41-41f7-9fe4-c7806acd9a8e-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "kd1Cl515onirvb1ZB0B1a9mafZ8Ld1z1VyQ7CFYbvgcJ",
    "COUCH_USERNAME": "1f70d18e-2c41-41f7-9fe4-c7806acd9a8e-bluemix"
};


async function main(params) {
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(params.COUCH_URL);
      try {
        let dbList = await cloudant.getAllDbs();
        return { "dbs": dbList.result };
      } catch (error) {
          return { error: error.description };
      }
}

